"""
Audit routes
"""

from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
from . import (  # noqa: E402
    intents,
    organization_audit,
    quality,
    risk,
    risky_prompts,
    themes,
    top_prompts,
    top_users,
    usage,
)

# Time-series endpoints
from . import adoption_curve
from . import risk_timeline
from . import quality_timeline
from . import theme_distribution
from . import intent_distribution

# Enhanced analytics endpoints
from . import analytics

__all__ = ["router"]
