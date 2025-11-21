"""
Audit routes
"""
from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
from . import organization_audit

__all__ = ["router"]
