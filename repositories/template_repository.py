"""Template repository - handles pure database operations for templates"""

from datetime import datetime

from supabase import Client

from domains.entities import Template, TemplateComment, TemplateTitle, TemplateUsage
from services.locale_service import LocaleService


class TemplateRepository:
    """Base repository for template database operations"""

    @staticmethod
    def get_templates_titles(
        client: Client,
        user_id: str | None = None,
        organization_id: str | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TemplateTitle]:
        query = client.table("prompt_templates").select("id, title, folder_id")
        if user_id:
            query = query.eq("user_id", user_id)
        if organization_id:
            query = query.eq("organization_id", organization_id)
        if published is not None:
            query = query.eq("published", published)
        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        templates_data = response.data or []
        templates = [TemplateTitle(**item) for item in templates_data]
        return templates

    @staticmethod
    def get_templates_with_usage(
        client: Client,
        organization_id: str,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TemplateUsage]:
        """Get templates with usage statistics for organization dashboards"""
        query = client.table("prompt_templates").select(
            "id, title, folder_id, usage_count, last_used_at, created_at"
        )
        query = query.eq("organization_id", organization_id)
        if published is not None:
            query = query.eq("published", published)
        query = query.order("usage_count", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        templates_data = response.data or []
        templates = [
            TemplateUsage(
                id=item["id"],
                title=item.get("title", {}),
                folder_id=item.get("folder_id"),
                usage_count=item.get("usage_count", 0),
                last_used_at=item.get("last_used_at"),
                created_at=item.get("created_at"),
            )
            for item in templates_data
        ]
        return templates

    @staticmethod
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
        response = client.table("prompt_templates").select("*").eq("id", template_id).execute()

        if not response.data:
            return None

        data = response.data[0]

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
            published=data.get("published", False),
        )

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        title: dict[str, str],
        description: dict[str, str] | None,
        folder_id: str | None,
        organization_id: str | None,
        tags: list[str] | None,
        workspace_type: str,
    ) -> Template:
        template_data = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "folder_id": folder_id,
            "organization_id": organization_id,
            "tags": tags or [],
            "workspace_type": workspace_type,
        }
        response = client.table("prompt_templates").insert(template_data).execute()
        if len(response.data or []) == 0:
            return None
        data = response.data[0]
        return Template(data)

    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        folder_id: str | None = None,
        tags: list[str] | None = None,
        current_version_id: int | None = None,
    ) -> bool:
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if folder_id is not None:
            update_data["folder_id"] = folder_id
        if tags is not None:
            update_data["tags"] = tags
        if current_version_id is not None:
            update_data["current_version_id"] = current_version_id

        response = client.table("prompt_templates").update(update_data).eq("id", template_id).execute()

        if len(response.data or []) == 0:
            return None
        data = response.data[0]

        return Template(data)

    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        response = client.table("prompt_templates").delete().eq("id", template_id).execute()

        return len(response.data or []) > 0

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> int:
        response = client.table("prompt_templates").select("usage_count").eq("id", template_id).execute()

        if not response.data:
            return 0

        current_count = response.data[0].get("usage_count", 0)
        new_count = current_count + 1

        client.table("prompt_templates").update(
            {"usage_count": new_count, "last_used_at": datetime.utcnow().isoformat()}
        ).eq("id", template_id).execute()

        return new_count

    @staticmethod
    def update_pinned_status(client: Client, user_id: str, template_id: str, is_pinned: bool) -> bool:
        response = (
            client.table("users_metadata").select("pinned_template_ids").eq("user_id", user_id).single().execute()
        )

        if not response.data:
            return False

        current_pinned = response.data.get("pinned_template_ids") or []

        if is_pinned and template_id not in current_pinned:
            current_pinned.append(template_id)
        elif not is_pinned and template_id in current_pinned:
            current_pinned.remove(template_id)

        client.table("users_metadata").update({"pinned_template_ids": current_pinned}).eq("user_id", user_id).execute()

        return True

    @staticmethod
    def get_user_templates_count(client: Client, user_id: str) -> int:
        query = client.table("prompt_templates").select("id").eq("user_id", user_id)
        response = query.execute()
        return len(response.data or [])

    @staticmethod
    def get_organization_templates_count(client: Client, organization_id: str) -> int:
        query = client.table("prompt_templates").select("id").eq("organization_id", organization_id)
        response = query.execute()
        return len(response.data or [])

    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Template]:
        # Search only user's own templates
        query_builder = client.table("prompt_templates").select("*").eq("user_id", user_id)

        # Apply text search on title and description
        query_builder = query_builder.or_(f"title->>en.ilike.%{query}%,description->>en.ilike.%{query}%")

        if tags:
            query_builder = query_builder.contains("tags", tags)

        query_builder = (
            query_builder.order("usage_count", desc=True)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
        )

        response = query_builder.execute()

        templates = []
        for data in response.data or []:
            templates.append(
                Template(
                    id=data["id"],
                    title=data.get("title", {}),
                    description=data.get("description"),
                    folder_id=data.get("folder_id"),
                    organization_id=data.get("organization_id"),
                    user_id=data["user_id"],
                    workspace_type=data["workspace_type"],
                    created_at=data["created_at"],
                    updated_at=data.get("updated_at"),
                    tags=data.get("tags"),
                    usage_count=data.get("usage_count", 0),
                    last_used_at=data.get("last_used_at"),
                    current_version_id=data.get("current_version_id"),
                    is_free=data.get("is_free", True),
                    published=data.get("published", False),
                )
            )

        return templates

    @staticmethod
    def get_comments(
        client: Client, template_id: str, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> list[TemplateComment]:
        from domains.entities import TemplateComment, TemplateCommentAuthor

        parent_comments_response = (
            client.table("prompt_templates_comments")
            .select("*")
            .eq("template_id", template_id)
            .is_("parent_comment_id", "null")
            .order("created_at", desc=True)
            .execute()
        )

        parent_comments_data = parent_comments_response.data or []

        all_user_ids = [c.get("user_id") for c in parent_comments_data if c.get("user_id")]

        for parent_comment in parent_comments_data:
            replies_response = (
                client.table("prompt_templates_comments")
                .select("*")
                .eq("parent_comment_id", parent_comment["id"])
                .order("created_at")
                .execute()
            )

            replies_data = replies_response.data or []
            parent_comment["_replies"] = replies_data

            for reply in replies_data:
                if reply.get("user_id"):
                    all_user_ids.append(reply.get("user_id"))

        users_map = {}
        if all_user_ids:
            users_resp = (
                client.table("users_metadata")
                .select("user_id, name, email, profile_picture_url, metadata")
                .in_("user_id", list(set(all_user_ids)))
                .execute()
            )

            for u in users_resp.data or []:
                meta = u.get("metadata") or {}
                users_map[u.get("user_id")] = {
                    "name": u.get("name") or meta.get("name") or u.get("email"),
                    "profile_picture_url": u.get("profile_picture_url") or meta.get("profile_picture_url"),
                }

        def build_comment(comment_data: dict) -> TemplateComment:
            user_id = comment_data.get("user_id")
            user_info = users_map.get(user_id, {"name": "Unknown", "profile_picture_url": None})

            # Use LocaleService for consistent localization
            content = LocaleService.localize_string(comment_data.get("content"), locale)

            author = TemplateCommentAuthor(
                id=user_id, name=user_info.get("name", "Unknown"), avatar=user_info.get("profile_picture_url")
            )

            return TemplateComment(
                id=comment_data.get("id"),
                text=content,
                parent_id=comment_data.get("parent_comment_id"),
                version_id=comment_data.get("version_id"),
                created_at=comment_data.get("created_at"),
                author=author,
                mentions=comment_data.get("mentions", []),
                replies=[],
            )

        comments = []
        for parent_data in parent_comments_data:
            parent_comment = build_comment(parent_data)

            replies = []
            for reply_data in parent_data.get("_replies", []):
                reply_comment = build_comment(reply_data)
                replies.append(reply_comment)

            parent_comment.replies = replies

            comments.append(parent_comment)

        return comments
