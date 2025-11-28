import uuid

import pytest


class TestAuthEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin):
        self.client = test_client
        self.supabase_admin = supabase_admin
        self.test_email = f"test-{uuid.uuid4().hex[:8]}@test.com"
        self.test_password = "TestPass123!"

        yield

        # Cleanup: try to delete test user if created
        try:
            # Find and delete test user
            users = supabase_admin.table("users_metadata").select("user_id").eq("email", self.test_email).execute()
            if users.data:
                for user in users.data:
                    try:
                        supabase_admin.auth.admin.delete_user(user["user_id"])
                    except Exception:
                        pass
                    supabase_admin.table("users_metadata").delete().eq("user_id", user["user_id"]).execute()
        except Exception as e:
            print(f"Cleanup warning: {e}")

    def test_sign_up_success(self):
        payload = {"email": self.test_email, "password": self.test_password, "first_name": "Test", "last_name": "User"}
        response = self.client.post("/auth/sign_up", json=payload)

        # Should return 201 or 200 depending on implementation
        assert response.status_code in [200, 201]

    def test_sign_up_missing_email(self):
        payload = {"password": self.test_password, "first_name": "Test", "last_name": "User"}
        response = self.client.post("/auth/sign_up", json=payload)
        assert response.status_code == 422

    def test_sign_up_missing_password(self):
        payload = {"email": self.test_email, "first_name": "Test", "last_name": "User"}
        response = self.client.post("/auth/sign_up", json=payload)
        assert response.status_code == 422

    def test_sign_up_weak_password(self):
        payload = {
            "email": self.test_email,
            "password": "123",  # Too weak
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post("/auth/sign_up", json=payload)
        # Might be 400 or 422 depending on validation
        assert response.status_code in [400, 422, 500]

    def test_sign_in_success(self):
        # Use existing user vincent+1@jayd.ai
        payload = {"email": "vincent+1@jayd.ai", "password": "test1234"}
        response = self.client.post("/auth/sign_in", json=payload)

        assert response.status_code == 200
        # Should set cookies
        assert "access_token" in response.cookies or "set-cookie" in response.headers

    def test_sign_in_wrong_password(self):
        payload = {"email": "vincent+1@jayd.ai", "password": "wrongpassword"}
        response = self.client.post("/auth/sign_in", json=payload)
        assert response.status_code in [400, 401, 403]

    def test_sign_in_nonexistent_user(self):
        payload = {"email": "nonexistent@example.com", "password": "password123"}
        response = self.client.post("/auth/sign_in", json=payload)
        assert response.status_code in [400, 401, 404]

    def test_sign_in_missing_email(self):
        payload = {"password": "password123"}
        response = self.client.post("/auth/sign_in", json=payload)
        assert response.status_code == 422

    def test_sign_out_success(self):
        # First sign in
        sign_in_response = self.client.post(
            "/auth/sign_in", json={"email": "vincent+1@jayd.ai", "password": "test1234"}
        )

        # Extract cookie values directly (secure cookies don't forward in TestClient)
        cookies = {
            "access_token": sign_in_response.cookies.get("access_token"),
            "refresh_token": sign_in_response.cookies.get("refresh_token"),
        }

        # Then sign out
        response = self.client.post("/auth/sign_out", cookies=cookies)
        assert response.status_code == 200

    def test_sign_out_without_auth(self):
        response = self.client.post("/auth/sign_out")
        # Might be 401 or might succeed with no-op
        assert response.status_code in [200, 401]

    def test_get_current_user_not_implemented(self):
        # This endpoint is marked as 501 Not Implemented
        response = self.client.get("/auth/me")
        assert response.status_code == 501

    def test_refresh_token_success(self):
        # Sign in first to get refresh token
        sign_in_response = self.client.post(
            "/auth/sign_in", json={"email": "vincent+1@jayd.ai", "password": "test1234"}
        )

        # Extract cookie values directly (secure cookies don't forward in TestClient)
        cookies = {
            "access_token": sign_in_response.cookies.get("access_token"),
            "refresh_token": sign_in_response.cookies.get("refresh_token"),
        }

        # Refresh token
        response = self.client.post("/auth/refresh", cookies=cookies)
        # Should return new tokens
        assert response.status_code in [200, 201]

    def test_refresh_token_without_token(self):
        response = self.client.post("/auth/refresh")
        assert response.status_code in [401, 403, 500]

    def test_oauth_sign_in_endpoint_exists(self):
        # Test OAuth endpoint exists
        response = self.client.post("/auth/oauth_sign_in", json={"provider": "google", "code": "test_code"})
        # Will fail without valid OAuth code, but endpoint should exist
        assert response.status_code in [400, 401, 422, 500]

    def test_forgot_password_not_implemented(self):
        # This endpoint is marked as 501 Not Implemented
        payload = {"email": "vincent+1@jayd.ai"}
        response = self.client.post("/auth/forgot-password", json=payload)
        assert response.status_code == 501

    def test_reset_password_not_implemented(self):
        # This endpoint is marked as 501 Not Implemented
        payload = {"token": "test_reset_token", "new_password": "NewPass123!"}
        response = self.client.post("/auth/reset-password", json=payload)
        assert response.status_code == 501


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
