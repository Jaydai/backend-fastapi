"""Template repository - handles pure database operations for templates"""
from supabase import Client
from domains.entities import Template, TemplateTitle, TemplateVersion, TemplateComment
from repositories.templates import get_templates_titles, get_template_by_id, create_template, update_template, delete_template, increment_usage, update_pinned_status, get_user_templates_count, get_organization_templates_count
from repositories.template_versions_repository import TemplateVersionRepository
from services.locale_service import LocaleService

class TemplateRepository:
    """Base repository for template database operations"""

    @staticmethod
    def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        return get_templates_titles(client, organization_id, folder_ids, published, user_id, limit, offset)


    @staticmethod
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
       return get_template_by_id(client, template_id)

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        title: dict[str, str],
        description: dict[str, str] | None,
        folder_id: str | None,
        organization_id: str | None,
        tags: list[str] | None,
        workspace_type: str
    ) -> Template:
        return create_template(client, user_id, title, description, folder_id, organization_id, tags, workspace_type)
       


    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        folder_id: str | None = None,
        tags: list[str] | None = None,
        current_version_id: int | None = None
    ) -> bool:
        return update_template(client, template_id, title, description, folder_id, tags, current_version_id)


    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        return delete_template(client, template_id)

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> int:
        return increment_usage(client, template_id)

    @staticmethod
    def update_pinned_status(
        client: Client,
        user_id: str,
        template_id: str,
        is_pinned: bool
    ) -> bool:
        return update_pinned_status(client, user_id, template_id, is_pinned)

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        return TemplateVersionRepository.get_versions(client, template_id)

    @staticmethod
    def get_user_templates_count(client: Client, user_id: str) -> int:
        return get_user_templates_count(client, user_id)

    @staticmethod
    def get_organization_templates_count(client: Client, organization_id: str) -> int:
        return get_organization_templates_count(client, organization_id)

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        author_id: str,
        content: dict[str, str],
        version_number: str | None = None,
        change_notes: dict[str, str] | None = None,
        status: str = "draft",
        optimized_for: list[str] | None = None
    ) -> TemplateVersion:
        if not version_number:
            versions = TemplateRepository.get_versions(client, template_id)
            if versions:
                latest = versions[0].version_number
                try:
                    major, minor = latest.split(".")
                    version_number = f"{major}.{int(minor) + 1}"
                except (ValueError, AttributeError):
                    version_number = "1.1"
            else:
                version_number = "1.0"

        version_data = {
            "template_id": template_id,
            "author_id": author_id,
            "content": content,
            "version_number": version_number,
            "change_notes": change_notes,
            "status": status,
            "is_current": False,
            "is_published": False,
            "usage_count": 0,
            "optimized_for": optimized_for
        }

        response = client.table("prompt_templates_versions").insert(version_data).execute()

        data = response.data[0]
        return TemplateVersion(
            id=data["id"],
            template_id=data["template_id"],
            version_number=data.get("version_number", "1.0"),
            content=data.get("content", {}),
            description=data.get("description"),
            change_notes=data.get("change_notes"),
            author_id=data["author_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            status=data.get("status", "draft"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        content: dict[str, str] | None = None,
        status: str | None = None
    ) -> TemplateVersion | None:
        update_data = {}
        if content is not None:
            update_data["content"] = content
        if status is not None:
            update_data["status"] = status

        if not update_data:
            return TemplateRepository.get_version_by_id(client, version_id)

        response = client.table("prompt_templates_versions")\
            .update(update_data)\
            .eq("id", version_id)\
            .eq("template_id", template_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return TemplateVersion(
            id=data["id"],
            template_id=data["template_id"],
            version_number=data.get("version_number", "1.0"),
            content=data.get("content", {}),
            description=data.get("description"),
            change_notes=data.get("change_notes"),
            author_id=data["author_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            status=data.get("status", "draft"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )

    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> list[Template]:
        # Search only user's own templates
        query_builder = client.table("prompt_templates").select("*").eq("user_id", user_id)

        # Apply text search on title and description
        query_builder = query_builder.or_(f"title->>en.ilike.%{query}%,description->>en.ilike.%{query}%")

        if tags:
            query_builder = query_builder.contains("tags", tags)

        query_builder = query_builder.order("usage_count", desc=True).order("created_at", desc=True).range(offset, offset + limit - 1)

        response = query_builder.execute()

        templates = []
        for data in response.data or []:
            templates.append(Template(
                id=data["id"],
                title=data.get("title", {}),
                description=data.get("description"),
                folder_id=data.get("folder_id"),
                organization_id=data.get("organization_id"),
                company_id=data.get("company_id"),
                user_id=data["user_id"],
                workspace_type=data["workspace_type"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at"),
                tags=data.get("tags"),
                usage_count=data.get("usage_count", 0),
                last_used_at=data.get("last_used_at"),
                current_version_id=data.get("current_version_id"),
                is_free=data.get("is_free", True),
                is_published=data.get("is_published", False)
            ))

        return templates

    @staticmethod
    def get_comments(client: Client, template_id: str, locale: str = LocaleService.DEFAULT_LOCALE) -> list[TemplateComment]:
        from domains.entities import TemplateComment, TemplateCommentAuthor

        parent_comments_response = client.table("prompt_templates_comments")\
            .select("*")\
            .eq("template_id", template_id)\
            .is_("parent_comment_id", "null")\
            .order("created_at", desc=True)\
            .execute()

        parent_comments_data = parent_comments_response.data or []

        all_user_ids = [c.get("user_id") for c in parent_comments_data if c.get("user_id")]

        for parent_comment in parent_comments_data:
            replies_response = client.table("prompt_templates_comments")\
                .select("*")\
                .eq("parent_comment_id", parent_comment["id"])\
                .order("created_at")\
                .execute()

            replies_data = replies_response.data or []
            parent_comment["_replies"] = replies_data

            for reply in replies_data:
                if reply.get("user_id"):
                    all_user_ids.append(reply.get("user_id"))

        users_map = {}
        if all_user_ids:
            users_resp = client.table("users_metadata")\
                .select("user_id, name, email, profile_picture_url, metadata")\
                .in_("user_id", list(set(all_user_ids)))\
                .execute()

            for u in users_resp.data or []:
                meta = u.get("metadata") or {}
                users_map[u.get("user_id")] = {
                    "name": u.get("name") or meta.get("name") or u.get("email"),
                    "profile_picture_url": u.get("profile_picture_url") or meta.get("profile_picture_url"),
                }

        def build_comment(comment_data: dict) -> TemplateComment:
            user_id = comment_data.get("user_id")
            user_info = users_map.get(user_id, {"name": "Unknown", "profile_picture_url": None})

            content = comment_data.get("content")
            if isinstance(content, dict):
                content = content.get(locale) or content.get("en") or next(iter(content.values()), "")

            author = TemplateCommentAuthor(
                id=user_id,
                name=user_info.get("name", "Unknown"),
                avatar=user_info.get("profile_picture_url")
            )

            return TemplateComment(
                id=comment_data.get("id"),
                text=content if isinstance(content, str) else "",
                parent_id=comment_data.get("parent_comment_id"),
                version_id=comment_data.get("version_id"),
                created_at=comment_data.get("created_at"),
                author=author,
                mentions=comment_data.get("mentions", []),
                replies=[]
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
