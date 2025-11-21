from supabase import Client
from domains.entities import Template, TemplateVersion, TemplateTitle

class TemplateRepository:
    @staticmethod
    def get_all_templates_title() -> list[TemplateTitle]:
        from core.supabase import supabase
        response = supabase.table("prompt_templates").select("id, title").execute()
        return [TemplateTitle(**item) for item in response.data]

    @staticmethod
    def _get_user_metadata(client: Client, user_id: str) -> dict:
        response = client.table("users_metadata")\
            .select("*")\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        if not response.data:
            return {"company_id": None, "organization_ids": [], "roles": {}}

        return response.data

    @staticmethod
    def get_templates(
        client: Client,
        user_id: str,
        workspace_type: str | None = None,
        organization_id: str | None = None,
        company_id: str | None = None,
        folder_id: int | None = None,
        tags: list[str] | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Template]:
        query = client.table("prompt_templates").select("id, title, description, folder_id, organization_id, company_id, user_id, workspace_type, created_at, updated_at, tags, usage_count, current_version_id, is_free")

        if workspace_type == "all" or (not workspace_type and not organization_id and not company_id):
            user_metadata = TemplateRepository._get_user_metadata(client, user_id)
            conditions = [f"user_id.eq.{user_id}"]

            company = user_metadata.get("company_id")
            if company:
                conditions.append(f"company_id.eq.{company}")

            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}
            if org_roles:
                for org_id in org_roles.keys():
                    conditions.append(f"organization_id.eq.{org_id}")

            query = query.or_(",".join(conditions))
        elif workspace_type == "user":
            query = query.eq("user_id", user_id).is_("organization_id", "null").is_("company_id", "null")
        elif workspace_type == "company":
            target_company_id = company_id
            if not target_company_id:
                user_metadata = TemplateRepository._get_user_metadata(client, user_id)
                target_company_id = user_metadata["company_id"]

            if not target_company_id:
                return []

            query = query.eq("company_id", target_company_id)
        elif workspace_type == "organization":
            user_metadata = TemplateRepository._get_user_metadata(client, user_id)
            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}

            if organization_id:
                if organization_id not in org_roles:
                    return []
                query = query.eq("organization_id", organization_id)
            else:
                if not org_roles:
                    return []
                query = query.in_("organization_id", list(org_roles.keys()))

        if folder_id is not None:
            query = query.eq("folder_id", folder_id)

        if tags:
            query = query.contains("tags", tags)

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)

        response = query.execute()

        templates_data = response.data or []

        if published is True:
            template_ids = [t["id"] for t in templates_data]
            if template_ids:
                versions_query = client.table("prompt_templates_versions")\
                    .select("template_id")\
                    .in_("template_id", template_ids)\
                    .eq("is_published", True)\
                    .execute()

                published_template_ids = set(v["template_id"] for v in (versions_query.data or []))
                templates_data = [t for t in templates_data if t["id"] in published_template_ids]

        templates = []
        for data in templates_data:
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
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
        response = client.table("prompt_templates").select("*").eq("id", template_id).execute()

        if not response.data:
            return None

        data = response.data[0] if response.data else None
        if not data:
            return None
        return Template(
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
        )

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        title: dict[str, str],
        description: dict[str, str] | None,
        folder_id: str | None,  # UUID
        organization_id: str | None,
        company_id: str | None,
        tags: list[str] | None,
        workspace_type: str
    ) -> Template:
        template_data = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "folder_id": folder_id,
            "organization_id": organization_id,
            "company_id": company_id,
            "tags": tags,
            "workspace_type": workspace_type,
            "usage_count": 0,
            "is_free": True
        }

        response = client.table("prompt_templates").insert(template_data).execute()

        data = response.data[0]
        return Template(
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
        )

    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        folder_id: int | None = None,
        tags: list[str] | None = None,
        current_version_id: int | None = None
    ) -> Template:
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

        data = response.data[0]
        return Template(
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
        )

    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        # Check if template exists first
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return False

        client.table("prompt_templates").update({"current_version_id": None}).eq("id", template_id).execute()
        client.table("prompt_templates_versions").delete().eq("template_id", template_id).execute()
        response = client.table("prompt_templates").delete().eq("id", template_id).execute()
        return len(response.data) > 0 if response.data else False

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> int:
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return 0

        new_count = template.usage_count + 1
        client.table("prompt_templates").update({
            "usage_count": new_count,
            "last_used_at": "now()"
        }).eq("id", template_id).execute()

        return new_count

    @staticmethod
    def update_pinned_status(client: Client, user_id: str, template_id: str, is_pinned: bool) -> bool:
        response = client.table("users_metadata").select("pinned_template_ids").eq("user_id", user_id).single().execute()

        if not response.data:
            pinned_ids = []
        else:
            pinned_ids = response.data.get("pinned_template_ids") or []

        if is_pinned:
            if template_id not in pinned_ids:
                pinned_ids.append(template_id)
        else:
            if template_id in pinned_ids:
                pinned_ids.remove(template_id)

        client.table("users_metadata").update({"pinned_template_ids": pinned_ids}).eq("user_id", user_id).execute()
        return True

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        response = client.table("prompt_templates_versions").select("*").eq("template_id", template_id).order("created_at", desc=True).execute()

        versions = []
        for data in response.data or []:
            versions.append(TemplateVersion(
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
            ))

        return versions

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
        response = client.table("prompt_templates_versions").select("*").eq("id", version_id).single().execute()

        if not response.data:
            return None

        data = response.data
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
                except:
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
    def get_comments(client: Client, template_id: str, locale: str = "en") -> list:
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