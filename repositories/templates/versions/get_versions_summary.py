"""Repository for getting version summaries without content."""

from supabase import Client
from dataclasses import dataclass


@dataclass
class VersionSummary:
    """Minimal version data for version selector."""
    id: int
    name: dict[str, str]  # Localized name
    slug: str
    is_current: bool


def get_versions_summary(client: Client, template_id: str) -> list[VersionSummary]:
    response = client.table("prompt_templates_versions").select(
        "id, name, slug, is_current"
    ).eq("template_id", template_id).order("created_at", desc=True).execute()

    if not response.data:
        return []

    return [VersionSummary(**item) for item in response.data]
