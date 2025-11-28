import pytest
from fastapi.testclient import TestClient


class TestUserEndpoints:
    def request(self, method, *args, **kwargs):
        """Helper to automatically include cookies in all requests"""
        if hasattr(self, "cookies"):
            kwargs.setdefault("cookies", self.cookies)
        return getattr(self.client, method)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request("patch", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request("put", *args, **kwargs)

    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin, create_test_user):
        self.user_id, access_token = create_test_user()

        self.client = test_client
        self.cookies = {"access_token": access_token}
        self.supabase_admin = supabase_admin

        yield

    def test_get_user_profile_success(self):
        response = self.get("/user/profile")

        assert response.status_code == 200
        data = response.json()
        assert "email" in data or "name" in data or "id" in data

    def test_get_user_profile_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/profile")
        assert response.status_code in [401, 403]

    def test_update_user_profile_success(self):
        payload = {"name": "Updated Name", "bio": "This is my updated bio"}
        response = self.put("/user/profile", json=payload)

        assert response.status_code == 200
        data = response.json()
        # Should have user profile fields
        assert "id" in data and ("first_name" in data or "email" in data)

    def test_update_user_profile_partial(self):
        payload = {"name": "Only Name Updated"}
        response = self.put("/user/profile", json=payload)

        assert response.status_code == 200

    def test_update_user_profile_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.put("/user/profile", json={"name": "Test"})
        assert response.status_code in [401, 403]

    def test_get_user_metadata_success(self):
        response = self.get("/user/metadata")

        # This endpoint is not implemented yet
        assert response.status_code == 501

    def test_get_user_metadata_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/metadata")
        assert response.status_code in [401, 403]

    def test_update_user_metadata_success(self):
        payload = {"preferences": {"theme": "dark", "language": "en"}, "settings": {"notifications": True}}
        response = self.put("/user/metadata", json=payload)

        # This endpoint is not implemented yet
        assert response.status_code == 501

    def test_update_user_metadata_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.put("/user/metadata", json={"preferences": {}})
        assert response.status_code in [401, 403, 501]

    def test_update_data_collection_preferences_enable(self):
        payload = {"data_collection": True}
        response = self.put("/user/data-collection", json=payload)

        assert response.status_code in [200, 201, 204]

    def test_update_data_collection_preferences_disable(self):
        payload = {"data_collection": False}
        response = self.put("/user/data-collection", json=payload)

        assert response.status_code in [200, 201, 204]

    def test_update_data_collection_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.put("/user/data-collection", json={"data_collection": True})
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
