"""
Domain entities for enrichment functionality
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class QualityMetrics:
    """Quality metrics for a chat enrichment"""
    quality_score: int  # 0-100
    clarity_score: int  # 0-5
    context_score: int  # 0-5
    specificity_score: int  # 0-5
    actionability_score: int  # 0-5


@dataclass
class FeedbackDetail:
    """Feedback details for chat quality"""
    summary: str
    strengths: list[str]
    improvements: list[str]
    improved_prompt_example: Optional[str] = None


@dataclass
class EnrichedChat:
    """Domain entity for enriched chat data"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    user_id: Optional[str] = None
    chat_id: Optional[int] = None
    chat_provider_id: Optional[str] = None
    message_provider_id: Optional[str] = None
    is_work_related: bool = False
    theme: Optional[str] = None
    intent: Optional[str] = None
    quality_metrics: Optional[QualityMetrics] = None
    feedback: Optional[FeedbackDetail] = None
    raw_response: Optional[dict] = None
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None
    user_override_quality: bool = False
    user_quality_score: Optional[int] = None


@dataclass
class RiskIssue:
    """Individual risk issue detected in a message"""
    category: str
    severity: str  # low, medium, high, critical
    description: str
    details: Optional[dict] = None


@dataclass
class RiskCategory:
    """Risk assessment for a specific category"""
    level: str  # none, low, medium, high, critical
    score: float  # 0-100
    detected: bool
    details: Optional[str] = None


@dataclass
class EnrichedMessage:
    """Domain entity for enriched message data"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    user_id: Optional[str] = None
    message_id: Optional[int] = None
    message_provider_id: Optional[str] = None
    overall_risk_level: str = "none"
    overall_risk_score: float = 0.0
    risk_categories: dict[str, RiskCategory] = None  # Keys: pii, security, confidential, etc.
    risk_summary: list[str] = None
    detected_issues: list[RiskIssue] = None
    user_whitelist: bool = False
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None

    def __post_init__(self):
        if self.risk_categories is None:
            self.risk_categories = {}
        if self.risk_summary is None:
            self.risk_summary = []
        if self.detected_issues is None:
            self.detected_issues = []
