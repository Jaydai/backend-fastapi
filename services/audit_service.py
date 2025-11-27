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
