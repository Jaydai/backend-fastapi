"""
Audit Service - Business logic for organization audits (REFACTORED with utilities)
Orchestrates parallel data fetching and aggregation
"""

import logging
from datetime import datetime, timedelta

from supabase import Client

from dtos.audit_dto import (
    IntentStatsWithContextDTO,
    OrganizationAuditResponseDTO,
    QualityStatsWithContextDTO,
    RiskStatsWithContextDTO,
    RiskyPromptsWithContextDTO,
    ThemeStatsWithContextDTO,
    TopPromptsWithContextDTO,
    TopUsersWithContextDTO,
    UsageStatsWithContextDTO,
    UserProfileResponseDTO,
    UserProfileDataDTO,
    UserProfileKPIsDTO,
    UserProfileComparisonDTO,
    UserActivityPointDTO,
    UserProviderUsageDTO,
    UserThemeDataDTO,
    UserIntentDataDTO,
)
from repositories.audit_repository import AuditRepository
from utils.enrichment import (
    aggregate_intent_stats,
    aggregate_quality_stats,
    aggregate_risk_stats,
    aggregate_risky_prompts,
    aggregate_theme_stats,
    aggregate_top_prompts,
    aggregate_top_users,
    aggregate_usage_stats,
    intent_stats_to_dto,
    quality_stats_to_dto,
    risk_stats_to_dto,
    risky_prompt_to_dto,
    theme_stats_to_dto,
    top_prompt_to_dto,
    top_user_to_dto,
    usage_stats_to_dto,
)

logger = logging.getLogger(__name__)


