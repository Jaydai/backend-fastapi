"""
Domain entities for enrichment functionality
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class QualityMetrics:
    """Quality metrics for a chat enrichment"""

    quality_score: int  # 0-100
    clarity_score: int  # 0-5
    context_score: int  # 0-5
    specificity_score: int  # 0-5
    actionability_score: int  # 0-5
    complexity_score: Optional[int] = None  # 1-5, task complexity


@dataclass
class FeedbackDetail:
    """Feedback details for chat quality"""

    summary: str
    strengths: list[str]
    improvements: list[str]
    improved_prompt_example: Optional[str] = None
    personalized_tip: Optional[str] = None  # Tailored advice based on skill level


@dataclass
class DomainExpertise:
    """Domain expertise detection"""
    theme_area: str  # Primary domain (coding, marketing, etc.)
    sub_specialties: list[str]  # Detected specialties
    tech_stack: list[str]  # Technologies/tools mentioned
    experience_level: str  # beginner, intermediate, advanced, expert


@dataclass
class ProductivityIndicators:
    """Organizational productivity insights"""
    estimated_complexity: str  # simple, moderate, complex, very_complex
    collaboration_signals: list[str]  # Teamwork indicators
    reusability_score: int  # 0-100: How templateable is this prompt


@dataclass
class EnrichedChat:
    """Domain entity for enriched chat data"""

    id: int | None = None
    created_at: datetime | None = None
    user_id: str | None = None
    chat_id: int | None = None
    chat_provider_id: str | None = None
    message_provider_id: str | None = None
    is_work_related: bool = False
    theme: Optional[str] = None
    intent: Optional[str] = None
    skill_level: Optional[str] = None  # beginner, intermediate, advanced, expert
    domain_expertise: Optional[DomainExpertise] = None
    quality_metrics: Optional[QualityMetrics] = None
    feedback: Optional[FeedbackDetail] = None
    productivity_indicators: Optional[ProductivityIndicators] = None
    raw_response: Optional[dict] = None
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None
    user_override_quality: bool = False
    user_quality_score: int | None = None


@dataclass
class RiskIssue:
    """Individual risk issue detected in a message"""

    category: str
    severity: str  # low, medium, high, critical
    description: str
    details: dict | None = None


@dataclass
class RiskCategory:
    """Risk assessment for a specific category"""

    level: str  # none, low, medium, high, critical
    score: float  # 0-100
    detected: bool
    details: Optional[str] = None
    confidence: Optional[float] = None  # 0-100: Detection confidence
    suggested_redaction: Optional[str] = None  # How to safely redact this content


@dataclass
class EnrichedMessage:
    """Domain entity for enriched message data"""

    id: int | None = None
    created_at: datetime | None = None
    user_id: str | None = None
    message_id: int | None = None
    message_provider_id: str | None = None
    overall_risk_level: str = "none"
    overall_risk_score: float = 0.0
    overall_confidence: Optional[float] = None  # Average confidence across detected risks
    suggested_action: Optional[str] = None  # block, warn, review, or allow
    risk_categories: dict[str, RiskCategory] = None  # Keys: pii, security, confidential, etc.
    risk_summary: list[str] = None
    detected_issues: list[RiskIssue] = None
    user_whitelist: bool = False
    processing_time_ms: int | None = None
    model_used: str | None = None

    def __post_init__(self):
        if self.risk_categories is None:
            self.risk_categories = {}
        if self.risk_summary is None:
            self.risk_summary = []
        if self.detected_issues is None:
            self.detected_issues = []
