"""
DTOs for audit endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Request DTOs

class OrganizationAuditRequestDTO(BaseModel):
    """Request parameters for organization audit"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")


# Response DTOs

class QualityStatsDTO(BaseModel):
    """Quality statistics response"""
    average_score: float
    median_score: Optional[float] = None
    distribution: dict[str, int]  # excellent, good, medium, poor
    total_rated: int
    trend_change: Optional[float] = None
    trend_7days: Optional[float] = None  # 7-day trend percentage change


class RiskStatsDTO(BaseModel):
    """Risk statistics response"""
    total_messages_assessed: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    none_count: int
    pii_detected_count: int
    credentials_detected_count: int
    sensitive_data_count: int
    average_risk_score: float
    risk_distribution: dict[str, int]
    trend_7days: Optional[float] = None  # 7-day trend percentage change in average risk


class UsageStatsDTO(BaseModel):
    """Usage statistics response"""
    total_prompts: int
    total_chats: int
    active_users: int
    work_related_count: int
    personal_count: int
    work_percentage: float
    average_prompts_per_user: float
    average_quality_score: float
    daily_average: Optional[float] = None  # Average prompts per day over the period
    trend_7days: Optional[float] = None  # 7-day trend percentage change in daily prompts


class ThemeStatsDTO(BaseModel):
    """Theme distribution response"""
    top_themes: list[dict]  # [{"theme": str, "count": int, "percentage": float}]
    total_categorized: int
    trend_change: Optional[dict[str, float]] = None


class IntentStatsDTO(BaseModel):
    """Intent distribution response"""
    top_intents: list[dict]  # [{"intent": str, "count": int, "percentage": float, "avg_quality": float}]
    total_categorized: int


class TopUserDTO(BaseModel):
    """Top user response"""
    user_id: str
    email: str
    name: Optional[str] = None
    total_prompts: int
    average_quality: float
    work_prompts: int
    high_risk_messages: int


class TopPromptDTO(BaseModel):
    """Top quality prompt response"""
    chat_provider_id: str
    message_provider_id: Optional[str] = None
    quality_score: int
    theme: str
    intent: str
    content_preview: str
    created_at: datetime


class RiskyPromptDTO(BaseModel):
    """Risky prompt response"""
    message_provider_id: str
    risk_level: str
    risk_score: float
    risk_categories: list[str]
    content_preview: str
    created_at: datetime
    user_whitelist: bool = False


class OrganizationAuditResponseDTO(BaseModel):
    """Complete organization audit response"""
    organization_id: str
    organization_name: str
    date_range: dict[str, str]
    quality_stats: QualityStatsDTO
    risk_stats: RiskStatsDTO
    usage_stats: UsageStatsDTO
    theme_stats: ThemeStatsDTO
    intent_stats: IntentStatsDTO
    top_users: list[TopUserDTO]
    top_prompts: list[TopPromptDTO]
    riskiest_prompts: list[RiskyPromptDTO]
    generated_at: datetime


# Individual endpoint response DTOs with context

class QualityStatsWithContextDTO(BaseModel):
    """Quality statistics with context"""
    organization_id: str
    date_range: dict[str, str]
    data: QualityStatsDTO
    generated_at: datetime


class RiskStatsWithContextDTO(BaseModel):
    """Risk statistics with context"""
    organization_id: str
    date_range: dict[str, str]
    data: RiskStatsDTO
    generated_at: datetime


class UsageStatsWithContextDTO(BaseModel):
    """Usage statistics with context"""
    organization_id: str
    date_range: dict[str, str]
    data: UsageStatsDTO
    generated_at: datetime


class ThemeStatsWithContextDTO(BaseModel):
    """Theme statistics with context"""
    organization_id: str
    date_range: dict[str, str]
    data: ThemeStatsDTO
    generated_at: datetime


class IntentStatsWithContextDTO(BaseModel):
    """Intent statistics with context"""
    organization_id: str
    date_range: dict[str, str]
    data: IntentStatsDTO
    generated_at: datetime


class TopUsersWithContextDTO(BaseModel):
    """Top users with context"""
    organization_id: str
    date_range: dict[str, str]
    data: list[TopUserDTO]
    generated_at: datetime


class TopPromptsWithContextDTO(BaseModel):
    """Top prompts with context"""
    organization_id: str
    date_range: dict[str, str]
    data: list[TopPromptDTO]
    generated_at: datetime


class RiskyPromptsWithContextDTO(BaseModel):
    """Risky prompts with context"""
    organization_id: str
    date_range: dict[str, str]
    data: list[RiskyPromptDTO]
    generated_at: datetime


# Time-series DTOs for charts

