"""
Audit Service - Business logic for organization audits (REFACTORED with utilities)
Orchestrates parallel data fetching and aggregation
"""
import logging
from supabase import Client
from datetime import datetime, timedelta
from typing import Optional

from repositories.audit_repository import AuditRepository
from dtos.audit_dto import OrganizationAuditResponseDTO
from utils.enrichment import (
    aggregate_quality_stats,
    aggregate_risk_stats,
    aggregate_usage_stats,
    aggregate_theme_stats,
    aggregate_intent_stats,
    aggregate_top_users,
    aggregate_top_prompts,
    aggregate_risky_prompts,
    quality_stats_to_dto,
    risk_stats_to_dto,
    usage_stats_to_dto,
    theme_stats_to_dto,
    intent_stats_to_dto,
    top_user_to_dto,
    top_prompt_to_dto,
    risky_prompt_to_dto
)

logger = logging.getLogger(__name__)


class AuditService:
    """Business logic for organization audit operations"""

    @staticmethod
    async def get_organization_audit(
        client: Client,
        user_id: str,
        organization_id: str,
        start_date: Optional[str],
        end_date: Optional[str],
        days: int
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
        audit_data = await AuditRepository.fetch_all_audit_data_parallel(
            client, user_ids, start_dt, end_dt
        )

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
            date_range={
                "start_date": start_dt.isoformat(),
                "end_date": end_dt.isoformat()
            },
            quality_stats=quality_stats_to_dto(quality_stats),
            risk_stats=risk_stats_to_dto(risk_stats),
            usage_stats=usage_stats_to_dto(usage_stats),
            theme_stats=theme_stats_to_dto(theme_stats),
            intent_stats=intent_stats_to_dto(intent_stats),
            top_users=[top_user_to_dto(u) for u in top_users],
            top_prompts=[top_prompt_to_dto(p) for p in top_prompts],
            riskiest_prompts=[risky_prompt_to_dto(p) for p in risky_prompts],
            generated_at=datetime.now()
        )


# ==================== PRIVATE HELPER FUNCTIONS ====================

def _calculate_date_range(
    start_date: Optional[str],
    end_date: Optional[str],
    days: int
) -> tuple[datetime, datetime]:
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
    organization_id: str,
    start_dt: datetime,
    end_dt: datetime
) -> OrganizationAuditResponseDTO:
    """Return empty audit response when no data available"""
    from dtos.audit_dto import (
        QualityStatsDTO, RiskStatsDTO, UsageStatsDTO,
        ThemeStatsDTO, IntentStatsDTO
    )

    return OrganizationAuditResponseDTO(
        organization_id=organization_id,
        organization_name="Organization",
        date_range={
            "start_date": start_dt.isoformat(),
            "end_date": end_dt.isoformat()
        },
        quality_stats=QualityStatsDTO(
            average_score=0.0,
            distribution={"excellent": 0, "good": 0, "medium": 0, "poor": 0},
            total_rated=0
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
            risk_distribution={}
        ),
        usage_stats=UsageStatsDTO(
            total_prompts=0,
            total_chats=0,
            active_users=0,
            work_related_count=0,
            personal_count=0,
            work_percentage=0.0,
            average_prompts_per_user=0.0,
            average_quality_score=0.0
        ),
        theme_stats=ThemeStatsDTO(top_themes=[], total_categorized=0),
        intent_stats=IntentStatsDTO(top_intents=[], total_categorized=0),
        top_users=[],
        top_prompts=[],
        riskiest_prompts=[],
        generated_at=datetime.now()
    )
