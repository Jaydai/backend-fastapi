"""Block repository - handles pure database operations for blocks"""

from supabase import Client

from domains.entities import Block, BlockTitle


class BlockBaseRepository:
    """Base repository for block database operations"""

    @staticmethod
    def get_blocks_titles(
        client: Client,
        organization_id: str | None = None,
        types: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        or_conditions: list[str] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[BlockTitle]:
        """
        Get block titles with filtering.
        Pure database operation - no permission checks.
        """
        query = client.table("prompt_blocks").select("id, title")

        # Apply OR conditions if provided (for workspace filters)
        if or_conditions:
            query = query.or_(",".join(or_conditions))
        elif organization_id:
            query = query.eq("organization_id", organization_id)
        elif user_id:
            query = query.eq("user_id", user_id).is_("organization_id", "null")

        # Type filtering
        if types is not None and len(types) > 0:
            query = query.in_("type", types)

        # Published filter
        if published is not None:
            query = query.eq("published", published)

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        blocks_data = response.data or []

        blocks = [BlockTitle(**item) for item in blocks_data]
        return blocks

    @staticmethod
    def get_block_by_id(client: Client, block_id: str) -> Block | None:
        """Get a single block by ID"""
        response = client.table("prompt_blocks").select("*").eq("id", block_id).execute()

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
            usage_count=data.get("usage_count", 0),
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
        workspace_type: str,
    ) -> Block:
        """Create a new block"""
        block_data = {
            "user_id": user_id,
            "type": block_type,
            "title": title,
            "description": description,
            "content": content,
            "published": published,
            "organization_id": organization_id,
            "workspace_type": workspace_type,
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
            usage_count=data.get("usage_count", 0),
        )

    @staticmethod
    def update_block(
        client: Client,
        block_id: str,
        block_type: str | None = None,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        content: dict[str, str] | None = None,
        published: bool | None = None,
    ) -> Block | None:
        """Update block fields"""
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

        response = client.table("prompt_blocks").update(update_data).eq("id", block_id).execute()

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
            usage_count=data.get("usage_count", 0),
        )

    @staticmethod
    def delete_block(client: Client, block_id: str) -> bool:
        """Delete a block"""
        response = client.table("prompt_blocks").delete().eq("id", block_id).execute()
        return len(response.data or []) > 0

    @staticmethod
    def get_pinned_block_ids(client: Client, user_id: str) -> list[str]:
        """Get list of pinned block IDs for a user"""
        response = client.table("users_metadata").select("pinned_block_ids").eq("user_id", user_id).single().execute()

        if not response.data:
            return []

        pinned_ids = response.data.get("pinned_block_ids") or []
        return [str(bid) for bid in pinned_ids]

    @staticmethod
    def update_pinned_blocks(client: Client, user_id: str, block_ids: list[str]) -> list[str]:
        """Update pinned blocks for a user"""
        client.table("users_metadata").update({"pinned_block_ids": block_ids}).eq("user_id", user_id).execute()

        return block_ids
