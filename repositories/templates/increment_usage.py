
from supabase import Client
from datetime import datetime


def increment_usage(client: Client, template_id: str) -> int:
    response = client.table("prompt_templates")\
        .select("usage_count")\
        .eq("id", template_id)\
        .execute()

    if not response.data:
        return 0

    current_count = response.data[0].get("usage_count", 0)
    new_count = current_count + 1

    client.table("prompt_templates")\
        .update({
            "usage_count": new_count,
            "last_used_at": datetime.utcnow().isoformat()
        })\
        .eq("id", template_id)\
        .execute()

    return new_count