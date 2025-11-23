"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion

def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
    response = client.table("prompt_templates_versions")\
        .select("*")\
        .eq("template_id", template_id)\
        .order("created_at", desc=True)\
        .execute()

    versions = []
    for data in response.data or []:
        versions.append(TemplateVersion(data))

    return versions