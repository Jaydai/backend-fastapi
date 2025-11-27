"""
Audit Analytics Service - New analytics endpoints for enhanced dashboard
Provides model distribution, quality analytics, usage patterns, and risk categories
"""

import logging
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from dtos.audit_dto import (
    ModelDistributionItemDTO,
    ModelDistributionResponseDTO,
    ProviderDistributionDTO,
    ProviderDistributionResponseDTO,
    QualityDistributionBinDTO,
    QualityDistributionResponseDTO,
    QualityMetricsTimelineDataPointDTO,
    QualityMetricsTimelineResponseDTO,
    RiskCategoriesResponseDTO,
    RiskCategoryItemDTO,
    UsageByHourDataPointDTO,
    UsageByHourResponseDTO,
)
from supabase import Client

logger = logging.getLogger(__name__)


def _calculate_date_range(start_date: str | None, end_date: str | None, days: int):
    """Calculate start and end datetime from parameters"""
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
    else:
        end_dt = datetime.now()

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
    else:
        start_dt = end_dt - timedelta(days=days)

    return start_dt, end_dt


def _get_user_ids_for_teams(client: Client, organization_id: str, team_ids: list[str] | None) -> list[str]:
    """Get user IDs filtered by teams, or all organization members if no teams specified"""
    if not team_ids or len(team_ids) == 0:
        response = (
            client.table("user_organization_roles").select("user_id").eq("organization_id", organization_id).execute()
        )
        return [row["user_id"] for row in response.data] if response.data else []

    # Get users in specified teams
    from repositories.team_repository import TeamRepository

    user_ids_set = set()
    for team_id in team_ids:
        members = TeamRepository.get_team_members(client, team_id)
        user_ids_set.update([m.user_id for m in members])

    return list(user_ids_set)


