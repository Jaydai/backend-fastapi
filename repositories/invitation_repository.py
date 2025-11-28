from supabase import Client

from domains.entities import OrganizationInvitation


class InvitationRepository:
    @staticmethod
    def get_pending_invitations(client: Client, user_email: str) -> list[OrganizationInvitation]:
        response = (
            client.table("share_invitations")
            .select("id, invited_email, inviter_email, inviter_name, status, organization_id, metadata, created_at")
            .eq("invited_email", user_email)
            .eq("invitation_type", "organization")
            .eq("status", "pending")
            .execute()
        )

        invitations = []
        for row in response.data or []:
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

    @staticmethod
    def get_invitation_by_id(client: Client, invitation_id: str) -> OrganizationInvitation | None:
        response = (
            client.table("share_invitations")
            .select("id, invited_email, inviter_email, inviter_name, status, organization_id, metadata, created_at")
            .eq("id", invitation_id)
            .eq("invitation_type", "organization")
            .execute()
        )

        if not response.data or len(response.data) == 0:
            return None

        row = response.data[0]
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
            created_at=row.get("created_at"),
        )

    @staticmethod
    def update_invitation_status(
        client: Client, invitation: OrganizationInvitation, new_status: str
    ) -> OrganizationInvitation | None:
        update_response = (
            client.table("share_invitations").update({"status": new_status}).eq("id", invitation.id).execute()
        )

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
            created_at=row.get("created_at"),
        )
