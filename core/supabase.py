"""
Supabase client initialization
"""
from supabase import create_client, Client, ClientOptions
import dotenv
import os

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

# Initialize service role Supabase client (for admin operations)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)
