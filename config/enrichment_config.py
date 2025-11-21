"""
Configuration for enrichment services
"""
import os
from enum import Enum


class EnrichmentModels(str, Enum):
    """Available models for enrichment"""
    GPT_4_NANO = "gpt-4.1-nano"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_4 = "gpt-4"


class EnrichmentConfig:
    """Configuration settings for enrichment services"""

    # Model Configuration
    DEFAULT_CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", EnrichmentModels.GPT_4_NANO)
    DEFAULT_RISK_ASSESSMENT_MODEL = os.getenv("RISK_ASSESSMENT_MODEL", EnrichmentModels.GPT_4_NANO)

    # Temperature settings (lower = more deterministic)
    CLASSIFICATION_TEMPERATURE = 0.1
    RISK_ASSESSMENT_TEMPERATURE = 0.1

    # Token limits
    CLASSIFICATION_MAX_TOKENS = 400
    RISK_ASSESSMENT_MAX_TOKENS = 800

    # Content limits
    MAX_USER_MESSAGE_LENGTH = 50000  # For requests
    MAX_TRUNCATED_MESSAGE_LENGTH = 20000  # For LLM processing
    MAX_ASSISTANT_RESPONSE_LENGTH = 20000

    # Batch limits
    MAX_CHAT_BATCH_SIZE = 50
    MAX_MESSAGE_BATCH_SIZE = 100

    # Risk Assessment Configuration
    RISK_LEVEL_THRESHOLDS = {
        "critical": 80.0,
        "high": 60.0,
        "medium": 40.0,
        "low": 20.0,
        "none": 0.0
    }

    # Risk category weights for overall score calculation
    RISK_CATEGORY_WEIGHTS = {
        "security": 1.5,        # Highest priority (credentials, API keys)
        "confidential": 1.3,    # Business-critical data
        "pii": 1.2,             # Personal information
        "data_leakage": 1.1,    # Internal systems/code
        "compliance": 1.0,      # Regulatory concerns
        "misinformation": 0.7   # Lower priority
    }

    # Quality score distribution buckets
    QUALITY_DISTRIBUTION_BUCKETS = {
        "excellent": (80, 100),
        "good": (60, 79),
        "medium": (40, 59),
        "poor": (0, 39)
    }

    # Retry configuration
    MAX_LLM_RETRIES = 2
    LLM_RETRY_DELAY_SECONDS = 1

    # Timeout configuration
    LLM_REQUEST_TIMEOUT_SECONDS = 30

    @classmethod
    def get_risk_level_from_score(cls, score: float) -> str:
        """Determine risk level from numeric score"""
        if score >= cls.RISK_LEVEL_THRESHOLDS["critical"]:
            return "critical"
        elif score >= cls.RISK_LEVEL_THRESHOLDS["high"]:
            return "high"
        elif score >= cls.RISK_LEVEL_THRESHOLDS["medium"]:
            return "medium"
        elif score >= cls.RISK_LEVEL_THRESHOLDS["low"]:
            return "low"
        else:
            return "none"

    @classmethod
    def get_quality_bucket(cls, score: int) -> str:
        """Determine quality bucket from numeric score"""
        for bucket, (min_score, max_score) in cls.QUALITY_DISTRIBUTION_BUCKETS.items():
            if min_score <= score <= max_score:
                return bucket
        return "poor"


# Export config instance
enrichment_config = EnrichmentConfig()
