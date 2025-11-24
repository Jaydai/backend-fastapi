from domains.entities import (
    Organization,
    OrganizationDetail,
    OrganizationInvitation,
    OrganizationMember,
    UserOrganizationRole,
)
from supabase import Client


class OrganizationRepository:
    @staticmethod
    def get_organizations_with_roles(client: Client) -> list[Organization]:
        response = client.table("organizations").select("*, user_organization_roles(*)").execute()

        if not response.data:
            return []
        
        organizations = []
        for row in response.data:
            # Get the first available role
            user_org_role = None
            if row.get("user_organization_roles") and len(row["user_organization_roles"]) > 0:
                role_data = row["user_organization_roles"][0]
                if role_data:
                    user_org_role = UserOrganizationRole(
                        user_id=role_data["user_id"],
                        role=role_data["role"],
                        organization_id=role_data.get("organization_id"),
                    )
                else:
                    user_org_role = None  # None in case of a global Admin

            organizations.append(
                Organization(
                    id=row["id"],
                    name=row["name"],
                    user_organization_role=user_org_role,
                    type=row.get("type", "standard"),  # Default to standard if not set
                    image_url=row.get("image_url"),
                    banner_url=row.get("banner_url"),
                    created_at=row.get("created_at"),
                    website_url=row.get("website_url"),
                )
            )

        return organizations

    @staticmethod
    def get_organization_members(client: Client, organization_id: str) -> list[OrganizationMember]:
        # First, get all user_organization_roles for this organization
        response = (
            client.table("user_organization_roles")
            .select("user_id, role")
            .eq("organization_id", organization_id)
            .execute()
        )

        if not response.data:
            return []

        members = []
        for role_data in response.data:
            user_id = role_data["user_id"]

            # Fetch user metadata separately
            user_metadata_response = (
                client.table("users_metadata").select("email, name").eq("user_id", user_id).execute()
            )

            user_metadata = {}
            if user_metadata_response.data and len(user_metadata_response.data) > 0:
                user_metadata = user_metadata_response.data[0]

            members.append(
                OrganizationMember(
                    user_id=user_id,
                    email=user_metadata.get("email") or "",
                    role=role_data["role"],
                    first_name=user_metadata.get("name"),
                    last_name=None,
                )
            )

        return members

    @staticmethod
    def update_member_role(
        client: Client, organization_id: str, user_id: str, new_role: str
    ) -> OrganizationMember | None:
        response = (
            client.table("user_organization_roles")
            .update({"role": new_role})
            .eq("organization_id", organization_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data or len(response.data) == 0:
            return None

        user_metadata_response = (
            client.table("users_metadata").select("email, name").eq("user_id", user_id).single().execute()
        )

        user_metadata = user_metadata_response.data if user_metadata_response.data else {}

        return OrganizationMember(
            user_id=user_id,
            email=user_metadata.get("email") or "",
            role=new_role,
            first_name=user_metadata.get("name"),
            last_name=None,
        )

    @staticmethod
    def remove_member(client: Client, organization_id: str, user_id: str) -> bool:
        response = (
            client.table("user_organization_roles")
            .delete()
            .eq("organization_id", organization_id)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data is not None and len(response.data) > 0

    @staticmethod
    def get_organization_by_id(client: Client, organization_id: str) -> OrganizationDetail | None:
        org_response = client.table("organizations").select("*").eq("id", organization_id).execute()

        if not org_response.data or len(org_response.data) == 0:
            return None

        org_data = org_response.data[0]

        # Get current user's role in this organization
        current_user_role = None
        roles_response = (
            client.table("user_organization_roles")
            .select("role")
            .eq("organization_id", organization_id)
            .limit(1)
            .execute()
        )

        if roles_response.data and len(roles_response.data) > 0:
            current_user_role = roles_response.data[0]["role"]

        # Get all members using existing method
        members = OrganizationRepository.get_organization_members(client, organization_id)

        return OrganizationDetail(
            id=org_data["id"],
            name=org_data["name"],
            description=org_data.get("description"),
            type=org_data.get("type", "standard"),  # Default to standard if not set
            image_url=org_data.get("image_url"),
            banner_url=org_data.get("banner_url"),
            website_url=org_data.get("website_url"),
            created_at=org_data.get("created_at"),
            user_role=current_user_role,
            members=members,
        )

    @staticmethod
    def get_organization_invitations(client: Client, organization_id: str) -> list[OrganizationInvitation]:
        response = (
            client.table("share_invitations")
            .select("id, invited_email, inviter_email, inviter_name, status, organization_id, metadata, created_at")
            .eq("organization_id", organization_id)
            .eq("invitation_type", "organization")
            .eq("status", "pending")
            .order("created_at", desc=True)
            .execute()
        )

        if not response.data:
            return []

        invitations = []
        for row in response.data:
            metadata = row.get("metadata", {})
            invitations.append(
                OrganizationInvitation(
                    id=row["id"],
                    invited_email=row["invited_email"],
                    inviter_email=row["inviter_email"],
                    inviter_name=row["inviter_name"],
                    status=row["status"],
                    organization_id=row["organization_id"],
                    role=metadata.get("role", "viewer"),
                    organization_name=metadata.get("organization_name"),
                    created_at=row.get("created_at"),
                )
            )

        return invitations
