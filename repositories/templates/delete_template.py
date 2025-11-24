from supabase import Client

def delete_template(client: Client, template_id: str) -> bool:
    response = client.table("prompt_templates")\
        .delete()\
        .eq("id", template_id)\
        .execute()

    return len(response.data or []) > 0