"""
FastAPI Dependencies

Reusable dependencies for route handlers.
Provides authentication and database client access.
"""

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from supabase import Client

logger = logging.getLogger(__name__)


async def get_authenticated_user(request: Request) -> str:
    """
    Get authenticated user ID from request state.

    The auth middleware sets user_id on request.state after
    validating the JWT token.

    Args:
        request: FastAPI request object

    Returns:
        User ID string

    Raises:
        HTTPException: 401 if not authenticated
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        logger.warning("Auth dependency: user_id not found in request state")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_id:
        logger.warning("Auth dependency: user_id is None or empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_supabase_client(request: Request) -> Client:
    """
    Get Supabase client from request state.

    The auth middleware initializes a Supabase client with
    the user's access token for RLS.

    Args:
        request: FastAPI request object

    Returns:
        Authenticated Supabase client

    Raises:
        HTTPException: 500 if client not available
    """
    try:
        client = request.state.supabase_client
    except AttributeError:
        logger.error("Supabase client not found in request state")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )

    if not client:
        logger.error("Supabase client is None")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )

    return client


# Type aliases for cleaner route signatures
# Usage: async def my_route(user_id: AuthenticatedUser, client: SupabaseClient)
AuthenticatedUser = Annotated[str, Depends(get_authenticated_user)]
SupabaseClient = Annotated[Client, Depends(get_supabase_client)]


# Combined dependency for routes that need both
async def get_auth_context(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
) -> tuple[str, Client]:
    """
    Get both authenticated user and Supabase client.

    Convenience dependency that returns both common dependencies.

    Args:
        user_id: From get_authenticated_user
        client: From get_supabase_client

    Returns:
        Tuple of (user_id, supabase_client)
    """
    return user_id, client


AuthContext = Annotated[tuple[str, Client], Depends(get_auth_context)]
