from supabase import Client
from domains.entities import OrganizationInvitation


class InvitationRepository:
    @staticmethod
    def get_invitation_by_id(client: Client, invitation_id: str) -> OrganizationInvitation | None:
        response = client.table("share_invitations") \
            .select("id, invited_email, inviter_email, inviter_name, status, organization_id, metadata, created_at") \
            .eq("id", invitation_id) \
            .eq("invitation_type", "organization") \
            .single() \
            .execute()

        if not response.data:
            return None

        row = response.data
        metadata = row.get("metadata", {})

        return OrganizationInvitation(
            id=row["id"],
            invited_email=row["invited_email"],
            inviter_email=row["inviter_email"],
            inviter_name=row["inviter_name"],
            status=row["status"],
            organization_id=row["organization_id"],
            role=metadata.get("role", "viewer"),
            organization_name=metadata.get("organization_name"),
            created_at=row.get("created_at")
        )

    @staticmethod
    def accept_invitation(client: Client, invitation: OrganizationInvitation) -> OrganizationInvitation | None:
        update_response = client.table("share_invitations") \
            .update({"status": "accepted"}) \
            .eq("id", invitation.id) \
            .execute()

        if not update_response.data:
            return None

        row = update_response.data[0]
        updated_metadata = row.get("metadata", {})

        return OrganizationInvitation(
            id=row["id"],
            invited_email=row["invited_email"],
            inviter_email=row["inviter_email"],
            inviter_name=row["inviter_name"],
            status=row["status"],
            organization_id=row["organization_id"],
            role=updated_metadata.get("role", "viewer"),
            organization_name=updated_metadata.get("organization_name"),
            created_at=row.get("created_at")
        )

    @staticmethod
    def decline_invitation(client: Client, invitation: OrganizationInvitation) -> OrganizationInvitation | None:
        update_response = client.table("share_invitations") \
            .update({"status": "declined"}) \
            .eq("id", invitation.id) \
            .execute()

        if not update_response.data:
            return None

        row = update_response.data[0]
        metadata = row.get("metadata", {})

        return OrganizationInvitation(
            id=row["id"],
            invited_email=row["invited_email"],
            inviter_email=row["inviter_email"],
            inviter_name=row["inviter_name"],
            status=row["status"],
            organization_id=row["organization_id"],
            role=metadata.get("role", "viewer"),
            organization_name=metadata.get("organization_name"),
            created_at=row.get("created_at")
        )