class AuditService:
    """Business logic for organization audit operations"""

    @staticmethod
    async def get_organization_audit(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> OrganizationAuditResponseDTO:
        """
        Get comprehensive organization audit with parallel data fetching
        """
        # Calculate date range
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)

        # Get organization member IDs
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            logger.warning(f"No members found for organization {organization_id}")
            return _create_empty_audit_response(organization_id, start_dt, end_dt)

        # Fetch all data in parallel
        audit_data = await AuditRepository.fetch_all_audit_data_parallel(client, user_ids, start_dt, end_dt)

        # Aggregate data using utility functions
        quality_stats = aggregate_quality_stats(audit_data["quality"])
        risk_stats = aggregate_risk_stats(audit_data["risk"])
        usage_stats = aggregate_usage_stats(audit_data["usage"])
        theme_stats = aggregate_theme_stats(audit_data["themes"])
        intent_stats = aggregate_intent_stats(audit_data["intents"])
        top_users = aggregate_top_users(audit_data["top_users"])
        top_prompts = aggregate_top_prompts(audit_data["top_prompts"])
        risky_prompts = aggregate_risky_prompts(audit_data["risky_prompts"])

        # Build response DTO using utility mappers
        return OrganizationAuditResponseDTO(
            organization_id=organization_id,
            organization_name="Organization",  # TODO: Fetch org name
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            quality_stats=quality_stats_to_dto(quality_stats),
            risk_stats=risk_stats_to_dto(risk_stats),
            usage_stats=usage_stats_to_dto(usage_stats),
            theme_stats=theme_stats_to_dto(theme_stats),
            intent_stats=intent_stats_to_dto(intent_stats),
            top_users=[top_user_to_dto(u) for u in top_users],
            top_prompts=[top_prompt_to_dto(p) for p in top_prompts],
            riskiest_prompts=[risky_prompt_to_dto(p) for p in risky_prompts],
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_quality_stats(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> QualityStatsWithContextDTO:
        """Get quality statistics for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            from dtos.audit_dto import QualityStatsDTO

            empty_stats = QualityStatsDTO(
                average_score=0.0,
                distribution={"excellent": 0, "good": 0, "medium": 0, "poor": 0},
                total_rated=0,
                daily_average=0.0,
            )
            return QualityStatsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=empty_stats,
                generated_at=datetime.now(),
            )

        quality_data = await AuditRepository.get_quality_stats_async(client, user_ids, start_dt, end_dt)
        quality_stats = aggregate_quality_stats(quality_data)

        return QualityStatsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=quality_stats_to_dto(quality_stats),
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_risk_stats(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> RiskStatsWithContextDTO:
        """Get risk statistics for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            from dtos.audit_dto import RiskStatsDTO

            empty_stats = RiskStatsDTO(
                total_messages_assessed=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                none_count=0,
                pii_detected_count=0,
                credentials_detected_count=0,
                sensitive_data_count=0,
                average_risk_score=0.0,
                risk_distribution={},
            )
            return RiskStatsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=empty_stats,
                generated_at=datetime.now(),
            )

        risk_data = await AuditRepository.get_risk_stats_async(client, user_ids, start_dt, end_dt)
        risk_stats = aggregate_risk_stats(risk_data)

        return RiskStatsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=risk_stats_to_dto(risk_stats),
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_usage_stats(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> UsageStatsWithContextDTO:
        """Get usage statistics for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            from dtos.audit_dto import UsageStatsDTO

            empty_stats = UsageStatsDTO(
                total_prompts=0,
                total_chats=0,
                active_users=0,
                work_related_count=0,
                personal_count=0,
                work_percentage=0.0,
                average_prompts_per_user=0.0,
                average_quality_score=0.0,
                daily_average=0.0,
            )
            return UsageStatsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=empty_stats,
                generated_at=datetime.now(),
            )

        usage_data = await AuditRepository.get_usage_stats_async(client, user_ids, start_dt, end_dt)
        usage_stats = aggregate_usage_stats(usage_data)

        return UsageStatsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=usage_stats_to_dto(usage_stats),
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_theme_stats(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> ThemeStatsWithContextDTO:
        """Get theme statistics for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            from dtos.audit_dto import ThemeStatsDTO

            empty_stats = ThemeStatsDTO(top_themes=[], total_categorized=0)
            return ThemeStatsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=empty_stats,
                generated_at=datetime.now(),
            )

        theme_data = await AuditRepository.get_theme_stats_async(client, user_ids, start_dt, end_dt)
        theme_stats = aggregate_theme_stats(theme_data)

        return ThemeStatsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=theme_stats_to_dto(theme_stats),
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_intent_stats(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> IntentStatsWithContextDTO:
        """Get intent statistics for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            from dtos.audit_dto import IntentStatsDTO

            empty_stats = IntentStatsDTO(top_intents=[], total_categorized=0)
            return IntentStatsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=empty_stats,
                generated_at=datetime.now(),
            )

        intent_data = await AuditRepository.get_intent_stats_async(client, user_ids, start_dt, end_dt)
        intent_stats = aggregate_intent_stats(intent_data)

        return IntentStatsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=intent_stats_to_dto(intent_stats),
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_top_users(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> TopUsersWithContextDTO:
        """Get top users for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            return TopUsersWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=[],
                generated_at=datetime.now(),
            )

        top_users_data = await AuditRepository.get_top_users_async(client, user_ids, start_dt, end_dt)
        top_users = aggregate_top_users(top_users_data)

        return TopUsersWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=[top_user_to_dto(u) for u in top_users],
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_top_prompts(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> TopPromptsWithContextDTO:
        """Get top prompts for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            return TopPromptsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=[],
                generated_at=datetime.now(),
            )

        top_prompts_data = await AuditRepository.get_top_prompts_async(client, user_ids, start_dt, end_dt)
        top_prompts = aggregate_top_prompts(top_prompts_data)

        return TopPromptsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=[top_prompt_to_dto(p) for p in top_prompts],
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_organization_risky_prompts(
        client: Client, user_id: str, organization_id: str, start_date: str | None, end_date: str | None, days: int
    ) -> RiskyPromptsWithContextDTO:
        """Get risky prompts for organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not user_ids:
            return RiskyPromptsWithContextDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                data=[],
                generated_at=datetime.now(),
            )

        risky_prompts_data = await AuditRepository.get_riskiest_prompts_async(
            client, user_ids, start_dt, end_dt, limit=100
        )
        risky_prompts = aggregate_risky_prompts(risky_prompts_data)

        return RiskyPromptsWithContextDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=[risky_prompt_to_dto(p) for p in risky_prompts],
            generated_at=datetime.now(),
        )

    @staticmethod
    async def get_user_profile(
        client: Client,
        requesting_user_id: str,
        organization_id: str,
        target_user_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
    ) -> UserProfileResponseDTO:
        """Get comprehensive profile for a specific user in the organization"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        org_user_ids = AuditRepository.get_organization_member_ids(client, organization_id)

        if not org_user_ids:
            raise ValueError("No members found for organization")

        # Verify target user is in the organization
        if target_user_id not in org_user_ids:
            raise ValueError("User not found in organization")

        # Fetch all user profile data
        profile_data = await AuditRepository.get_user_profile_data_async(
            client, target_user_id, org_user_ids, start_dt, end_dt
        )

        # Process the data
        user_info = profile_data["user_info"]
        user_messages = profile_data["user_messages"]
        user_quality = profile_data["user_quality"]
        user_risks = profile_data["user_risks"]
        trend_quality = profile_data["trend_quality"]
        org_messages = profile_data["org_messages"]
        org_quality = profile_data["org_quality"]

        # Calculate KPIs
        total_prompts = len(user_messages)
        quality_scores = [q["quality_score"] for q in user_quality if q.get("quality_score") is not None]
        average_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0

        work_related = sum(1 for q in user_quality if q.get("is_work_related"))
        work_percentage = (work_related / len(user_quality) * 100) if user_quality else 0.0

        high_risk_count = len(user_risks)

        # Calculate quality trend
        trend_scores = [q["quality_score"] for q in trend_quality if q.get("quality_score") is not None]
        trend_avg = sum(trend_scores) / len(trend_scores) if trend_scores else None
        quality_trend = None
        if trend_avg is not None and trend_avg > 0:
            quality_trend = ((average_quality - trend_avg) / trend_avg) * 100

        # Calculate percentile ranking among org users
        user_prompt_counts = {}
        for msg in org_messages:
            uid = msg["user_id"]
            user_prompt_counts[uid] = user_prompt_counts.get(uid, 0) + 1

        sorted_counts = sorted(user_prompt_counts.values())
        user_count = user_prompt_counts.get(target_user_id, 0)
        if sorted_counts:
            rank = sum(1 for c in sorted_counts if c <= user_count)
            percentile_ranking = (rank / len(sorted_counts)) * 100
        else:
            percentile_ranking = 0.0

        # Calculate org averages for comparison
        org_total_prompts = len(org_messages)
        org_active_users = len(set(msg["user_id"] for msg in org_messages))
        org_avg_prompts = org_total_prompts / org_active_users if org_active_users > 0 else 0

        org_quality_scores = [q["quality_score"] for q in org_quality if q.get("quality_score") is not None]
        org_avg_quality = sum(org_quality_scores) / len(org_quality_scores) if org_quality_scores else 0.0

        org_work_related = sum(1 for q in org_quality if q.get("is_work_related"))
        org_work_percentage = (org_work_related / len(org_quality) * 100) if org_quality else 0.0

        # Calculate user vs org differences
        user_quality_vs_org = ((average_quality - org_avg_quality) / org_avg_quality * 100) if org_avg_quality > 0 else 0
        user_prompts_vs_org = ((total_prompts - org_avg_prompts) / org_avg_prompts * 100) if org_avg_prompts > 0 else 0

        # Build activity timeline (group by date)
        activity_by_date: dict[str, dict] = {}
        for msg in user_messages:
            date_str = msg["created_at"][:10]  # YYYY-MM-DD
            if date_str not in activity_by_date:
                activity_by_date[date_str] = {"count": 0, "chat_ids": set()}
            activity_by_date[date_str]["count"] += 1
            if msg.get("chat_provider_id"):
                activity_by_date[date_str]["chat_ids"].add(msg["chat_provider_id"])

        # Get quality scores per date
        chat_to_quality = {q["chat_provider_id"]: q.get("quality_score", 0) for q in user_quality}
        activity_timeline = []
        for date_str in sorted(activity_by_date.keys()):
            data = activity_by_date[date_str]
            chat_qualities = [chat_to_quality.get(cid, 0) for cid in data["chat_ids"] if cid in chat_to_quality]
            avg_q = sum(chat_qualities) / len(chat_qualities) if chat_qualities else 0.0
            activity_timeline.append(
                UserActivityPointDTO(date=date_str, prompt_count=data["count"], average_quality=round(avg_q, 2))
            )

        # Build provider breakdown
        provider_counts: dict[str, int] = {}
        for q in user_quality:
            provider = q.get("provider") or "Unknown"
            provider_counts[provider] = provider_counts.get(provider, 0) + 1

        total_provider_chats = sum(provider_counts.values())
        provider_breakdown = [
            UserProviderUsageDTO(
                provider_name=provider,
                chat_count=count,
                percentage=round(count / total_provider_chats * 100, 1) if total_provider_chats > 0 else 0,
            )
            for provider, count in sorted(provider_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        # Build theme distribution
        theme_counts: dict[str, int] = {}
        for q in user_quality:
            theme = q.get("theme")
            if theme:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1

        total_themes = sum(theme_counts.values())
        themes = [
            UserThemeDataDTO(
                theme=theme,
                count=count,
                percentage=round(count / total_themes * 100, 1) if total_themes > 0 else 0,
            )
            for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        # Build intent distribution with quality
        intent_data: dict[str, dict] = {}
        for q in user_quality:
            intent = q.get("intent")
            if intent:
                if intent not in intent_data:
                    intent_data[intent] = {"count": 0, "quality_sum": 0, "quality_count": 0}
                intent_data[intent]["count"] += 1
                if q.get("quality_score") is not None:
                    intent_data[intent]["quality_sum"] += q["quality_score"]
                    intent_data[intent]["quality_count"] += 1

        total_intents = sum(d["count"] for d in intent_data.values())
        intents = [
            UserIntentDataDTO(
                intent=intent,
                count=data["count"],
                percentage=round(data["count"] / total_intents * 100, 1) if total_intents > 0 else 0,
                avg_quality=round(data["quality_sum"] / data["quality_count"], 2) if data["quality_count"] > 0 else 0,
            )
            for intent, data in sorted(intent_data.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
        ]

        # Build response
        return UserProfileResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            data=UserProfileDataDTO(
                user_id=target_user_id,
                email=user_info.get("email", ""),
                name=user_info.get("name"),
                kpis=UserProfileKPIsDTO(
                    total_prompts=total_prompts,
                    average_quality=round(average_quality, 2),
                    work_percentage=round(work_percentage, 1),
                    high_risk_count=high_risk_count,
                    quality_trend=round(quality_trend, 1) if quality_trend is not None else None,
                    percentile_ranking=round(percentile_ranking, 1),
                ),
                comparison=UserProfileComparisonDTO(
                    org_average_quality=round(org_avg_quality, 2),
                    org_average_prompts=round(org_avg_prompts, 1),
                    org_average_work_percentage=round(org_work_percentage, 1),
                    user_quality_vs_org=round(user_quality_vs_org, 1),
                    user_prompts_vs_org=round(user_prompts_vs_org, 1),
                ),
                activity_timeline=activity_timeline,
                provider_breakdown=provider_breakdown,
                themes=themes,
                intents=intents,
            ),
            generated_at=datetime.now(),
        )


# ==================== PRIVATE HELPER FUNCTIONS ====================


def _calculate_date_range(start_date: str | None, end_date: str | None, days: int) -> tuple[datetime, datetime]:
    """Calculate date range for audit"""
    if not end_date:
        end_dt = datetime.now()
    else:
        end_dt = datetime.fromisoformat(end_date)

    if not start_date:
        start_dt = end_dt - timedelta(days=days)
    else:
        start_dt = datetime.fromisoformat(start_date)

    return start_dt, end_dt


def _create_empty_audit_response(
    organization_id: str, start_dt: datetime, end_dt: datetime
) -> OrganizationAuditResponseDTO:
    """Return empty audit response when no data available"""
    from dtos.audit_dto import IntentStatsDTO, QualityStatsDTO, RiskStatsDTO, ThemeStatsDTO, UsageStatsDTO

    return OrganizationAuditResponseDTO(
        organization_id=organization_id,
        organization_name="Organization",
        date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
        quality_stats=QualityStatsDTO(
            average_score=0.0, distribution={"excellent": 0, "good": 0, "medium": 0, "poor": 0}, total_rated=0
        ),
        risk_stats=RiskStatsDTO(
            total_messages_assessed=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            none_count=0,
            pii_detected_count=0,
            credentials_detected_count=0,
            sensitive_data_count=0,
            average_risk_score=0.0,
            risk_distribution={},
        ),
        usage_stats=UsageStatsDTO(
            total_prompts=0,
            total_chats=0,
            active_users=0,
            work_related_count=0,
            personal_count=0,
            work_percentage=0.0,
            average_prompts_per_user=0.0,
            average_quality_score=0.0,
        ),
        theme_stats=ThemeStatsDTO(top_themes=[], total_categorized=0),
        intent_stats=IntentStatsDTO(top_intents=[], total_categorized=0),
        top_users=[],
        top_prompts=[],
        riskiest_prompts=[],
        generated_at=datetime.now(),
    )
