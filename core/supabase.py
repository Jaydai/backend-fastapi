"""
Supabase client initialization
"""

import os

import dotenv
from supabase import Client, ClientOptions, create_client

# Load .env.local first (higher priority), then .env as fallback
dotenv.load_dotenv(".env.local")
dotenv.load_dotenv()  # Loads .env if variables not already set

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")
# Support both SUPABASE_SECRET_KEY and SUPABASE_SERVICE_ROLE_KEY
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize service role Supabase client (for admin operations)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)


def create_authenticated_client(access_token: str) -> Client:
    """
    Create a Supabase client authenticated with a user's access token.
    This client will respect RLS policies for the authenticated user.

    Args:
        access_token: The user's JWT access token

    Returns:
        Authenticated Supabase client
    """
    options = ClientOptions()
    options.headers = {"Authorization": f"Bearer {access_token}"}
    return create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, options)
