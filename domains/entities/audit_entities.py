"""
Domain entities for audit functionality
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class QualityStats:
    """Quality statistics aggregation"""

    average_score: float
    median_score: float | None = None
    distribution: dict[str, int] | None = None  # excellent, good, medium, poor
    total_rated: int = 0
    trend_change: float | None = None  # Percentage change vs previous period

    def __post_init__(self):
        if self.distribution is None:
            self.distribution = {"excellent": 0, "good": 0, "medium": 0, "poor": 0}


@dataclass
class RiskStats:
    """Risk statistics aggregation"""

    total_messages_assessed: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    none_count: int = 0
    pii_detected_count: int = 0
    credentials_detected_count: int = 0
    sensitive_data_count: int = 0
    average_risk_score: float = 0.0
    risk_distribution: dict[str, int] | None = None

    def __post_init__(self):
        if self.risk_distribution is None:
            self.risk_distribution = {
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count,
                "none": self.none_count,
            }


@dataclass
class UsageStats:
    """Usage statistics aggregation"""

    total_prompts: int = 0
    total_chats: int = 0
    active_users: int = 0
    work_related_count: int = 0
    personal_count: int = 0
    work_percentage: float = 0.0
    average_prompts_per_user: float = 0.0
    average_quality_score: float = 0.0


@dataclass
class ThemeStats:
    """Theme distribution statistics"""

    top_themes: list[dict[str, any]] = None  # [{"theme": str, "count": int, "percentage": float}]
    total_categorized: int = 0
    trend_change: dict[str, float] | None = None  # Per-theme percentage changes

    def __post_init__(self):
        if self.top_themes is None:
            self.top_themes = []
        if self.trend_change is None:
            self.trend_change = {}


@dataclass
class IntentStats:
    """Intent distribution statistics"""

    top_intents: list[dict[str, any]] = None  # [{"intent": str, "count": int, "avg_quality": float}]
    total_categorized: int = 0

    def __post_init__(self):
        if self.top_intents is None:
            self.top_intents = []


@dataclass
class TopUser:
    """Top user by activity"""

    user_id: str
    email: str
    total_prompts: int
    average_quality: float
    work_prompts: int
    high_risk_messages: int
    name: str | None = None


@dataclass
class TopPrompt:
    """Top quality prompt"""

    chat_provider_id: str
    quality_score: int
    theme: str
    intent: str
    content_preview: str  # First 200 chars
    created_at: datetime
    message_provider_id: str | None = None


@dataclass
class RiskyPrompt:
    """High-risk prompt"""

    message_provider_id: str
    risk_level: str
    risk_score: float
    risk_categories: list[str]
    content_preview: str  # First 200 chars
    content_full: str  # Full content
    created_at: datetime
    user_whitelist: bool = False
    user_email: Optional[str] = None
    user_name: Optional[str] = None


@dataclass
class OrganizationAudit:
    """Complete organization audit data"""

    organization_id: str
    organization_name: str
    date_range: dict[str, str]  # start_date, end_date
    quality_stats: QualityStats
    risk_stats: RiskStats
    usage_stats: UsageStats
    theme_stats: ThemeStats
    intent_stats: IntentStats
    top_users: list[TopUser]
    top_prompts: list[TopPrompt]
    riskiest_prompts: list[RiskyPrompt]
    generated_at: datetime

    def __post_init__(self):
        if self.top_users is None:
            self.top_users = []
        if self.top_prompts is None:
            self.top_prompts = []
        if self.riskiest_prompts is None:
            self.riskiest_prompts = []
