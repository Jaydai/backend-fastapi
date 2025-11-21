"""
DTOs for enrichment endpoints
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# Request DTOs

class ChatEnrichmentRequestDTO(BaseModel):
    """Request model for single chat enrichment"""
    user_message: str = Field(..., max_length=50000, description="User message content")
    assistant_response: Optional[str] = Field(None, description="Assistant response if available")
    chat_provider_id: Optional[str] = Field(None, description="External chat ID")
    message_provider_id: Optional[str] = Field(None, description="External message ID")
    chat_id: Optional[int] = Field(None, description="Internal chat ID")


class ChatEnrichmentBatchItemDTO(BaseModel):
    """Single item in a batch chat enrichment request"""
    user_message: str = Field(..., max_length=50000)
    assistant_response: Optional[str] = None
    chat_provider_id: Optional[str] = None
    message_provider_id: Optional[str] = None
    chat_id: Optional[int] = None


class ChatEnrichmentBatchRequestDTO(BaseModel):
    """Request model for batch chat enrichment"""
    chats: list[ChatEnrichmentBatchItemDTO] = Field(..., min_length=1, max_length=50)


class EnrichMessageRequestDTO(BaseModel):
    """Request model for single message enrichment"""
    content: str = Field(..., max_length=20000, description="Message content")
    role: str = Field(default="user", description="Message role")
    message_provider_id: Optional[str] = Field(None, description="External message ID")
    message_id: Optional[int] = Field(None, description="Internal message ID")
    context: Optional[dict] = Field(None, description="Additional context")


class EnrichMessageBatchRequestDTO(BaseModel):
    """Request model for batch message enrichment"""
    messages: list[EnrichMessageRequestDTO] = Field(..., min_length=1, max_length=100)


class WhitelistMessageRequestDTO(BaseModel):
    """Request to whitelist a risky message"""
    message_provider_id: str = Field(..., description="Message provider ID to whitelist")


class OverrideQualityRequestDTO(BaseModel):
    """Request to override chat quality score"""
    chat_provider_id: str = Field(..., description="Chat provider ID")
    quality_score: int = Field(..., ge=0, le=10, description="User quality score (0-10)")


# Response DTOs

class QualityMetricsDTO(BaseModel):
    """Quality metrics response"""
    quality_score: int = Field(..., ge=0, le=100)
    clarity_score: int = Field(..., ge=0, le=5)
    context_score: int = Field(..., ge=0, le=5)
    specificity_score: int = Field(..., ge=0, le=5)
    actionability_score: int = Field(..., ge=0, le=5)


class FeedbackDTO(BaseModel):
    """Feedback details response"""
    summary: str
    strengths: list[str]
    improvements: list[str]
    improved_prompt_example: Optional[str] = None


class ChatEnrichmentResponseDTO(BaseModel):
    """Response model for chat enrichment"""
    is_work_related: bool
    theme: str
    intent: str
    quality: Optional[QualityMetricsDTO] = None
    feedback: Optional[FeedbackDTO] = None
    raw: dict
    processing_time_ms: Optional[int] = None


class RiskCategoryDetailDTO(BaseModel):
    """Risk category detail response"""
    level: str  # none, low, medium, high, critical
    score: float = Field(..., ge=0.0, le=100.0)
    detected: bool
    details: Optional[str] = None


class RiskIssueDTO(BaseModel):
    """Individual risk issue response"""
    category: str
    severity: str
    description: str
    details: Optional[dict] = None


class EnrichMessageResponseDTO(BaseModel):
    """Response model for message enrichment"""
    overall_risk_level: str
    overall_risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_categories: dict[str, RiskCategoryDetailDTO]
    risk_summary: list[str]
    detected_issues: list[RiskIssueDTO]
    processing_time_ms: Optional[int] = None


class RiskyMessageDTO(BaseModel):
    """Response model for a single risky message"""
    message_provider_id: str
    risk_level: str
    risk_score: float
    risk_categories: dict[str, RiskCategoryDetailDTO]
    risk_summary: list[str]
    content_preview: str
    created_at: datetime
    user_whitelist: bool = False


class RatedChatDTO(BaseModel):
    """Response model for a single rated chat"""
    chat_provider_id: str
    quality_score: int
    theme: str
    intent: str
    quality_metrics: QualityMetricsDTO
    content_preview: str
    created_at: datetime
    user_override_quality: bool = False
    user_quality_score: Optional[int] = None