class AuditAnalyticsService:
    """Service for new audit analytics endpoints"""

    @staticmethod
    async def get_model_distribution(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
    ) -> ModelDistributionResponseDTO:
        """Get distribution of AI models being used"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return ModelDistributionResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                models=[],
                total_messages=0,
                generated_at=datetime.now(),
            )

        # Fetch messages with model information
        response = (
            client.table("messages")
            .select("model")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .execute()
        )

        # Count models
        model_counts = Counter()
        for row in response.data or []:
            model = row.get("model") or "Unknown"
            model_counts[model] += 1

        total = sum(model_counts.values())

        # Build response
        models = [
            ModelDistributionItemDTO(
                model_name=model, count=count, percentage=(count / total * 100) if total > 0 else 0.0
            )
            for model, count in model_counts.most_common()
        ]

        return ModelDistributionResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            models=models,
            total_messages=total,
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_provider_distribution(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
    ) -> ProviderDistributionResponseDTO:
        """Get distribution of chat providers being used"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return ProviderDistributionResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                providers=[],
                total_chats=0,
                generated_at=datetime.now(),
            )

        # Fetch chats with provider information
        chats_result = (
            client.table("chats")
            .select("chat_provider_id, provider_name")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .execute()
        )

        # Fetch messages to count messages per provider
        messages_result = (
            client.table("messages")
            .select("id, chat_provider_id")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .execute()
        )

        # Calculate provider distribution
        provider_counts = defaultdict(lambda: {"chats": 0, "messages": 0})
        chat_provider_to_name = {}

        # Count chats and build mapping
        for row in chats_result.data or []:
            provider_name = row.get("provider_name") or "Unknown"
            chat_provider_id = row.get("chat_provider_id")
            provider_counts[provider_name]["chats"] += 1
            if chat_provider_id:
                chat_provider_to_name[chat_provider_id] = provider_name

        # Count messages per provider
        for row in messages_result.data or []:
            chat_provider_id = row.get("chat_provider_id")
            if chat_provider_id and chat_provider_id in chat_provider_to_name:
                provider = chat_provider_to_name[chat_provider_id]
                provider_counts[provider]["messages"] += 1

        # Calculate total chats for percentage
        total_chats = sum(p["chats"] for p in provider_counts.values())

        # Build provider distribution list
        providers = [
            ProviderDistributionDTO(
                provider_name=provider,
                chat_count=counts["chats"],
                message_count=counts["messages"],
                percentage=(counts["chats"] / total_chats * 100) if total_chats > 0 else 0.0,
            )
            for provider, counts in sorted(provider_counts.items(), key=lambda x: x[1]["chats"], reverse=True)
        ]

        return ProviderDistributionResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            providers=providers,
            total_chats=total_chats,
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_quality_timeline(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
        granularity: str,
    ) -> QualityMetricsTimelineResponseDTO:
        """Get quality score trends over time with all dimensions"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return QualityMetricsTimelineResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                granularity=granularity,
                team_filter=team_ids,
                timeline=[],
                averages={},
                generated_at=datetime.now(),
            )

        # Fetch quality data
        response = (
            client.table("enriched_chats")
            .select("created_at, quality_score, clarity_score, context_score, specificity_score, actionability_score")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .execute()
        )

        # Group by date
        date_data = defaultdict(
            lambda: {
                "quality_scores": [],
                "clarity_scores": [],
                "context_scores": [],
                "specificity_scores": [],
                "actionability_scores": [],
            }
        )

        all_scores = defaultdict(list)

        for row in response.data or []:
            date = row["created_at"].split("T")[0]

            if row.get("quality_score") is not None:
                date_data[date]["quality_scores"].append(row["quality_score"])
                all_scores["quality_score"].append(row["quality_score"])

            if row.get("clarity_score") is not None:
                date_data[date]["clarity_scores"].append(row["clarity_score"])
                all_scores["clarity_score"].append(row["clarity_score"])

            if row.get("context_score") is not None:
                date_data[date]["context_scores"].append(row["context_score"])
                all_scores["context_score"].append(row["context_score"])

            if row.get("specificity_score") is not None:
                date_data[date]["specificity_scores"].append(row["specificity_score"])
                all_scores["specificity_score"].append(row["specificity_score"])

            if row.get("actionability_score") is not None:
                date_data[date]["actionability_scores"].append(row["actionability_score"])
                all_scores["actionability_score"].append(row["actionability_score"])

        # Build timeline
        timeline = []
        for date in sorted(date_data.keys()):
            data = date_data[date]
            timeline.append(
                QualityMetricsTimelineDataPointDTO(
                    date=date,
                    quality_score=sum(data["quality_scores"]) / len(data["quality_scores"])
                    if data["quality_scores"]
                    else None,
                    clarity_score=sum(data["clarity_scores"]) / len(data["clarity_scores"])
                    if data["clarity_scores"]
                    else None,
                    context_score=sum(data["context_scores"]) / len(data["context_scores"])
                    if data["context_scores"]
                    else None,
                    specificity_score=sum(data["specificity_scores"]) / len(data["specificity_scores"])
                    if data["specificity_scores"]
                    else None,
                    actionability_score=sum(data["actionability_scores"]) / len(data["actionability_scores"])
                    if data["actionability_scores"]
                    else None,
                    count=len(data["quality_scores"]),
                )
            )

        # Calculate averages
        averages = {}
        for key, scores in all_scores.items():
            if scores:
                averages[key] = sum(scores) / len(scores)

        return QualityMetricsTimelineResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            granularity=granularity,
            team_filter=team_ids,
            timeline=timeline,
            averages=averages,
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_quality_distribution(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
    ) -> QualityDistributionResponseDTO:
        """Get distribution of quality scores in bins"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return QualityDistributionResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                bins=[],
                total_rated=0,
                average_score=0.0,
                generated_at=datetime.now(),
            )

        # Fetch quality scores
        response = (
            client.table("enriched_chats")
            .select("quality_score")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .not_.is_("quality_score", "null")
            .execute()
        )

        # Bin the scores
        bins_data = {"0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}

        scores = []
        for row in response.data or []:
            score = row.get("quality_score")
            if score is not None:
                scores.append(score)
                if score <= 20:
                    bins_data["0-20"] += 1
                elif score <= 40:
                    bins_data["21-40"] += 1
                elif score <= 60:
                    bins_data["41-60"] += 1
                elif score <= 80:
                    bins_data["61-80"] += 1
                else:
                    bins_data["81-100"] += 1

        total = len(scores)
        average = sum(scores) / total if total > 0 else 0.0

        # Build bins list
        bins = [
            QualityDistributionBinDTO(
                range=bin_range, count=count, percentage=(count / total * 100) if total > 0 else 0.0
            )
            for bin_range, count in bins_data.items()
        ]

        return QualityDistributionResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            bins=bins,
            total_rated=total,
            average_score=average,
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_usage_by_hour(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
    ) -> UsageByHourResponseDTO:
        """Get usage patterns by hour of day"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return UsageByHourResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                hourly_data=[],
                peak_hour=0,
                total_messages=0,
                generated_at=datetime.now(),
            )

        # Fetch messages
        response = (
            client.table("messages")
            .select("created_at")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .execute()
        )

        # Count by hour and weekday/weekend
        hour_counts = defaultdict(lambda: {"weekday": 0, "weekend": 0})

        for row in response.data or []:
            dt = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
            hour = dt.hour
            is_weekend = dt.weekday() >= 5  # Saturday = 5, Sunday = 6

            if is_weekend:
                hour_counts[hour]["weekend"] += 1
            else:
                hour_counts[hour]["weekday"] += 1

        # Build hourly data
        hourly_data = []
        total_messages = 0
        max_count = 0
        peak_hour = 0

        for hour in range(24):
            weekday = hour_counts[hour]["weekday"]
            weekend = hour_counts[hour]["weekend"]
            total = weekday + weekend
            total_messages += total

            if total > max_count:
                max_count = total
                peak_hour = hour

            hourly_data.append(
                UsageByHourDataPointDTO(hour=hour, weekday_count=weekday, weekend_count=weekend, total_count=total)
            )

        return UsageByHourResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            hourly_data=hourly_data,
            peak_hour=peak_hour,
            total_messages=total_messages,
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_risk_categories(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: list[str] | None,
    ) -> RiskCategoriesResponseDTO:
        """Get breakdown of risk categories"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return RiskCategoriesResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                categories=[],
                total_risky_messages=0,
                generated_at=datetime.now(),
            )

        # Fetch risk data
        response = (
            client.table("enriched_messages")
            .select("risk_categories, overall_risk_level")
            .in_("user_id", user_ids)
            .gte("created_at", start_dt.isoformat())
            .lte("created_at", end_dt.isoformat())
            .neq("overall_risk_level", "none")
            .execute()
        )

        # Parse risk categories
        category_counts = defaultdict(int)
        category_severity = defaultdict(lambda: defaultdict(int))

        for row in response.data or []:
            risk_categories = row.get("risk_categories", {})
            risk_level = row.get("overall_risk_level", "none")

            if isinstance(risk_categories, dict):
                for category, details in risk_categories.items():
                    if isinstance(details, dict) and details.get("detected"):
                        category_counts[category] += 1
                        category_severity[category][risk_level] += 1

        total = sum(category_counts.values())

        # Build categories list
        categories = []
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            categories.append(
                RiskCategoryItemDTO(
                    category=category,
                    count=count,
                    percentage=(count / total * 100) if total > 0 else 0.0,
                    severity_breakdown=dict(category_severity[category]),
                )
            )

        return RiskCategoriesResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            categories=categories,
            total_risky_messages=len(response.data or []),
            generated_at=datetime.now(),
        )
