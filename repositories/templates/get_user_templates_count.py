"""Get template titles repository"""
from supabase import Client



def get_user_templates_count(
    client: Client,
    user_id: str,
) -> int:

    query = client.table("prompt_templates").select("id").eq("user_id", user_id)
    response = query.execute()
    return len(response.data or [])