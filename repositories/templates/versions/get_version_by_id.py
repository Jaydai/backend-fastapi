"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion

def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
    """Get a specific version by ID"""
    response = client.table("prompt_templates_versions")\
        .select("*")\
        .eq("id", version_id)\
        .execute()

    if not response.data:
        return None

    data = response.data[0]
    return TemplateVersion(data)