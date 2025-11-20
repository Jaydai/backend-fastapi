import pytest
from fastapi.testclient import TestClient
import uuid


class TestNotificationsEndpoints:

    def request(self, method, *args, **kwargs):
        """Helper to automatically include cookies in all requests"""
        if hasattr(self, 'cookies'):
            kwargs.setdefault('cookies', self.cookies)
        return getattr(self.client, method)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('post', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('patch', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('delete', *args, **kwargs)

    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin, create_test_user):
        self.user_id, access_token = create_test_user()

        self.client = test_client
        self.cookies = {"access_token": access_token}
        self.supabase_admin = supabase_admin
        self.notification_ids_to_cleanup = []

        yield

        # Cleanup notifications
        try:
            for notif_id in self.notification_ids_to_cleanup:
                supabase_admin.table("notifications").delete().eq("id", notif_id).execute()
        except Exception as e:
            print(f"Cleanup warning: {e}")

    def test_get_all_notifications_success(self):
        response = self.get("/notifications")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_all_notifications_with_filters(self):
        # Test with read filter
        response = self.get("/notifications?read=false")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_all_notifications_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/notifications")
        assert response.status_code in [401, 403]

    def test_get_notification_stats_success(self):
        response = self.get("/notifications/stats")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Should have count fields (API returns "total" and "unread")
        assert "unread" in data or "total" in data

    def test_get_notification_stats_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/notifications/stats")
        assert response.status_code in [401, 403]

    def test_mark_notification_as_read_not_found(self):
        fake_id = 99999  # Use integer ID instead of UUID
        response = self.patch(f"/notifications/{fake_id}", json={"read": True})
        assert response.status_code == 404

    def test_mark_notification_as_read_unauthorized(self):
        fake_id = 99999  # Use integer ID instead of UUID
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.patch(f"/notifications/{fake_id}", json={"read": True})
        assert response.status_code in [401, 403]

    def test_mark_all_as_read_success(self):
        response = self.patch("/notifications?mark_all_as_read=true")
        # Should succeed even if no notifications
        assert response.status_code in [200, 201]

    def test_mark_all_as_read_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.patch("/notifications?mark_all_as_read=true")
        assert response.status_code in [401, 403]

    def test_delete_notification_not_found(self):
        fake_id = 99999  # Use integer ID instead of UUID
        response = self.delete(f"/notifications/{fake_id}")
        assert response.status_code == 404

    def test_delete_notification_unauthorized(self):
        fake_id = 99999  # Use integer ID instead of UUID
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.delete(f"/notifications/{fake_id}")
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
