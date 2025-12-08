"""
DTOs for audit endpoints
"""

from datetime import datetime

from pydantic import BaseModel, Field

# Request DTOs


class OrganizationAuditRequestDTO(BaseModel):
    """Request parameters for organization audit"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")


# Response DTOs


class QualityStatsDTO(BaseModel):
    """Quality statistics response"""

    average_score: float
    median_score: float | None = None
    distribution: dict[str, int]  # excellent, good, medium, poor
    total_rated: int
    trend_change: float | None = None
    trend_7days: float | None = None  # 7-day trend percentage change


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
    trend_7days: float | None = None  # 7-day trend percentage change in average risk


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
    daily_average: float | None = None  # Average prompts per day over the period
    trend_7days: float | None = None  # 7-day trend percentage change in daily prompts


class ThemeStatsDTO(BaseModel):
    """Theme distribution response"""

    top_themes: list[dict]  # [{"theme": str, "count": int, "percentage": float}]
    total_categorized: int
    trend_change: dict[str, float] | None = None


class IntentStatsDTO(BaseModel):
    """Intent distribution response"""

    top_intents: list[dict]  # [{"intent": str, "count": int, "percentage": float, "avg_quality": float}]
    total_categorized: int


class TopUserDTO(BaseModel):
    """Top user response"""

    user_id: str
    email: str
    name: str | None = None
    total_prompts: int
    average_quality: float
    work_prompts: int
    high_risk_messages: int


class TopPromptDTO(BaseModel):
    """Top quality prompt response"""

    chat_provider_id: str
    message_provider_id: str | None = None
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
    content_full: str
    created_at: datetime
    user_whitelist: bool = False
    user_email: str | None = None
    user_name: str | None = None


class TeamStatsDTO(BaseModel):
    """Team adoption statistics"""

    team_id: str
    team_name: str
    team_color: str
    active_users: int
    total_prompts: int
    average_quality: float


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
    team_stats: list[TeamStatsDTO] = []
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
    label: str | None = None  # For categorical breakdowns


class MultiSeriesDataPointDTO(BaseModel):
    """Single data point with multiple series (e.g., per-team breakdown)"""

    date: str  # YYYY-MM-DD format
    values: dict[str, float]  # {series_name: value}


class AdoptionCurveRequestDTO(BaseModel):
    """Request parameters for adoption curve"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: list[str | None] = Field(None, description="Filter by team IDs (empty = all teams)")
    granularity: str = Field(default="day", pattern=r"^(day|week|month)$", description="Time granularity")
    view_mode: str = Field(
        default="chats", pattern=r"^(chats|messages|providers|models)$", description="View mode for analytics"
    )


class ProviderDistributionDTO(BaseModel):
    """Provider distribution statistics"""

    provider_name: str
    chat_count: int
    message_count: int
    percentage: float


class AdoptionCurveDataDTO(BaseModel):
    """Adoption curve data response"""

    overall: list[TimeSeriesDataPointDTO]  # Overall usage across all teams
    by_team: dict[str, list[TimeSeriesDataPointDTO]]  # {team_name: data_points}
    total_prompts: int
    total_chats: int
    average_daily_prompts: float
    average_messages_per_chat: float  # Average number of messages per chat
    provider_distribution: list[ProviderDistributionDTO]  # Distribution by provider (ChatGPT, Claude, etc.)
    by_provider: dict[str, list[TimeSeriesDataPointDTO]] | None = None  # Time series per provider
    by_model: dict[str, int] | None = None  # Distribution by model when view_mode is 'models'


class AdoptionCurveResponseDTO(BaseModel):
    """Adoption curve response with context"""

    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: list[str] | None = None
    view_mode: str  # 'chats', 'messages', 'providers', or 'models'
    data: AdoptionCurveDataDTO
    generated_at: datetime


class RiskTimelineRequestDTO(BaseModel):
    """Request parameters for risk timeline"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: list[str | None] = Field(None, description="Filter by team IDs")
    granularity: str = Field(default="day", pattern=r"^(day|week|month)$", description="Time granularity")


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
    team_filter: list[str] | None = None
    data: RiskTimelineDataDTO
    generated_at: datetime


class QualityTimelineRequestDTO(BaseModel):
    """Request parameters for quality timeline (old endpoint)"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: list[str | None] = Field(None, description="Filter by team IDs")
    granularity: str = Field(default="day", pattern=r"^(day|week|month)$", description="Time granularity")


class QualityTimelineDataPointDTO(BaseModel):
    """Quality timeline data point (old endpoint format)"""

    date: str  # YYYY-MM-DD
    average_score: float
    median_score: float | None = None
    total_rated: int


class QualityTimelineDataDTO(BaseModel):
    """Quality timeline data response (old endpoint format)"""

    overall: list[QualityTimelineDataPointDTO]  # Overall quality across all teams
    by_team: dict[str, list[QualityTimelineDataPointDTO]]  # {team_name: data_points}
    overall_average: float
    total_rated: int


class QualityTimelineResponseDTO(BaseModel):
    """Quality timeline response with context (old endpoint format)"""

    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: list[str] | None = None
    data: QualityTimelineDataDTO
    generated_at: datetime


