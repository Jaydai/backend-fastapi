"""Get template titles repository"""
from supabase import Client



def get_organization_templates_count(
    client: Client,
    organization_id: str,
) -> int:

    query = client.table("prompt_templates").select("id").eq("organization_id", organization_id)
    response = query.execute()
    return len(response.data or [])