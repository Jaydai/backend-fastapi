"""Enhanced audit analytics endpoints"""

import logging

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import (
    ModelDistributionResponseDTO,
    ProviderDistributionResponseDTO,
    QualityDistributionResponseDTO,
    QualityMetricsTimelineResponseDTO,
    RiskCategoriesResponseDTO,
    UsageByHourResponseDTO,
)
from services.audit_analytics_service import AuditAnalyticsService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/model-distribution", response_model=ModelDistributionResponseDTO)
async def get_model_distribution(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get distribution of AI models being used across the organization

    Shows which models (GPT-4, Claude-3, Gemini, etc.) are being used
    and their relative proportions.
    """
    try:
        result = await AuditAnalyticsService.get_model_distribution(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model distribution: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get model distribution: {str(e)}")


@router.get("/organizations/{organization_id}/provider-distribution", response_model=ProviderDistributionResponseDTO)
async def get_provider_distribution(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get distribution of chat providers being used across the organization

    Shows which providers (ChatGPT, Claude, Gemini, etc.) are being used
    and their relative proportions by number of chats and messages.
    """
    try:
        result = await AuditAnalyticsService.get_provider_distribution(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting provider distribution: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get provider distribution: {str(e)}")


@router.get(
    "/organizations/{organization_id}/quality-metrics-timeline", response_model=QualityMetricsTimelineResponseDTO
)
async def get_quality_timeline(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
    granularity: str = Query(default="day", pattern="^(day|week|month)$", description="Time granularity"),
):
    """
    Get quality score trends over time with all dimensions

    Tracks quality_score, clarity_score, context_score, specificity_score,
    and actionability_score over time to show improvement trends.
    """
    try:
        result = await AuditAnalyticsService.get_quality_timeline(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids, granularity
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality timeline: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get quality timeline: {str(e)}")


@router.get("/organizations/{organization_id}/quality-distribution", response_model=QualityDistributionResponseDTO)
async def get_quality_distribution(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get distribution of quality scores in bins (histogram)

    Shows how many prompts fall into each quality range:
    0-20, 21-40, 41-60, 61-80, 81-100
    """
    try:
        result = await AuditAnalyticsService.get_quality_distribution(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quality distribution: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get quality distribution: {str(e)}")


@router.get("/organizations/{organization_id}/usage-by-hour", response_model=UsageByHourResponseDTO)
async def get_usage_by_hour(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get usage patterns by hour of day

    Shows which hours of the day have the most AI usage,
    split by weekday vs weekend patterns.
    """
    try:
        result = await AuditAnalyticsService.get_usage_by_hour(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting usage by hour: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get usage by hour: {str(e)}")


@router.get("/organizations/{organization_id}/risk-categories", response_model=RiskCategoriesResponseDTO)
async def get_risk_categories(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get breakdown of risk categories

    Shows which types of risks are most common (PII, credentials, security, etc.)
    with severity breakdown for each category.
    """
    try:
        result = await AuditAnalyticsService.get_risk_categories(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk categories: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get risk categories: {str(e)}")