class ThemeTimelineRequestDTO(BaseModel):
    """Request parameters for theme distribution over time"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: list[str | None] = Field(None, description="Filter by team IDs")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top themes to track")


class ThemeDistributionDTO(BaseModel):
    """Theme distribution at a point in time"""

    themes: dict[str, int]  # {theme_name: count}
    total: int


class ThemeTimelineResponseDTO(BaseModel):
    """Theme timeline response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    top_themes: list[str]  # Top N themes being tracked
    current_distribution: ThemeDistributionDTO
    generated_at: datetime


class IntentTimelineRequestDTO(BaseModel):
    """Request parameters for intent distribution over time"""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    team_ids: list[str | None] = Field(None, description="Filter by team IDs")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top intents to track")


class IntentDistributionDTO(BaseModel):
    """Intent distribution at a point in time"""

    intents: dict[str, int]  # {intent_name: count}
    total: int


class IntentTimelineResponseDTO(BaseModel):
    """Intent timeline response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    top_intents: list[str]  # Top N intents being tracked
    current_distribution: IntentDistributionDTO
    generated_at: datetime


# Model and Provider Analytics DTOs


class ModelDistributionItemDTO(BaseModel):
    """Single model distribution item"""

    model_name: str
    count: int
    percentage: float


class ModelDistributionResponseDTO(BaseModel):
    """Model distribution response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    models: list[ModelDistributionItemDTO]
    total_messages: int
    generated_at: datetime


class ProviderDistributionResponseDTO(BaseModel):
    """Provider distribution response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    providers: list[ProviderDistributionDTO]
    total_chats: int
    generated_at: datetime


# Quality Analytics DTOs (New Enhanced Endpoint)


class QualityMetricsTimelineDataPointDTO(BaseModel):
    """Quality metrics at a specific time (new analytics endpoint)"""

    date: str
    quality_score: float | None = None
    clarity_score: float | None = None
    context_score: float | None = None
    specificity_score: float | None = None
    actionability_score: float | None = None
    count: int  # Number of chats rated on this date


class QualityMetricsTimelineResponseDTO(BaseModel):
    """Quality metrics timeline response (new analytics endpoint)"""

    organization_id: str
    date_range: dict[str, str]
    granularity: str
    team_filter: list[str] | None = None
    timeline: list[QualityMetricsTimelineDataPointDTO]
    averages: dict[str, float]  # Overall averages for each metric
    generated_at: datetime


class QualityDistributionBinDTO(BaseModel):
    """Quality score distribution bin"""

    range: str  # e.g., "0-20", "21-40"
    count: int
    percentage: float


class QualityDistributionResponseDTO(BaseModel):
    """Quality score distribution response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    bins: list[QualityDistributionBinDTO]
    total_rated: int
    average_score: float
    generated_at: datetime


# Usage Analytics DTOs


class UsageByHourDataPointDTO(BaseModel):
    """Usage data for a specific hour"""

    hour: int  # 0-23
    weekday_count: int
    weekend_count: int
    total_count: int


class UsageByHourResponseDTO(BaseModel):
    """Usage by hour response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    hourly_data: list[UsageByHourDataPointDTO]
    peak_hour: int
    total_messages: int
    generated_at: datetime


# Risk Analytics DTOs


class RiskCategoryItemDTO(BaseModel):
    """Risk category breakdown"""

    category: str
    count: int
    percentage: float
    severity_breakdown: dict[str, int | None] = None  # {critical: x, high: y, ...}


class RiskCategoriesResponseDTO(BaseModel):
    """Risk categories breakdown response"""

    organization_id: str
    date_range: dict[str, str]
    team_filter: list[str] | None = None
    categories: list[RiskCategoryItemDTO]
    total_risky_messages: int
    generated_at: datetime


# User Profile DTOs


class UserProfileKPIsDTO(BaseModel):
    """User profile KPIs"""

    total_prompts: int
    average_quality: float
    work_percentage: float
    high_risk_count: int
    quality_trend: float | None = None
    percentile_ranking: float


class UserProfileComparisonDTO(BaseModel):
    """User comparison to organization averages"""

    org_average_quality: float
    org_average_prompts: float
    org_average_work_percentage: float
    user_quality_vs_org: float  # Percentage difference
    user_prompts_vs_org: float  # Percentage difference


class UserActivityPointDTO(BaseModel):
    """User activity data point for timeline"""

    date: str
    prompt_count: int
    average_quality: float


class UserProviderUsageDTO(BaseModel):
    """User provider usage breakdown"""

    provider_name: str
    chat_count: int
    percentage: float


class UserThemeDataDTO(BaseModel):
    """User theme distribution"""

    theme: str
    count: int
    percentage: float


class UserIntentDataDTO(BaseModel):
    """User intent distribution with quality"""

    intent: str
    count: int
    percentage: float
    avg_quality: float


class UserProfileDataDTO(BaseModel):
    """Complete user profile data"""

    user_id: str
    email: str
    name: str | None = None
    kpis: UserProfileKPIsDTO
    comparison: UserProfileComparisonDTO
    activity_timeline: list[UserActivityPointDTO]
    provider_breakdown: list[UserProviderUsageDTO]
    themes: list[UserThemeDataDTO]
    intents: list[UserIntentDataDTO]


class UserProfileResponseDTO(BaseModel):
    """User profile response with context"""

    organization_id: str
    date_range: dict[str, str]
    data: UserProfileDataDTO
    generated_at: datetime
