"""
Audit routes
"""
from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
from . import organization_audit
from . import quality
from . import risk
from . import usage
from . import themes
from . import intents
from . import top_users
from . import top_prompts
from . import risky_prompts

# Time-series endpoints
from . import adoption_curve
from . import risk_timeline
from . import quality_timeline
from . import theme_distribution
from . import intent_distribution

# Enhanced analytics endpoints
from . import analytics

__all__ = ["router"]
