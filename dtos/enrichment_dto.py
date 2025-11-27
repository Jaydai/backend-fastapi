"""
DTOs for enrichment endpoints
"""

from datetime import datetime

from pydantic import BaseModel, Field

# Request DTOs


class ChatEnrichmentRequestDTO(BaseModel):
    """Request model for single chat enrichment"""

    user_message: str = Field(..., max_length=50000, description="User message content")
    assistant_response: Optional[str] = Field(None, description="Assistant response if available")
    chat_provider_id: Optional[str] = Field(None, description="External chat ID")
    message_provider_id: Optional[str] = Field(None, description="External message ID")
    chat_id: Optional[int] = Field(None, description="Internal chat ID")
    user_id: Optional[str] = Field(None, description="User ID for unauthenticated batch processing")


class ChatEnrichmentBatchItemDTO(BaseModel):
    """Single item in a batch chat enrichment request"""

    user_message: str = Field(..., max_length=50000)
    assistant_response: Optional[str] = None
    chat_provider_id: Optional[str] = None
    message_provider_id: Optional[str] = None
    chat_id: Optional[int] = None
    user_id: Optional[str] = Field(None, description="User ID for unauthenticated batch processing")


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
    user_id: Optional[str] = Field(None, description="User ID for unauthenticated batch processing")


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

# NEW: Advanced enrichment DTOs (defined first to avoid circular dependencies)


class DomainExpertiseDTO(BaseModel):
    """Domain expertise detection"""

    theme_area: str = Field(..., description="Primary domain (coding, marketing, etc.)")
    sub_specialties: list[str] = Field(default_factory=list, description="Detected specialties")
    tech_stack: list[str] = Field(default_factory=list, description="Technologies/tools mentioned")
    experience_level: str = Field(..., description="beginner, intermediate, advanced, expert")


class ProductivityIndicatorsDTO(BaseModel):
    """Organizational productivity insights"""

    estimated_complexity: str = Field(..., description="simple, moderate, complex, very_complex")
    collaboration_signals: list[str] = Field(default_factory=list, description="Teamwork indicators")
    reusability_score: int = Field(..., ge=0, le=100, description="How templateable is this prompt")


class QualityMetricsDTO(BaseModel):
    """Quality metrics response"""

    quality_score: int = Field(..., ge=0, le=100)
    clarity_score: int = Field(..., ge=0, le=5)
    context_score: int = Field(..., ge=0, le=5)
    specificity_score: int = Field(..., ge=0, le=5)
    actionability_score: int = Field(..., ge=0, le=5)
    complexity_score: Optional[int] = Field(None, ge=1, le=5, description="Task complexity (1-5)")


class FeedbackDTO(BaseModel):
    """Feedback details response"""

    summary: str
    strengths: list[str]
    improvements: list[str]
    improved_prompt_example: Optional[str] = None
    personalized_tip: Optional[str] = Field(None, description="Tailored advice based on skill level")


class ChatEnrichmentResponseDTO(BaseModel):
    """Response model for chat enrichment"""

    is_work_related: bool
    theme: str
    intent: str
    skill_level: Optional[str] = Field(None, description="beginner, intermediate, advanced, expert")
    domain_expertise: Optional[DomainExpertiseDTO] = None
    quality: Optional[QualityMetricsDTO] = None
    feedback: Optional[FeedbackDTO] = None
    productivity_indicators: Optional[ProductivityIndicatorsDTO] = None
    raw: dict
    processing_time_ms: int | None = None


class RiskCategoryDetailDTO(BaseModel):
    """Risk category detail response"""

    level: str  # none, low, medium, high, critical
    score: float = Field(..., ge=0.0, le=100.0)
    detected: bool
    details: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=100.0, description="Detection confidence (0-100)")
    suggested_redaction: Optional[str] = Field(None, description="How to safely redact this content")


class RiskIssueDTO(BaseModel):
    """Individual risk issue response"""

    category: str
    severity: str
    description: str
    details: Optional[dict | str] = None


class EnrichMessageResponseDTO(BaseModel):
    """Response model for message enrichment"""

    overall_risk_level: str
    overall_risk_score: float = Field(..., ge=0.0, le=100.0)
    overall_confidence: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="Average confidence across detected risks"
    )
    suggested_action: Optional[str] = Field(None, description="Recommended action: block, warn, review, or allow")
    risk_categories: dict[str, RiskCategoryDetailDTO]
    risk_summary: list[str]
    detected_issues: list[RiskIssueDTO]
    processing_time_ms: int | None = None


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
    user_quality_score: int | None = None
