"""
Audit routes
"""

from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
# Time-series endpoints
# Enhanced analytics endpoints
from . import (  # noqa: E402
    adoption_curve,
    analytics,
    intent_distribution,
    intents,
    organization_audit,
    quality,
    quality_timeline,
    risk,
    risk_timeline,
    risky_prompts,
    theme_distribution,
    themes,
    top_prompts,
    top_users,
    usage,
)

__all__ = ["router"]
