from supabase import Client
from domains.entities import Block, BlockTitle

class BlockRepository:
    @staticmethod
    def _get_user_metadata(client: Client, user_id: str) -> dict:
        response = client.table("users_metadata")\
            .select("*")\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        if not response.data:
            return {"organization_ids": [], "roles": {}}

        return response.data

    @staticmethod
    def get_blocks(
        client: Client,
        user_id: str,
        block_type: str | None = None,
        workspace_type: str | None = None,
        organization_id: str | None = None,
        published: bool | None = None,
        search_query: str | None = None
    ) -> list[Block]:
        query = client.table("prompt_blocks").select("*")

        if workspace_type == "all" or (not workspace_type and not organization_id):
            user_metadata = BlockRepository._get_user_metadata(client, user_id)
            conditions = [f"user_id.eq.{user_id}"]

            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}
            if org_roles:
                for org_id in org_roles.keys():
                    conditions.append(f"organization_id.eq.{org_id}")

            query = query.or_(",".join(conditions))
        elif workspace_type == "user":
            query = query.eq("user_id", user_id).is_("organization_id", "null")
        elif workspace_type == "organization":
            user_metadata = BlockRepository._get_user_metadata(client, user_id)
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

        if block_type is not None:
            query = query.eq("type", block_type)

        if published is not None:
            query = query.eq("published", published)

        if search_query:
            query = query.or_(f"title->>custom.ilike.%{search_query}%,content->>custom.ilike.%{search_query}%")

        query = query.order("created_at", desc=True)

        response = query.execute()

        blocks = []
        for data in response.data or []:
            blocks.append(Block(
                id=data["id"],
                type=data["type"],
                title=data.get("title", {}),
                description=data.get("description"),
                content=data.get("content", {}),
                published=data.get("published", False),
                user_id=data["user_id"],
                organization_id=data.get("organization_id"),
                workspace_type=data.get("workspace_type", "user"),
                created_at=data["created_at"],
                updated_at=data.get("updated_at"),
                usage_count=data.get("usage_count", 0)
            ))

        return blocks

    @staticmethod
    def get_blocks_titles(
        client: Client,
        organization_id: str | None = None,
        types: list[str] | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[BlockTitle]:
        """
        Get block titles (id, title) with optional filtering.

        Args:
            client: Supabase client
            organization_id: Filter by organization ID
            types: Filter by block types (None = all types)
            published: Filter by published status
            limit: Max number of results
            offset: Pagination offset

        Returns:
            List of BlockTitle entities
        """
        query = client.table("prompt_blocks").select("id, title")

        if organization_id:
            query = query.eq("organization_id", organization_id)

        if types is not None and len(types) > 0:
            query = query.in_("type", types)

        if published is not None:
            query = query.eq("published", published)

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        blocks_data = response.data or []

        blocks = [BlockTitle(**item) for item in blocks_data]
        return blocks

    @staticmethod
    def get_block_by_id(client: Client, block_id: str) -> Block | None:
        response = client.table("prompt_blocks")\
            .select("*")\
            .eq("id", block_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return Block(
            id=data["id"],
            type=data["type"],
            title=data.get("title", {}),
            description=data.get("description"),
            content=data.get("content", {}),
            published=data.get("published", False),
            user_id=data["user_id"],
            organization_id=data.get("organization_id"),
            workspace_type=data.get("workspace_type", "user"),
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0)
        )

    @staticmethod
    def create_block(
        client: Client,
        user_id: str,
        block_type: str,
        title: dict[str, str],
        description: dict[str, str] | None,
        content: dict[str, str],
        published: bool,
        organization_id: str | None,
        workspace_type: str
    ) -> Block:
        block_data = {
            "user_id": user_id,
            "type": block_type,
            "title": title,
            "description": description,
            "content": content,
            "published": published,
            "organization_id": organization_id,
            "workspace_type": workspace_type
        }

        response = client.table("prompt_blocks").insert(block_data).execute()

        data = response.data[0]
        return Block(
            id=data["id"],
            type=data["type"],
            title=data.get("title", {}),
            description=data.get("description"),
            content=data.get("content", {}),
            published=data.get("published", False),
            user_id=data["user_id"],
            organization_id=data.get("organization_id"),
            workspace_type=data.get("workspace_type", "user"),
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0)
        )

    @staticmethod
    def update_block(
        client: Client,
        block_id: str,
        block_type: str | None = None,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        content: dict[str, str] | None = None,
        published: bool | None = None
    ) -> Block | None:
        update_data = {}
        if block_type is not None:
            update_data["type"] = block_type
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if content is not None:
            update_data["content"] = content
        if published is not None:
            update_data["published"] = published

        response = client.table("prompt_blocks")\
            .update(update_data)\
            .eq("id", block_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return Block(
            id=data["id"],
            type=data["type"],
            title=data.get("title", {}),
            description=data.get("description"),
            content=data.get("content", {}),
            published=data.get("published", False),
            user_id=data["user_id"],
            organization_id=data.get("organization_id"),
            workspace_type=data.get("workspace_type", "user"),
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0)
        )

    @staticmethod
    def delete_block(client: Client, block_id: str) -> bool:
        response = client.table("prompt_blocks").delete().eq("id", block_id).execute()
        return len(response.data or []) > 0

    @staticmethod
    def get_pinned_block_ids(client: Client, user_id: str) -> list[str]:
        response = client.table("users_metadata")\
            .select("pinned_block_ids")\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        if not response.data:
            return []

        pinned_ids = response.data.get("pinned_block_ids") or []
        return [str(bid) for bid in pinned_ids]

    @staticmethod
    def update_pinned_blocks(client: Client, user_id: str, block_ids: list[str]) -> list[str]:
        client.table("users_metadata")\
            .update({"pinned_block_ids": block_ids})\
            .eq("user_id", user_id)\
            .execute()

        return block_ids
