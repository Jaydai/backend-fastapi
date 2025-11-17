"""
Configuration pytest pour les tests backend-fastapi
"""
import pytest
from typing import Generator
from core.supabase import supabase


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Setup et cleanup de la base de données de test
    """
    print("\n🔧 Setting up test database...")
    
    # Vous pouvez ajouter ici du setup global si nécessaire
    # Par exemple: créer des données de base, configurer des variables d'env, etc.
    
    yield
    
    # Cleanup après tous les tests
    print("\n🧹 Cleaning up test database...")
    
    # Supprimer toutes les données de test
    # Note: Adapter selon vos besoins
    try:
        # Supprimer les rôles de test
        supabase.table("user_organization_roles").delete().like("user_id", "%").execute()
        
        # Supprimer les templates de test
        supabase.table("prompt_templates").delete().like("id", "%").execute()
        
        # Supprimer les organisations de test
        supabase.table("organizations").delete().like("name", "Test Organization%").execute()
    except Exception as e:
        print(f"⚠️ Warning during cleanup: {e}")


@pytest.fixture(autouse=True)
def reset_database_between_tests():
    """
    Reset partiel de la DB entre chaque test pour isolation
    """
    yield
    
    # Cleanup après chaque test individuel si nécessaire
    # Cette partie est optionnelle selon vos besoins


@pytest.fixture
def authenticated_headers(access_token: str) -> dict:
    """Helper pour créer des headers d'authentification"""
    return {"Authorization": f"Bearer {access_token}"}
