from domains.entities.stats_entities import (
    MessageDistribution,
    UsageOverview,
    UsagePatterns,
    UsageTimeline,
    UserStats,
    WeeklyConversationStats,
)
from dtos.stats_dto import (
    ChatStatisticsDTO,
    DailyStatsDTO,
    EnergyUsageDTO,
    MessageDistributionDTO,
    ModelBreakdownDTO,
    ModelUsageStatsDTO,
    ProviderBreakdownDTO,
    ThinkingTimeDTO,
    TimelineDataPointDTO,
    TokenUsageDTO,
    TopProviderDTO,
    UsageOverviewDTO,
    UsagePatternsDTO,
    UsagePeriodDTO,
    UsageSummaryDTO,
    UsageTimelineDTO,
    UserStatsDTO,
    WeeklyConversationStatsDTO,
)


class StatsMapper:
    @staticmethod
    def to_user_stats_dto(entity: UserStats) -> UserStatsDTO:
        return UserStatsDTO(
            total_chats=entity.total_chats,
            recent_chats=entity.recent_chats,
            total_messages=entity.total_messages,
            avg_messages_per_chat=entity.avg_messages_per_chat,
            messages_per_day=entity.messages_per_day,
            chats_per_day=entity.chats_per_day,
            token_usage=TokenUsageDTO(
                recent=entity.token_usage.recent,
                recent_input=entity.token_usage.recent_input,
                recent_output=entity.token_usage.recent_output,
                total=entity.token_usage.total,
                total_input=entity.token_usage.total_input,
                total_output=entity.token_usage.total_output,
            ),
            energy_usage=EnergyUsageDTO(
                recent_wh=entity.energy_usage.recent_wh,
                total_wh=entity.energy_usage.total_wh,
                per_message_wh=entity.energy_usage.per_message_wh,
                equivalent=entity.energy_usage.equivalent,
            ),
            thinking_time=ThinkingTimeDTO(average=entity.thinking_time.average, total=entity.thinking_time.total),
            efficiency=entity.efficiency,
            model_usage={
                k: ModelUsageStatsDTO(count=v.count, input_tokens=v.input_tokens, output_tokens=v.output_tokens)
                for k, v in entity.model_usage.items()
            },
        )

    @staticmethod
    def to_weekly_conversation_stats_dto(entity: WeeklyConversationStats) -> WeeklyConversationStatsDTO:
        return WeeklyConversationStatsDTO(
            total_conversations=entity.total_conversations,
            total_messages=entity.total_messages,
            daily_breakdown=[
                DailyStatsDTO(date=day.date, conversations=day.conversations, messages=day.messages)
                for day in entity.daily_breakdown
            ],
        )

    @staticmethod
    def to_message_distribution_dto(entity: MessageDistribution) -> MessageDistributionDTO:
        return MessageDistributionDTO(
            by_role=entity.by_role, by_model=entity.by_model, total_messages=entity.total_messages
        )

    @staticmethod
    def to_usage_overview_dto(entity: UsageOverview) -> UsageOverviewDTO:
        return UsageOverviewDTO(
            period=UsagePeriodDTO(
                days=entity.period.days, start_date=entity.period.start_date, end_date=entity.period.end_date
            ),
            summary=UsageSummaryDTO(
                total_messages=entity.summary.total_messages,
                total_chats=entity.summary.total_chats,
                total_tokens=entity.summary.total_tokens,
                input_tokens=entity.summary.input_tokens,
                output_tokens=entity.summary.output_tokens,
                estimated_cost_usd=entity.summary.estimated_cost_usd,
                energy_consumption_wh=entity.summary.energy_consumption_wh,
                co2_emissions_kg=entity.summary.co2_emissions_kg,
                avg_messages_per_chat=entity.summary.avg_messages_per_chat,
                most_used_provider=entity.summary.most_used_provider,
                top_providers=[
                    TopProviderDTO(name=p["name"], chats=p["chats"], rank=p["rank"])
                    for p in entity.summary.top_providers
                ],
            ),
            model_breakdown={
                k: ModelBreakdownDTO(
                    messages=v["messages"],
                    input_tokens=v["input_tokens"],
                    output_tokens=v["output_tokens"],
                    cost=v["cost"],
                )
                for k, v in entity.model_breakdown.items()
            },
            provider_breakdown={
                k: ProviderBreakdownDTO(
                    messages=v["messages"],
                    chats=v["chats"],
                    input_tokens=v["input_tokens"],
                    output_tokens=v["output_tokens"],
                    cost=v["cost"],
                    avg_messages_per_chat=v["avg_messages_per_chat"],
                )
                for k, v in entity.provider_breakdown.items()
            },
            chat_statistics=ChatStatisticsDTO(
                total_chats=entity.chat_statistics.total_chats,
                avg_messages_per_chat=entity.chat_statistics.avg_messages_per_chat,
                longest_chat=entity.chat_statistics.longest_chat,
                chat_distribution_by_provider=entity.chat_statistics.chat_distribution_by_provider,
                recent_chats=entity.chat_statistics.recent_chats,
            ),
        )

    @staticmethod
    def to_usage_timeline_dto(entity: UsageTimeline) -> UsageTimelineDTO:
        return UsageTimelineDTO(
            granularity=entity.granularity,
            period=UsagePeriodDTO(
                days=entity.period.days, start_date=entity.period.start_date, end_date=entity.period.end_date
            ),
            timeline=[
                TimelineDataPointDTO(
                    timestamp=point.timestamp,
                    messages=point.messages,
                    chats=point.chats,
                    input_tokens=point.input_tokens,
                    output_tokens=point.output_tokens,
                    total_tokens=point.total_tokens,
                    cost_usd=point.cost_usd,
                    energy_wh=point.energy_wh,
                )
                for point in entity.timeline
            ],
        )

    @staticmethod
    def to_usage_patterns_dto(entity: UsagePatterns) -> UsagePatternsDTO:
        return UsagePatternsDTO(
            period=UsagePeriodDTO(
                days=entity.period.days, start_date=entity.period.start_date, end_date=entity.period.end_date
            ),
            hourly_distribution=entity.hourly_distribution,
            daily_distribution=entity.daily_distribution,
            peak_hour=entity.peak_hour,
            peak_day=entity.peak_day,
        )
