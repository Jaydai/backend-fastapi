from supabase import Client


class UserPermissionsService:
    """Service to handle user permissions and access checks"""

    @staticmethod
    def get_user_metadata(client: Client, user_id: str) -> dict:
        """Get user metadata including organization roles"""
        response = client.table("users_metadata").select("*").eq("user_id", user_id).single().execute()

        if not response.data:
            return {"organization_ids": [], "roles": {}}

        return response.data

    @staticmethod
    def get_user_organization_ids(client: Client, user_id: str) -> list[str]:
        """Get list of organization IDs the user has access to"""
        user_metadata = UserPermissionsService.get_user_metadata(client, user_id)
        roles = user_metadata.get("roles") or {}
        org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}
        return list(org_roles.keys())

    @staticmethod
    def user_has_org_access(client: Client, user_id: str, organization_id: str) -> bool:
        """Check if user has access to a specific organization"""
        org_ids = UserPermissionsService.get_user_organization_ids(client, user_id)
        return organization_id in org_ids

    @staticmethod
    def build_workspace_filter_conditions(
        client: Client, user_id: str, workspace_type: str | None = None, organization_id: str | None = None
    ) -> dict:
        """
        Build filter conditions for workspace-based queries.

        Returns:
            dict with either:
            - {"type": "or", "conditions": [...]} for OR conditions
            - {"type": "user"} for user-only filter
            - {"type": "organization", "org_id": str} for single org filter
            - {"type": "organizations", "org_ids": []} for multiple orgs filter
            - {"type": "none"} for no results
        """
        if organization_id:
            # Check access
            if not UserPermissionsService.user_has_org_access(client, user_id, organization_id):
                return {"type": "none"}
            return {"type": "organization", "org_id": organization_id}

        if workspace_type == "user":
            return {"type": "user"}

        if workspace_type == "organization":
            org_ids = UserPermissionsService.get_user_organization_ids(client, user_id)
            if not org_ids:
                return {"type": "none"}
            return {"type": "organizations", "org_ids": org_ids}

        # Default or "all": user + all their organizations
        org_ids = UserPermissionsService.get_user_organization_ids(client, user_id)
        conditions = [f"user_id.eq.{user_id}"]
        for org_id in org_ids:
            conditions.append(f"organization_id.eq.{org_id}")

        return {"type": "or", "conditions": conditions}
