import calendar
from collections import defaultdict
from datetime import UTC, datetime, timedelta

from domains.entities.stats_entities import (
    ChatStatistics,
    DailyStats,
    EnergyUsage,
    MessageDistribution,
    ModelUsageStats,
    ThinkingTime,
    TimelineDataPoint,
    TokenUsage,
    UsageOverview,
    UsagePatterns,
    UsagePeriod,
    UsageSummary,
    UsageTimeline,
    UserStats,
    WeeklyConversationStats,
)
from dtos.stats_dto import (
    MessageDistributionDTO,
    UsageOverviewDTO,
    UsagePatternsDTO,
    UsageTimelineDTO,
    UserStatsDTO,
    WeeklyConversationStatsDTO,
)
from mappers.stats_mapper import StatsMapper
from repositories.stats_repository import StatsRepository
from supabase import Client
from utils.stats_helpers import (
    CO2_PER_KWH,
    ENERGY_COST_PER_INPUT_TOKEN,
    ENERGY_COST_PER_OUTPUT_TOKEN,
    JOULES_PER_WH,
    calculate_cost,
    energy_to_equivalent,
    estimate_tokens,
    fetch_all_paginated,
    parse_datetime_safe,
)


class StatsService:
    @staticmethod
    def get_user_stats(client: Client, user_id: str, recent_days: int = 7) -> UserStatsDTO:
        """Get comprehensive user statistics"""
        current_date = datetime.now()
        recent_date = current_date - timedelta(days=recent_days)
        recent_date_str = recent_date.strftime("%Y-%m-%d")

        # Get chats
        chats = StatsRepository.get_user_chats(client, user_id)
        total_chats = len(chats)

        recent_chats = [c for c in chats if (c.created_at or "") >= recent_date_str]
        recent_chats_count = len(recent_chats)

        # Get messages
        messages = StatsRepository.get_user_messages(client, user_id)
        total_messages = len(messages)

        # Calculate average messages per chat
        conv_msg_counts = {}
        for m in messages:
            cid = m.chat_provider_id
            if cid:
                conv_msg_counts[cid] = conv_msg_counts.get(cid, 0) + 1

        avg_messages_per_chat = round(total_messages / total_chats, 2) if total_chats else 0

        # Token and energy usage
        recent_input, recent_output, all_input, all_output = 0, 0, 0, 0
        recent_messages = [m for m in messages if (m.created_at or "") >= recent_date_str]

        for msg in messages:
            tokens = estimate_tokens(msg.content or "")
            if msg.role == "user":
                all_input += tokens
                if msg in recent_messages:
                    recent_input += tokens
            else:
                all_output += tokens
                if msg in recent_messages:
                    recent_output += tokens

        all_tokens = all_input + all_output
        recent_tokens = recent_input + recent_output

        all_energy_wh = (
            all_input * ENERGY_COST_PER_INPUT_TOKEN + all_output * ENERGY_COST_PER_OUTPUT_TOKEN
        ) / JOULES_PER_WH
        recent_energy_wh = (
            recent_input * ENERGY_COST_PER_INPUT_TOKEN + recent_output * ENERGY_COST_PER_OUTPUT_TOKEN
        ) / JOULES_PER_WH

        # Thinking time
        thinking_times = []
        msg_lookup = {m.message_provider_id: m for m in messages if m.message_provider_id}

        for msg in messages:
            if msg.role == "assistant" and msg.parent_message_provider_id and msg.created_at:
                parent_msg = msg_lookup.get(msg.parent_message_provider_id)
                if parent_msg and parent_msg.created_at:
                    try:
                        t1 = datetime.fromisoformat(msg.created_at.replace("Z", "+00:00"))
                        t0 = datetime.fromisoformat(parent_msg.created_at.replace("Z", "+00:00"))
                        diff = (t1 - t0).total_seconds()
                        if 0.1 <= diff <= 60:
                            thinking_times.append(diff)
                    except Exception:
                        pass

        avg_thinking_time = round(sum(thinking_times) / len(thinking_times), 2) if thinking_times else 2.5
        total_thinking_time = (
            round(sum(thinking_times), 2) if thinking_times else round(avg_thinking_time * total_messages, 2)
        )

        # Message count per day (last N days)
        messages_per_day = {(current_date - timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(recent_days)}
        for msg in messages:
            if msg.created_at:
                date = msg.created_at.split("T")[0]
                if date in messages_per_day:
                    messages_per_day[date] += 1

        # Efficiency score
        messages_score = 100 - min(abs(avg_messages_per_chat - 5) * 10, 100)
        token_score = (all_output / all_input * 100) if all_input else 50
        response_time_score = 100 - min((avg_thinking_time / 3) * 10, 100)
        energy_per_token_mwh = (all_energy_wh * 1000) / all_tokens if all_tokens else 0
        energy_score = 100 - min(energy_per_token_mwh * 10, 100)
        efficiency_score = round((messages_score + token_score + response_time_score + energy_score) / 4)

        # Model usage
        model_usage = {}
        for msg in messages:
            model = msg.model or "unknown"
            if model not in model_usage:
                model_usage[model] = {"count": 0, "input_tokens": 0, "output_tokens": 0}
            model_usage[model]["count"] += 1
            tok = estimate_tokens(msg.content or "")
            if msg.role == "user":
                model_usage[model]["input_tokens"] += tok
            else:
                model_usage[model]["output_tokens"] += tok

        # Chats per day
        chats_per_day = {(current_date - timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(recent_days)}
        for chat in chats:
            if chat.created_at:
                date = chat.created_at.split("T")[0]
                if date in chats_per_day:
                    chats_per_day[date] += 1

        # Sort by date
        chats_per_day = dict(sorted(chats_per_day.items()))

        # Build entity
        model_usage_entities = {k: ModelUsageStats(**v) for k, v in model_usage.items()}

        entity = UserStats(
            total_chats=total_chats,
            recent_chats=recent_chats_count,
            total_messages=total_messages,
            avg_messages_per_chat=avg_messages_per_chat,
            messages_per_day=messages_per_day,
            chats_per_day=chats_per_day,
            token_usage=TokenUsage(
                recent=recent_tokens,
                recent_input=recent_input,
                recent_output=recent_output,
                total=all_tokens,
                total_input=all_input,
                total_output=all_output,
            ),
            energy_usage=EnergyUsage(
                recent_wh=round(recent_energy_wh, 4),
                total_wh=round(all_energy_wh, 4),
                per_message_wh=round(all_energy_wh / total_messages, 6) if total_messages else 0,
                equivalent=energy_to_equivalent(all_energy_wh),
            ),
            thinking_time=ThinkingTime(average=avg_thinking_time, total=total_thinking_time),
            efficiency=efficiency_score,
            model_usage=model_usage_entities,
        )

        # Map entity to DTO
        return StatsMapper.to_user_stats_dto(entity)

    @staticmethod
    def get_weekly_conversation_stats(client: Client, user_id: str, days: int = 7) -> WeeklyConversationStatsDTO:
        """Get conversation statistics for the specified number of days"""
        start_date = (datetime.now(UTC) - timedelta(days=days)).isoformat()

        # Get chats from last N days
        chats = StatsRepository.get_user_chats(client, user_id, start_date)
        conversation_ids = [conv.chat_provider_id for conv in chats if conv.chat_provider_id]

        if not conversation_ids:
            entity = WeeklyConversationStats(total_conversations=0, total_messages=0, daily_breakdown=[])
            return StatsMapper.to_weekly_conversation_stats_dto(entity)

        # Get messages from those chats
        messages = StatsRepository.get_chat_message_count(client, user_id, conversation_ids, start_date)

        # Calculate daily breakdown
        daily_stats = {}
        for i in range(days):
            date = (datetime.now(UTC) - timedelta(days=i)).date()
            daily_stats[str(date)] = {"date": str(date), "conversations": 0, "messages": 0}

        # Count conversations per day
        for conv in chats:
            conv_date = str(parse_datetime_safe(conv.created_at).date())
            if conv_date in daily_stats:
                daily_stats[conv_date]["conversations"] += 1

        # Count messages per day
        for msg in messages:
            msg_date = str(parse_datetime_safe(msg.created_at).date())
            if msg_date in daily_stats:
                daily_stats[msg_date]["messages"] += 1

        daily_list = [
            DailyStats(**stats) for stats in sorted(daily_stats.values(), key=lambda x: x["date"], reverse=True)
        ]

        entity = WeeklyConversationStats(
            total_conversations=len(chats), total_messages=len(messages), daily_breakdown=daily_list
        )

        # Map entity to DTO
        return StatsMapper.to_weekly_conversation_stats_dto(entity)

    @staticmethod
    def get_message_distribution(client: Client, user_id: str) -> MessageDistributionDTO:
        """Get message distribution by role and model"""
        messages = StatsRepository.get_user_messages(client, user_id)

        if not messages:
            entity = MessageDistribution(by_role={}, by_model={}, total_messages=0)
            return StatsMapper.to_message_distribution_dto(entity)

        # Calculate distribution by role
        by_role = {}
        for msg in messages:
            role = msg.role or "unknown"
            by_role[role] = by_role.get(role, 0) + 1

        # Calculate distribution by model
        by_model = {}
        for msg in messages:
            model = msg.model or "unknown"
            by_model[model] = by_model.get(model, 0) + 1

        entity = MessageDistribution(by_role=by_role, by_model=by_model, total_messages=len(messages))

        # Map entity to DTO
        return StatsMapper.to_message_distribution_dto(entity)

    @staticmethod
    def get_usage_overview(client: Client, user_id: str, days: int = 30) -> UsageOverviewDTO:
        """Get comprehensive usage overview"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Fetch messages with pagination
        def fetch_messages_batch(offset, limit):
            return StatsRepository.get_messages_paginated(client, user_id, start_date.isoformat(), offset, limit)

        messages = fetch_all_paginated(fetch_messages_batch)

        # Fetch chats with pagination
        def fetch_chats_batch(offset, limit):
            return StatsRepository.get_chats_paginated(client, user_id, start_date.isoformat(), offset, limit)

        chats = fetch_all_paginated(fetch_chats_batch)

        # Calculate metrics
        total_messages = len(messages)
        total_chats = len(chats)

        # Token and cost analysis
        total_input_tokens = 0
        total_output_tokens = 0
        total_cost = 0.0
        model_usage = defaultdict(lambda: {"messages": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0})
        provider_usage = defaultdict(
            lambda: {"messages": 0, "chats": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0}
        )

        # Build chat provider mapping
        chat_providers = {}
        for chat in chats:
            chat_provider_id = chat.chat_provider_id
            provider_name = chat.provider_name
            if chat_provider_id and provider_name:
                chat_providers[chat_provider_id] = provider_name
                provider_usage[provider_name]["chats"] += 1

        for msg in messages:
            content = msg.content or ""
            model = msg.model or "unknown"
            role = msg.role
            chat_provider_id = msg.chat_provider_id

            tokens = estimate_tokens(content)

            if role == "user":
                total_input_tokens += tokens
                model_usage[model]["input_tokens"] += tokens
            else:
                total_output_tokens += tokens
                model_usage[model]["output_tokens"] += tokens

            model_usage[model]["messages"] += 1

            # Calculate cost
            input_tokens = tokens if role == "user" else 0
            output_tokens = tokens if role != "user" else 0
            cost = calculate_cost(model, input_tokens, output_tokens)
            total_cost += cost
            model_usage[model]["cost"] += cost

            # Provider analysis
            provider = chat_providers.get(chat_provider_id, "unknown")
            provider_usage[provider]["messages"] += 1
            provider_usage[provider]["input_tokens"] += input_tokens
            provider_usage[provider]["output_tokens"] += output_tokens
            provider_usage[provider]["cost"] += cost

        # Calculate avg messages per chat for each provider
        for _, stats in provider_usage.items():
            if stats["chats"] > 0:
                stats["avg_messages_per_chat"] = round(stats["messages"] / stats["chats"], 1)
            else:
                stats["avg_messages_per_chat"] = 0

        # Energy and environmental impact
        total_energy_wh = (
            total_input_tokens * ENERGY_COST_PER_INPUT_TOKEN + total_output_tokens * ENERGY_COST_PER_OUTPUT_TOKEN
        ) / JOULES_PER_WH
        co2_emissions_kg = (total_energy_wh / 1000) * CO2_PER_KWH

        # Chat statistics
        chat_stats = StatsService._get_chat_statistics(client, user_id, chats, messages, days)

        # Top providers
        top_providers = []
        filtered_providers = {k: v for k, v in provider_usage.items() if k != "unknown"}
        sorted_providers = sorted(filtered_providers.items(), key=lambda x: x[1]["chats"], reverse=True)
        for i, (provider_name, stats) in enumerate(sorted_providers[:3]):
            top_providers.append({"name": provider_name, "chats": stats["chats"], "rank": i + 1})

        entity = UsageOverview(
            period=UsagePeriod(days=days, start_date=start_date.isoformat(), end_date=end_date.isoformat()),
            summary=UsageSummary(
                total_messages=total_messages,
                total_chats=total_chats,
                total_tokens=total_input_tokens + total_output_tokens,
                input_tokens=total_input_tokens,
                output_tokens=total_output_tokens,
                estimated_cost_usd=round(total_cost, 4),
                energy_consumption_wh=round(total_energy_wh, 4),
                co2_emissions_kg=round(co2_emissions_kg, 6),
                avg_messages_per_chat=round(total_messages / total_chats, 2) if total_chats > 0 else 0,
                most_used_provider=top_providers[0]["name"] if top_providers else None,
                top_providers=top_providers,
            ),
            model_breakdown=dict(model_usage),
            provider_breakdown=dict(provider_usage),
            chat_statistics=chat_stats,
        )

        # Map entity to DTO
        return StatsMapper.to_usage_overview_dto(entity)

    @staticmethod
    def _get_chat_statistics(client: Client, user_id: str, chats: list, messages: list, days: int) -> ChatStatistics:
        """Helper to calculate chat statistics"""
        if not chats:
            return ChatStatistics(
                total_chats=0,
                avg_messages_per_chat=0,
                longest_chat=None,
                chat_distribution_by_provider={},
                recent_chats=[],
            )

        # Count messages per chat
        chat_message_counts = defaultdict(int)
        valid_chat_ids = {chat.chat_provider_id for chat in chats if chat.chat_provider_id}

        for message in messages:
            chat_provider_id = message.chat_provider_id
            if chat_provider_id and chat_provider_id in valid_chat_ids:
                chat_message_counts[chat_provider_id] += 1

        # Enrich chats with message counts
        enriched_chats = []
        for chat in chats:
            chat_provider_id = chat.chat_provider_id
            message_count = chat_message_counts.get(chat_provider_id, 0)
            if message_count > 0:
                enriched_chats.append(
                    {
                        "id": chat.id,
                        "chat_provider_id": chat.chat_provider_id,
                        "title": chat.title,
                        "provider_name": chat.provider_name,
                        "created_at": chat.created_at,
                        "message_count": message_count,
                    }
                )

        total_chats = len(enriched_chats)
        total_messages = sum(chat["message_count"] for chat in enriched_chats)
        avg_messages_per_chat = total_messages / total_chats if total_chats > 0 else 0

        # Find longest chat
        longest_chat = max(enriched_chats, key=lambda x: x["message_count"]) if enriched_chats else None
        if longest_chat:
            longest_chat = {
                "id": str(longest_chat["id"]),
                "title": longest_chat.get("title"),
                "message_count": longest_chat["message_count"],
                "provider_name": longest_chat.get("provider_name"),
                "chat_provider_id": longest_chat.get("chat_provider_id"),
                "created_at": longest_chat["created_at"],
            }

        # Provider distribution
        provider_distribution = defaultdict(int)
        for chat in enriched_chats:
            provider = chat.get("provider_name") or "Unknown"
            provider_distribution[provider] += 1

        # Recent chats (top 10)
        recent_chats = sorted(enriched_chats, key=lambda x: x["created_at"], reverse=True)[:10]
        recent_chats = [
            {
                "id": str(chat["id"]),
                "title": chat.get("title"),
                "message_count": chat["message_count"],
                "provider_name": chat.get("provider_name"),
                "created_at": chat["created_at"],
            }
            for chat in recent_chats
        ]

        return ChatStatistics(
            total_chats=total_chats,
            avg_messages_per_chat=round(avg_messages_per_chat, 1),
            longest_chat=longest_chat,
            chat_distribution_by_provider=dict(provider_distribution),
            recent_chats=recent_chats,
        )

    @staticmethod
    def get_usage_timeline(
        client: Client, user_id: str, days: int = 30, granularity: str = "daily"
    ) -> UsageTimelineDTO:
        """Get usage timeline data"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Fetch messages with pagination
        def fetch_messages_batch(offset, limit):
            return StatsRepository.get_messages_paginated(client, user_id, start_date.isoformat(), offset, limit)

        messages = fetch_all_paginated(fetch_messages_batch)

        # Fetch chats with pagination
        def fetch_chats_batch(offset, limit):
            return StatsRepository.get_chats_paginated(client, user_id, start_date.isoformat(), offset, limit)

        chats = fetch_all_paginated(fetch_chats_batch)

        # Filter chats with messages
        if chats:
            chat_ids = {chat.chat_provider_id for chat in chats if chat.chat_provider_id}
            chat_message_counts = defaultdict(int)

            for message in messages:
                chat_provider_id = message.chat_provider_id
                if chat_provider_id and chat_provider_id in chat_ids:
                    chat_message_counts[chat_provider_id] += 1

            chats = [chat for chat in chats if chat_message_counts.get(chat.chat_provider_id, 0) > 0]

        # Group by time periods
        timeline_data = defaultdict(
            lambda: {"messages": 0, "chats": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0, "energy_wh": 0.0}
        )

        for msg in messages:
            created_at = parse_datetime_safe(msg.created_at)

            # Determine time bucket
            if granularity == "hourly":
                time_key = created_at.strftime("%Y-%m-%d %H:00")
            elif granularity == "weekly":
                week_start = created_at - timedelta(days=created_at.weekday())
                time_key = week_start.strftime("%Y-%m-%d")
            else:
                time_key = created_at.strftime("%Y-%m-%d")

            content = msg.content or ""
            model = msg.model or "unknown"
            role = msg.role
            tokens = estimate_tokens(content)

            timeline_data[time_key]["messages"] += 1

            if role == "user":
                timeline_data[time_key]["input_tokens"] += tokens
                cost = calculate_cost(model, tokens, 0)
                energy = tokens * ENERGY_COST_PER_INPUT_TOKEN / JOULES_PER_WH
            else:
                timeline_data[time_key]["output_tokens"] += tokens
                cost = calculate_cost(model, 0, tokens)
                energy = tokens * ENERGY_COST_PER_OUTPUT_TOKEN / JOULES_PER_WH

            timeline_data[time_key]["cost"] += cost
            timeline_data[time_key]["energy_wh"] += energy

        # Process chats
        for chat in chats:
            created_at = parse_datetime_safe(chat.created_at)

            if granularity == "hourly":
                time_key = created_at.strftime("%Y-%m-%d %H:00")
            elif granularity == "weekly":
                week_start = created_at - timedelta(days=created_at.weekday())
                time_key = week_start.strftime("%Y-%m-%d")
            else:
                time_key = created_at.strftime("%Y-%m-%d")

            timeline_data[time_key]["chats"] += 1

        # Convert to list
        timeline_list = []
        for time_key in sorted(timeline_data.keys()):
            data = timeline_data[time_key]
            timeline_list.append(
                TimelineDataPoint(
                    timestamp=time_key,
                    messages=data["messages"],
                    chats=data["chats"],
                    input_tokens=data["input_tokens"],
                    output_tokens=data["output_tokens"],
                    total_tokens=data["input_tokens"] + data["output_tokens"],
                    cost_usd=round(data["cost"], 4),
                    energy_wh=round(data["energy_wh"], 4),
                )
            )

        entity = UsageTimeline(
            granularity=granularity,
            period=UsagePeriod(days=days, start_date=start_date.isoformat(), end_date=end_date.isoformat()),
            timeline=timeline_list,
        )

        # Map entity to DTO
        return StatsMapper.to_usage_timeline_dto(entity)

    @staticmethod
    def get_usage_patterns(client: Client, user_id: str, days: int = 30) -> UsagePatternsDTO:
        """Get usage patterns (time of day, day of week)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Fetch messages with pagination
        def fetch_messages_batch(offset, limit):
            return StatsRepository.get_messages_paginated(client, user_id, start_date.isoformat(), offset, limit)

        messages = fetch_all_paginated(fetch_messages_batch)

        # Initialize patterns
        hourly_usage = {str(i): 0 for i in range(24)}
        daily_usage = {calendar.day_name[i]: 0 for i in range(7)}

        for msg in messages:
            created_at = parse_datetime_safe(msg.created_at)

            # Hour of day
            hour = str(created_at.hour)
            hourly_usage[hour] += 1

            # Day of week
            day_name = calendar.day_name[created_at.weekday()]
            daily_usage[day_name] += 1

        entity = UsagePatterns(
            period=UsagePeriod(days=days, start_date=start_date.isoformat(), end_date=end_date.isoformat()),
            hourly_distribution=hourly_usage,
            daily_distribution=daily_usage,
            peak_hour=max(hourly_usage.items(), key=lambda x: x[1])[0] if any(hourly_usage.values()) else "0",
            peak_day=max(daily_usage.items(), key=lambda x: x[1])[0] if any(daily_usage.values()) else "Monday",
        )

        # Map entity to DTO
        return StatsMapper.to_usage_patterns_dto(entity)
