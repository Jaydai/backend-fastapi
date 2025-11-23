"""Get template titles - simplified version"""
from supabase import Client
from domains.entities import TemplateTitle


def get_templates_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[TemplateTitle]:
    """
    Get template titles (id, title) with simple filtering.

    Logic:
    - If folder_id provided: Get templates in that folder
    - Else if organization_id provided: Get templates for that organization
    - Else if user_id provided: Get templates for that user
    - Else: Get all templates (RLS will filter based on access)
    """
    query = client.table("prompt_templates").select("id, title")

    # Priority 1: Filter by folder if specified
    if folder_id is not None:
        if folder_id == "root" or folder_id == "":
            query = query.is_("folder_id", "null")
        else:
            query = query.eq("folder_id", folder_id)
    # Priority 2: Filter by organization
    elif organization_id:
        query = query.eq("organization_id", organization_id)
    # Priority 3: Filter by user
    elif user_id:
        query = query.eq("user_id", user_id)
    # Priority 4: Get all (RLS will filter)

    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    templates_data = response.data or []

    templates = [TemplateTitle(**item) for item in templates_data]
    return templates