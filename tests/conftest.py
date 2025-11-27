"""
Configuration pytest pour les tests backend-fastapi
"""

import os
import uuid

import dotenv
import pytest
from fastapi.testclient import TestClient
from supabase import Client, create_client

from main import app

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")


@pytest.fixture(scope="session")
def supabase_admin() -> Client:
    """
    Client Supabase avec SERVICE ROLE pour les tests (bypass RLS)
    """
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


@pytest.fixture
def test_client() -> TestClient:
    """
    TestClient FastAPI pour les tests d'endpoints
    """
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(supabase_admin: Client):
    """
    Setup et cleanup de la base de données de test
    """
    print("\n🔧 Setting up test database...")

    yield

    print("\n🧹 Cleaning up test database...")

    try:
        # Clean up only test organizations and their resources
        # DO NOT delete vincent@jayd.ai user
        supabase_admin.table("organizations").delete().like("name", "Test Org%").execute()
        supabase_admin.table("user_organization_roles").delete().like("organization_id", "%").execute()

        # Clean up test data but preserve user metadata for vincent@jayd.ai
        supabase_admin.table("prompt_folders").delete().like("title", "%").execute()
        supabase_admin.table("prompt_blocks").delete().like("title", "%").execute()
        supabase_admin.table("prompt_templates").delete().like("id", "%").execute()
    except Exception as e:
        print(f"⚠️ Warning during cleanup: {e}")


@pytest.fixture(autouse=True)
def reset_database_between_tests():
    """
    Reset partiel de la DB entre chaque test pour isolation
    """
    yield


@pytest.fixture
def test_user_id() -> str:
    """
    Génère un user_id de test unique
    """
    return str(uuid.uuid4())


@pytest.fixture
def test_org_id() -> str:
    """
    Génère un organization_id de test unique
    """
    return str(uuid.uuid4())


@pytest.fixture
def create_test_user(supabase_admin: Client):
    """
    Factory fixture pour se connecter avec l'utilisateur de test existant
    Returns tuple (user_id, access_token)
    """

    def _create_user(user_id: str | None = None, email: str | None = None) -> tuple[str, str]:
        # Use existing test user instead of creating new ones
        email = "vincent@jayd.ai"
        password = "test1234"

        try:
            # Sign in with existing user
            sign_in_response = supabase_admin.auth.sign_in_with_password({"email": email, "password": password})

            if not sign_in_response.session or not sign_in_response.user:
                print("Warning: Failed to sign in test user")
                return ("", "")

            created_user_id = sign_in_response.user.id
            access_token = sign_in_response.session.access_token

            # Ensure user_metadata exists
            existing = supabase_admin.table("users_metadata").select("*").eq("user_id", created_user_id).execute()

            if not existing.data:
                supabase_admin.table("users_metadata").insert(
                    {
                        "user_id": created_user_id,
                        "email": email,
                        "name": "Vincent Test",
                        "pinned_folder_ids": [],
                        "pinned_block_ids": [],
                        "pinned_template_ids": [],
                        "roles": {"organizations": {}},
                    }
                ).execute()

            return (created_user_id, access_token)
        except Exception as e:
            print(f"Warning signing in test user: {e}")
            return ("", "")

    return _create_user


@pytest.fixture
def create_test_organization(supabase_admin: Client):
    """
    Factory fixture pour utiliser l'organisation existante de vincent@jayd.ai
    """

    def _create_org(org_id: str | None = None, org_name: str | None = None) -> str:
        # Use existing Jaydai organization for vincent@jayd.ai
        return "19864b30-936d-4a8d-996a-27d17f11f00f"

    return _create_org


@pytest.fixture
def assign_role(supabase_admin: Client):
    """
    Factory fixture pour assigner ou mettre à jour des rôles
    """

    def _assign_role(user_id: str, role: str, organization_id: str | None = None):
        try:
            # Check if role already exists
            existing = (
                supabase_admin.table("user_organization_roles")
                .select("*")
                .eq("user_id", user_id)
                .eq("organization_id", organization_id)
                .execute()
            )

            if existing.data:
                # Update existing role
                supabase_admin.table("user_organization_roles").update({"role": role}).eq("user_id", user_id).eq(
                    "organization_id", organization_id
                ).execute()
            else:
                # Insert new role
                supabase_admin.table("user_organization_roles").insert(
                    {"user_id": user_id, "role": role, "organization_id": organization_id}
                ).execute()
        except Exception as e:
            print(f"Warning assigning role: {e}")

    return _assign_role


@pytest.fixture
def authenticated_headers(test_user_id: str) -> dict:
    """
    Headers d'authentification pour les tests
    """
    return {"Authorization": f"Bearer mock_token_{test_user_id}", "Accept-Language": "en"}


@pytest.fixture
def authenticated_client(test_client: TestClient, authenticated_headers: dict):
    """
    TestClient avec headers d'authentification pré-configurés
    """
    test_client.headers.update(authenticated_headers)
    return test_client
