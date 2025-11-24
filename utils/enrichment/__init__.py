"""
Enrichment Utilities
Helper functions for cleaner, more readable code
"""

from .aggregators import (
    aggregate_intent_stats,
    aggregate_quality_stats,
    aggregate_risk_stats,
    aggregate_risky_prompts,
    aggregate_theme_stats,
    aggregate_top_prompts,
    aggregate_top_users,
    aggregate_usage_stats,
)
from .dto_mappers import (
    classification_to_enriched_chat,
    classification_to_response_dto,
    intent_stats_to_dto,
    quality_stats_to_dto,
    risk_assessment_to_enriched_message,
    risk_assessment_to_response_dto,
    risk_stats_to_dto,
    risky_prompt_to_dto,
    theme_stats_to_dto,
    top_prompt_to_dto,
    top_user_to_dto,
    usage_stats_to_dto,
)
from .validators import (
    ensure_required_fields,
    get_risk_level_hierarchy,
    is_valid_risk_level,
    sanitize_classification_result,
    sanitize_risk_assessment_result,
    truncate_message,
    validate_quality_scores,
    validate_risk_scores,
)

__all__ = [
    # DTO Mappers
    "classification_to_enriched_chat",
    "classification_to_response_dto",
    "risk_assessment_to_enriched_message",
    "risk_assessment_to_response_dto",
    "quality_stats_to_dto",
    "risk_stats_to_dto",
    "usage_stats_to_dto",
    "theme_stats_to_dto",
    "intent_stats_to_dto",
    "top_user_to_dto",
    "top_prompt_to_dto",
    "risky_prompt_to_dto",
    # Aggregators
    "aggregate_quality_stats",
    "aggregate_risk_stats",
    "aggregate_usage_stats",
    "aggregate_theme_stats",
    "aggregate_intent_stats",
    "aggregate_top_users",
    "aggregate_top_prompts",
    "aggregate_risky_prompts",
    # Validators
    "truncate_message",
    "validate_quality_scores",
    "validate_risk_scores",
    "ensure_required_fields",
    "sanitize_classification_result",
    "sanitize_risk_assessment_result",
    "is_valid_risk_level",
    "get_risk_level_hierarchy",
]
