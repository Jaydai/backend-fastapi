from supabase import Client
from domains.entities import TemplateTitle

def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        query = client.table("prompt_templates").select("id, title")
        
        if organization_id:
            query = query.eq("organization_id", organization_id)
        elif user_id:
            query = query.eq("user_id", user_id)
        if folder_ids is not None:
            if len(folder_ids) == 0:
                query = query.is_("folder_id", "null")
            else:
                query = query.in_("folder_id", folder_ids)
        if published is not None:
            # Need to check if template has published version
            # This requires a subquery or join - for now, we'll handle this differently
            pass

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        templates_data = response.data or []

        templates = [TemplateTitle(**item) for item in templates_data]
        return templates