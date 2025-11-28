"""
Configuration pytest pour les tests backend-fastapi
"""

import os
import uuid
from unittest.mock import patch

import dotenv
import pytest
from fastapi.testclient import TestClient
from supabase import Client, create_client

from tests.mocks import MockSupabaseClient

# Set testing mode BEFORE importing app
os.environ["TESTING_MODE"] = "true"

from main import app
from services import AuthService

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")


@pytest.fixture(scope="session")
def shared_test_storage():
    """Shared storage for mock Supabase data across tests"""
    return {}


@pytest.fixture(scope="session")
def supabase_admin(shared_test_storage) -> Client:
    """
    Client Supabase avec SERVICE ROLE pour les tests (bypass RLS)
    Falls back to mock client if Supabase is not available
    """
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        # Test connection
        client.table("users_metadata").select("user_id").limit(1).execute()
        print("✅ Connected to real Supabase for tests")
        return client
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to Supabase: {e}")
        print("⚠️ Tests will run in mock mode without real Supabase connection")
        return MockSupabaseClient(shared_test_storage)


@pytest.fixture
def mock_auth_service(shared_test_storage):
    """
    Mock AuthService to accept mock tokens and create_client to use service key
    """
    from supabase import create_client as original_create_client

    import middleware.auth_middleware

    original_get_current_user_id = AuthService.get_current_user_id

    def mock_get_current_user_id(access_token: str):
        """Mock version that accepts mock_token_* format"""
        if access_token and access_token.startswith("mock_token_"):
            return access_token.replace("mock_token_", "")
        return original_get_current_user_id(access_token)

    def mock_create_client_for_middleware(url, key, options=None):
        """When middleware creates authenticated client with mock token, use service key instead"""
        if options and hasattr(options, "headers"):
            auth_header = options.headers.get("Authorization", "")
            if "mock_token_" in auth_header:
                # Use service key instead of mock token for real Supabase
                return original_create_client(url, SUPABASE_SERVICE_KEY)
        return original_create_client(url, key, options)

    with (
        patch.object(AuthService, "get_current_user_id", side_effect=mock_get_current_user_id),
        patch.object(middleware.auth_middleware, "create_client", side_effect=mock_create_client_for_middleware),
    ):
        yield


@pytest.fixture(autouse=True)
def setup_auth_mock(mock_auth_service):
    """Automatically apply auth mocking to all tests"""
    pass


@pytest.fixture
def mock_supabase_client(shared_test_storage, supabase_admin):
    """
    Mock Supabase client for injecting into requests
    Only returns mock if real Supabase is not available
    """
    is_mock = isinstance(supabase_admin, MockSupabaseClient)
    if is_mock:
        return MockSupabaseClient(shared_test_storage)
    return None


@pytest.fixture(autouse=True)
def inject_mock_supabase(mock_supabase_client):
    """
    Inject mock Supabase client into core.supabase module for all tests
    Only if Supabase is not available (mock mode)
    """
    if mock_supabase_client is None:
        # Real Supabase is available, don't inject mock
        yield
        return

    import core.supabase

    # Store original (might be None in CI mode)
    original_supabase = getattr(core.supabase, "supabase", None)

    # Replace with mock using setattr (safe even if module attributes are restricted)
    core.supabase.supabase = mock_supabase_client

    yield

    # Restore original
    core.supabase.supabase = original_supabase


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

    # Check if using mock client
    is_mock = isinstance(supabase_admin, MockSupabaseClient)

    yield

    print("\n🧹 Cleaning up test database...")

    if is_mock:
        print("⚠️ Skipping cleanup - using mock Supabase")
        return

    try:
        # Clean up only test organizations and their resources
        # DO NOT delete vincent+1@jayd.ai user
        supabase_admin.table("organizations").delete().like("name", "Test Org%").execute()
        supabase_admin.table("user_organization_roles").delete().like("organization_id", "%").execute()

        # Clean up test data but preserve user metadata for vincent+1@jayd.ai
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
        # Check if using mock Supabase
        is_mock = isinstance(supabase_admin, MockSupabaseClient)

        if is_mock:
            # Mock mode - create mock user
            mock_user_id = user_id or str(uuid.uuid4())
            mock_token = f"mock_token_{mock_user_id}"

            # Store mock user metadata
            supabase_admin.table("users_metadata").insert(
                {
                    "user_id": mock_user_id,
                    "email": email or "test@example.com",
                    "name": "Test User",
                    "pinned_folder_ids": [],
                    "pinned_block_ids": [],
                    "pinned_template_ids": [],
                    "roles": {"organizations": {}},
                }
            ).execute()

            return (mock_user_id, mock_token)

        # Use existing test user instead of creating new ones
        email = "vincent+1@jayd.ai"
        password = "test1234"

        try:
            # Sign in with existing user
            sign_in_response = supabase_admin.auth.sign_in_with_password({"email": email, "password": password})

            if not sign_in_response.session or not sign_in_response.user:
                print("Warning: Failed to sign in test user")
                # Fallback to mock mode
                mock_user_id = str(uuid.uuid4())
                mock_token = f"mock_token_{mock_user_id}"
                return (mock_user_id, mock_token)

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
            # Fallback to mock mode
            mock_user_id = str(uuid.uuid4())
            mock_token = f"mock_token_{mock_user_id}"
            return (mock_user_id, mock_token)

    return _create_user


@pytest.fixture
def create_test_organization(supabase_admin: Client):
    """
    Factory fixture pour utiliser l'organisation existante de vincent+1@jayd.ai
    """

    def _create_org(org_id: str | None = None, org_name: str | None = None) -> str:
        # Use existing Jaydai organization for vincent+1@jayd.ai
        return "19864b30-936d-4a8d-996a-27d17f11f00f"

    return _create_org


@pytest.fixture
def assign_role(supabase_admin: Client):
    """
    Factory fixture pour assigner ou mettre à jour des rôles
    """

    def _assign_role(user_id: str, role: str, organization_id: str | None = None):
        # Check if using mock
        is_mock = isinstance(supabase_admin, MockSupabaseClient)

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
            if not is_mock:
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
