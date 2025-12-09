from supabase import Client

from core.supabase import supabase_admin
from domains.entities import (
    Organization,
    OrganizationDetail,
    OrganizationInvitation,
    OrganizationMember,
    UserOrganizationRole,
)


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
        # Use admin client to bypass RLS - users can only see their own roles by default
        # but we need to see all members in the organization for the org dashboard
        admin_client = supabase_admin if supabase_admin else client

        # First, get all user_organization_roles for this organization
        response = (
            admin_client.table("user_organization_roles")
            .select("user_id, role")
            .eq("organization_id", organization_id)
            .execute()
        )

        if not response.data:
            return []

        members = []
        for role_data in response.data:
            user_id = role_data["user_id"]

            # Fetch user metadata separately (also using admin client for consistency)
            user_metadata_response = (
                admin_client.table("users_metadata").select("email, name").eq("user_id", user_id).execute()
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
    def create_organization(
        client: Client,
        user_id: str,
        name: str,
        description: str | None = None,
        image_url: str | None = None,
        website_url: str | None = None,
        org_type: str = "company",
    ) -> Organization:
        """
        Create a new organization and add the creator as admin.

        Returns the created Organization entity.
        """
        # Use admin client to bypass RLS for organization creation
        # This is a trusted server-side operation
        admin_client = supabase_admin if supabase_admin else client

        # Create the organization
        org_data = {
            "name": name,
            "type": org_type,
        }

        if description:
            org_data["description"] = {"text": description}
        if image_url:
            org_data["image_url"] = image_url
        if website_url:
            org_data["website_url"] = website_url

        org_response = admin_client.table("organizations").insert(org_data).execute()

        if not org_response.data or len(org_response.data) == 0:
            raise ValueError("Failed to create organization")

        org_row = org_response.data[0]
        org_id = org_row["id"]

        # Add creator as admin (using admin client to bypass RLS)
        role_data = {
            "user_id": user_id,
            "organization_id": org_id,
            "role": "admin",
        }

        role_response = admin_client.table("user_organization_roles").insert(role_data).execute()

        if not role_response.data:
            # Try to clean up the org if role creation failed
            admin_client.table("organizations").delete().eq("id", org_id).execute()
            raise ValueError("Failed to assign admin role to organization creator")

        return Organization(
            id=org_id,
            name=org_row["name"],
            type=org_row.get("type", "standard"),
            image_url=org_row.get("image_url"),
            banner_url=org_row.get("banner_url"),
            created_at=org_row.get("created_at"),
            website_url=org_row.get("website_url"),
            user_organization_role=UserOrganizationRole(
                user_id=user_id,
                organization_id=org_id,
                role="admin",
            ),
        )

    @staticmethod
    def create_invitation(
        client: Client,
        organization_id: str,
        organization_name: str,
        inviter_id: str,
        inviter_name: str,
        inviter_email: str,
        invited_email: str,
        role: str = "viewer",
    ) -> OrganizationInvitation:
        """
        Create an organization invitation.
        """
        # Use admin client to bypass RLS for invitation creation
        admin_client = supabase_admin if supabase_admin else client

        invitation_data = {
            "organization_id": organization_id,
            "invited_email": invited_email,
            "inviter_email": inviter_email,
            "inviter_name": inviter_name,
            "invitation_type": "organization",
            "status": "pending",
            "metadata": {
                "role": role,
                "organization_name": organization_name,
            },
        }

        response = admin_client.table("share_invitations").insert(invitation_data).execute()

        if not response.data or len(response.data) == 0:
            raise ValueError(f"Failed to create invitation for {invited_email}")

        row = response.data[0]
        return OrganizationInvitation(
            id=row["id"],
            invited_email=row["invited_email"],
            inviter_email=row["inviter_email"],
            inviter_name=row["inviter_name"],
            status=row["status"],
            organization_id=row["organization_id"],
            role=role,
            organization_name=organization_name,
            created_at=row.get("created_at"),
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
