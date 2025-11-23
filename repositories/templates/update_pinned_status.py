from supabase import Client

def update_pinned_status(
    client: Client,
    user_id: str,
    template_id: str,
    is_pinned: bool
) -> bool:
    response = client.table("users_metadata")\
        .select("pinned_template_ids")\
        .eq("user_id", user_id)\
        .single()\
        .execute()

    if not response.data:
        return False

    current_pinned = response.data.get("pinned_template_ids") or []

    if is_pinned and template_id not in current_pinned:
        current_pinned.append(template_id)
    elif not is_pinned and template_id in current_pinned:
        current_pinned.remove(template_id)

    client.table("users_metadata")\
        .update({"pinned_template_ids": current_pinned})\
        .eq("user_id", user_id)\
        .execute()

    return True
