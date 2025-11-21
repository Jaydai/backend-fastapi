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


class ThemeStatsDTO(BaseModel):
    """Theme distribution response"""
    top_themes: list[dict]  # [{"theme": str, "count": int, "percentage": float}]
    total_categorized: int
    trend_change: Optional[dict[str, float]] = None


class IntentStatsDTO(BaseModel):
    """Intent distribution response"""
    top_intents: list[dict]  # [{"intent": str, "count": int, "avg_quality": float}]
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
