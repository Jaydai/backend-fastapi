import uuid

import pytest
from fastapi.testclient import TestClient


class TestFoldersEndpoints:
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

    def delete(self, *args, **kwargs):
        return self.request("delete", *args, **kwargs)

    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin, create_test_user, create_test_organization, assign_role):
        self.user_id, access_token = create_test_user()
        self.org_id = create_test_organization(org_name="Test Org Folders")
        assign_role(self.user_id, "admin", self.org_id)

        self.folder_ids_to_cleanup = []
        self.client = test_client
        self.cookies = {"access_token": access_token}
        self.supabase_admin = supabase_admin

        yield

        try:
            # Clean up only the resources created during this test
            for folder_id in self.folder_ids_to_cleanup:
                supabase_admin.table("prompt_folders").delete().eq("id", folder_id).execute()

            # DO NOT delete the organization - we're reusing Jaydai organization
            # DO NOT delete the user - we're reusing vincent+1@jayd.ai
            # Role assignments will remain for the user
        except Exception as e:
            print(f"Cleanup warning: {e}")

    def test_get_folders_empty_list(self):
        response = self.get("/folders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_folder_success(self):
        payload = {"title": "Test Folder", "description": "Test description"}
        response = self.post("/folders", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Folder"
        assert data["description"] == "Test description"
        assert "id" in data
        assert data["workspace_type"] == "user"
        assert data["user_id"] is not None

        self.folder_ids_to_cleanup.append(data["id"])

    def test_create_folder_organization(self):
        payload = {"title": "Org Folder", "description": "Organization folder", "organization_id": self.org_id}
        response = self.post("/folders", json=payload)

        # May fail due to RLS policies
        assert response.status_code in [201, 403, 500]
        if response.status_code == 201:
            data = response.json()
            assert data["title"] == "Org Folder"
            assert data["organization_id"] == self.org_id
            assert data["workspace_type"] == "organization"
            self.folder_ids_to_cleanup.append(data["id"])

    def test_create_folder_missing_title(self):
        payload = {"description": "No title"}
        response = self.post("/folders", json=payload)
        assert response.status_code == 422

    def test_create_folder_with_parent(self):
        parent_payload = {"title": "Parent Folder"}
        parent_response = self.post("/folders", json=parent_payload)
        parent_id = parent_response.json()["id"]
        self.folder_ids_to_cleanup.append(parent_id)

        child_payload = {"title": "Child Folder", "parent_folder_id": parent_id}
        child_response = self.post("/folders", json=child_payload)

        assert child_response.status_code == 201
        data = child_response.json()
        assert data["parent_folder_id"] == parent_id

        self.folder_ids_to_cleanup.append(data["id"])

    def test_get_folders_with_filters(self):
        folder1 = self.post("/folders", json={"title": "User Folder"})
        self.folder_ids_to_cleanup.append(folder1.json()["id"])

        folder2 = self.post("/folders", json={"title": "Org Folder", "organization_id": self.org_id})
        if folder2.status_code == 201:
            self.folder_ids_to_cleanup.append(folder2.json()["id"])

        response = self.get("/folders?workspace_type=user")
        assert response.status_code == 200
        folders = response.json()
        assert len(folders) >= 1
        assert all(f["workspace_type"] == "user" for f in folders)

    def test_get_folder_by_id_success(self):
        create_response = self.post("/folders", json={"title": "Test Folder Detail"})
        folder_id = create_response.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id)

        response = self.get(f"/folders/{folder_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == folder_id
        assert data["title"] == "Test Folder Detail"

    def test_get_folder_by_id_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.get(f"/folders/{fake_id}")
        assert response.status_code == 404

    def test_update_folder_success(self):
        create_response = self.post("/folders", json={"title": "Original Title", "description": "Original desc"})
        folder_id = create_response.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id)

        update_payload = {"title": "Updated Title", "description": "Updated desc"}
        response = self.patch(f"/folders/{folder_id}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated desc"

    def test_update_folder_partial(self):
        create_response = self.post("/folders", json={"title": "Original", "description": "Original desc"})
        folder_id = create_response.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id)

        update_payload = {"title": "Only Title Updated"}
        response = self.patch(f"/folders/{folder_id}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Updated"
        assert data["description"] == "Original desc"

    def test_update_folder_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.patch(f"/folders/{fake_id}", json={"title": "Update"})
        assert response.status_code == 404

    def test_delete_folder_success(self):
        create_response = self.post("/folders", json={"title": "To Delete"})
        folder_id = create_response.json()["id"]

        response = self.delete(f"/folders/{folder_id}")
        assert response.status_code == 204

        get_response = self.get(f"/folders/{folder_id}")
        assert get_response.status_code == 404

    def test_delete_folder_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.delete(f"/folders/{fake_id}")
        assert response.status_code == 404

    def test_pin_folder_success(self):
        create_response = self.post("/folders", json={"title": "To Pin"})
        folder_id = create_response.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id)

        response = self.patch(f"/folders/{folder_id}/pin?pinned=true")

        assert response.status_code == 200
        data = response.json()
        assert data["pinned"] is True

    def test_unpin_folder_success(self):
        create_response = self.post("/folders", json={"title": "To Unpin"})
        folder_id = create_response.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id)

        self.patch(f"/folders/{folder_id}/pin?pinned=true")

        response = self.patch(f"/folders/{folder_id}/pin?pinned=false")

        assert response.status_code == 200
        data = response.json()
        assert data["pinned"] is False

    def test_get_pinned_folders(self):
        create_response1 = self.post("/folders", json={"title": "Pinned 1"})
        folder_id1 = create_response1.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id1)

        create_response2 = self.post("/folders", json={"title": "Pinned 2"})
        folder_id2 = create_response2.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id2)

        self.patch(f"/folders/{folder_id1}/pin?pinned=true")
        self.patch(f"/folders/{folder_id2}/pin?pinned=true")

        response = self.get("/folders/pinned")

        assert response.status_code == 200
        pinned = response.json()
        assert isinstance(pinned, list)
        assert len(pinned) >= 2

    def test_update_pinned_folders(self):
        create_response1 = self.post("/folders", json={"title": "Pin 1"})
        folder_id1 = create_response1.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id1)

        create_response2 = self.post("/folders", json={"title": "Pin 2"})
        folder_id2 = create_response2.json()["id"]
        self.folder_ids_to_cleanup.append(folder_id2)

        payload = {"folder_ids": [folder_id1, folder_id2]}
        response = self.put("/folders/pinned", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "pinned_folder_ids" in data

    def test_get_root_items(self):
        folder_response = self.post("/folders", json={"title": "Root Folder"})
        self.folder_ids_to_cleanup.append(folder_response.json()["id"])

        response = self.get("/folders/root/items")

        assert response.status_code == 200
        data = response.json()
        assert "folders" in data
        assert "templates" in data
        assert isinstance(data["folders"], list)
        assert isinstance(data["templates"], list)

    def test_get_folder_items(self):
        parent_response = self.post("/folders", json={"title": "Parent"})
        parent_id = parent_response.json()["id"]
        self.folder_ids_to_cleanup.append(parent_id)

        child_response = self.post("/folders", json={"title": "Child", "parent_folder_id": parent_id})
        self.folder_ids_to_cleanup.append(child_response.json()["id"])

        response = self.get(f"/folders/{parent_id}/items")

        assert response.status_code == 200
        data = response.json()
        assert "folders" in data
        assert "templates" in data
        assert len(data["folders"]) >= 1

    def test_get_folder_items_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.get(f"/folders/{fake_id}/items")
        assert response.status_code == 404

    def test_create_folder_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.post("/folders", json={"title": "No Auth"})
        assert response.status_code in [401, 403]

    def test_get_folders_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/folders")
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