class TimeSeriesDataPointDTO(BaseModel):
    """Single data point in a time series"""
    date: str  # YYYY-MM-DD format
    value: float
    label: Optional[str] = None  # For categorical breakdowns


class MultiSeriesDataPointDTO(BaseModel):
    """Single data point with multiple series (e.g., per-team breakdown)"""
    date: str  # YYYY-MM-DD format
    values: dict[str, float]  # {series_name: value}


class AdoptionCurveRequestDTO(BaseModel):
    """Request parameters for adoption curve"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: Optional[list[int]] = Field(None, description="Filter by team IDs (empty = all teams)")
    granularity: str = Field(default='day', pattern=r'^(day|week|month)$', description="Time granularity")


class AdoptionCurveDataDTO(BaseModel):
    """Adoption curve data response"""
    overall: list[TimeSeriesDataPointDTO]  # Overall usage across all teams
    by_team: dict[str, list[TimeSeriesDataPointDTO]]  # {team_name: data_points}
    total_prompts: int
    total_chats: int
    average_daily_prompts: float


class AdoptionCurveResponseDTO(BaseModel):
    """Adoption curve response with context"""
    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: Optional[list[int]] = None
    data: AdoptionCurveDataDTO
    generated_at: datetime


class RiskTimelineRequestDTO(BaseModel):
    """Request parameters for risk timeline"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: Optional[list[int]] = Field(None, description="Filter by team IDs")
    granularity: str = Field(default='day', pattern=r'^(day|week|month)$', description="Time granularity")


class RiskTimelineDataPointDTO(BaseModel):
    """Risk timeline data point with risk type breakdown"""
    date: str  # YYYY-MM-DD
    total_risky_messages: int
    by_risk_level: dict[str, int]  # {critical: x, high: y, medium: z, low: w}
    by_risk_type: dict[str, int]  # {pii: x, security: y, compliance: z, ...}


class RiskTimelineDataDTO(BaseModel):
    """Risk timeline data response"""
    timeline: list[RiskTimelineDataPointDTO]
    total_risky_messages: int
    risk_level_totals: dict[str, int]
    risk_type_totals: dict[str, int]


class RiskTimelineResponseDTO(BaseModel):
    """Risk timeline response with context"""
    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: Optional[list[int]] = None
    data: RiskTimelineDataDTO
    generated_at: datetime


class QualityTimelineRequestDTO(BaseModel):
    """Request parameters for quality timeline"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: Optional[list[int]] = Field(None, description="Filter by team IDs")
    granularity: str = Field(default='day', pattern=r'^(day|week|month)$', description="Time granularity")


class QualityTimelineDataPointDTO(BaseModel):
    """Quality timeline data point"""
    date: str  # YYYY-MM-DD
    average_score: float
    median_score: Optional[float] = None
    total_rated: int


class QualityTimelineDataDTO(BaseModel):
    """Quality timeline data response"""
    overall: list[QualityTimelineDataPointDTO]  # Overall quality across all teams
    by_team: dict[str, list[QualityTimelineDataPointDTO]]  # {team_name: data_points}
    overall_average: float
    total_rated: int


class QualityTimelineResponseDTO(BaseModel):
    """Quality timeline response with context"""
    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: Optional[list[int]] = None
    data: QualityTimelineDataDTO
    generated_at: datetime


class ThemeTimelineRequestDTO(BaseModel):
    """Request parameters for theme distribution over time"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: Optional[list[int]] = Field(None, description="Filter by team IDs")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top themes to track")


class ThemeDistributionDTO(BaseModel):
    """Theme distribution at a point in time"""
    themes: dict[str, int]  # {theme_name: count}
    total: int


class ThemeTimelineResponseDTO(BaseModel):
    """Theme timeline response"""
    organization_id: str
    date_range: dict[str, str]
    team_filter: Optional[list[int]] = None
    top_themes: list[str]  # Top N themes being tracked
    current_distribution: ThemeDistributionDTO
    generated_at: datetime


class IntentTimelineRequestDTO(BaseModel):
    """Request parameters for intent distribution over time"""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: Optional[list[int]] = Field(None, description="Filter by team IDs")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top intents to track")


class IntentDistributionDTO(BaseModel):
    """Intent distribution at a point in time"""
    intents: dict[str, int]  # {intent_name: count}
    total: int


class IntentTimelineResponseDTO(BaseModel):
    """Intent timeline response"""
    organization_id: str
    date_range: dict[str, str]
    team_filter: Optional[list[int]] = None
    top_intents: list[str]  # Top N intents being tracked
    current_distribution: IntentDistributionDTO
    generated_at: datetime
