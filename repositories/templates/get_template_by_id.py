"""Template repository - handles pure database operations for templates"""
from supabase import Client
from domains.entities import Template


def get_template_by_id(client: Client, template_id: str) -> Template | None:
    """Get a single template by ID"""
    response = client.table("prompt_templates")\
        .select("*")\
        .eq("id", template_id)\
        .execute()

    if not response.data:
        return None

    data = response.data[0]

    print(f"DATAAAAAAA🙏🏻 ===?. {data}")
    return Template(
        id=data["id"],
        title=data.get("title", {}),
        description=data.get("description"),
        folder_id=data.get("folder_id"),
        organization_id=data.get("organization_id"),
        user_id=data["user_id"],
        created_at=data["created_at"],
        updated_at=data.get("updated_at"),
        usage_count=data.get("usage_count", 0),
        last_used_at=data.get("last_used_at"),
        current_version_id=data.get("current_version_id"),
        is_published=data.get("is_published", False)
    )