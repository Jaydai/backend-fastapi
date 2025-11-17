"""
Test Suite Simplifié: Cohérence Permissions DB ↔ Service Layer
===============================================================

Cette suite teste que les permissions au niveau service Python 
sont cohérentes avec les RLS policies SQL.

Scénarios testés:
- User dans une organisation SANS rôle global admin
- User dans une organisation AVEC rôle global admin  
- User dans plusieurs organizations en viewer
- User dans plusieurs organizations dont une seule en admin
"""

import pytest
from services import PermissionService
from domains.enums import RoleEnum, PermissionEnum
from supabase import create_client, Client
import os
import dotenv
import uuid

# Load .env pour obtenir les clés Supabase
dotenv.load_dotenv()

# Client Supabase avec SERVICE ROLE pour les tests (bypass RLS)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


class TestPermissionsServiceLayer:
    """Tests de cohérence permissions au niveau service"""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Setup des données de test pour chaque test"""
        self.org1_id = str(uuid.uuid4())
        self.org2_id = str(uuid.uuid4())
        self.org3_id = str(uuid.uuid4())
        
        # Créer les organisations via RPC (avec service_role key = bypass RLS)
        try:
            supabase_admin.rpc("create_test_organization", {"p_org_id": self.org1_id, "p_org_name": "Test Org 1"}).execute()
            supabase_admin.rpc("create_test_organization", {"p_org_id": self.org2_id, "p_org_name": "Test Org 2"}).execute()
            supabase_admin.rpc("create_test_organization", {"p_org_id": self.org3_id, "p_org_name": "Test Org 3"}).execute()
            print(f"✅ Created test organizations")
        except Exception as e:
            print(f"⚠️ Could not create organizations: {e}")
        
        yield
        
        # Cleanup après chaque test via RPC (avec service_role key = bypass RLS)
        try:
            supabase_admin.rpc("cleanup_test_data", {"p_org_ids": [self.org1_id, self.org2_id, self.org3_id]}).execute()
            print(f"✅ Cleaned up test data")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    
    def assign_role(self, user_id: str, role: RoleEnum, organization_id: str | None):
        """Helper pour assigner un rôle via RPC (avec service_role key = bypass RLS)"""
        try:
            # D'abord créer l'utilisateur s'il n'existe pas
            supabase_admin.rpc("create_test_user", {"p_user_id": user_id}).execute()
            
            # Puis assigner le rôle
            supabase_admin.rpc("create_test_user_role", {
                "p_user_id": user_id,
                "p_role": role.value,
                "p_organization_id": organization_id,
            }).execute()
            org_display = organization_id[:8] + "..." if organization_id else "GLOBAL"
            print(f"  ✅ Assigned {role.value} to user {user_id[:8]}... in org {org_display}")
        except Exception as e:
            print(f"  ⚠️ Could not assign role: {e}")
    
    
    # ========================================================================
    # SCÉNARIO 1: User viewer dans UNE organisation SANS admin global
    # ========================================================================
    
    def test_scenario_1_viewer_in_one_org(self):
        """
        ✅ SCÉNARIO 1: User viewer dans org1, SANS rôle global admin
        
        Comportement attendu:
        - ✅ Peut accéder aux ressources de son organisation (org1)
        - ✅ Peut accéder aux ressources globales (organization_id=NULL)
        - ❌ NE PEUT PAS accéder aux ressources d'autres organisations (org2, org3)
        - ❌ Permissions limitées selon le rôle viewer
        """
        print("\n" + "="*80)
        print("📋 SCÉNARIO 1: Viewer dans une organisation")
        print("="*80)
        
        user_id = str(uuid.uuid4())
        self.assign_role(user_id, RoleEnum.VIEWER, self.org1_id)
        
        # Test READ dans son org: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org1_id)
        print(f"\n  READ org1: {result}")
        assert result == True, "❌ Viewer devrait pouvoir lire dans son org"
        
        # Test READ dans autre org: NE DOIT PAS pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org2_id)
        print(f"  READ org2: {result}")
        assert result == False, "❌ Viewer ne devrait PAS pouvoir lire autre org"
        
        # Test READ ressource globale: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, None)
        print(f"  READ global: {result}")
        assert result == True, "❌ Viewer devrait pouvoir lire ressources globales"
        
        # Test CREATE dans son org: NE DOIT PAS pouvoir (viewer = lecture uniquement)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_CREATE, self.org1_id)
        print(f"  CREATE org1: {result}")
        assert result == False, "❌ Viewer ne devrait PAS pouvoir créer"
        
        print("\n✅ SCÉNARIO 1 PASS\n")
    
    
    # ========================================================================
    # SCÉNARIO 2: User avec rôle global admin
    # ========================================================================
    
    def test_scenario_2_global_admin(self):
        """
        ✅ SCÉNARIO 2: User avec rôle global admin (peut aussi avoir rôle dans org1)
        
        Comportement attendu:
        - ✅ Bypass complet - accès universel à TOUTES les organisations
        - ✅ Peut accéder aux ressources de org1, org2, org3
        - ✅ Peut accéder aux ressources globales
        - ✅ Admin global = permissions illimitées
        """
        print("\n" + "="*80)
        print("📋 SCÉNARIO 2: Admin global (bypass complet)")
        print("="*80)
        
        user_id = str(uuid.uuid4())
        self.assign_role(user_id, RoleEnum.ADMIN, organization_id=None)  # Admin global
        self.assign_role(user_id, RoleEnum.VIEWER, self.org1_id)  # Aussi viewer dans org1
        
        # Test: Vérifier que c'est bien un admin global
        is_admin = PermissionService.user_is_global_admin(user_id)
        print(f"\n  Is global admin: {is_admin}")
        assert is_admin == True, "❌ Devrait être admin global"
        
        # Test READ org1: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org1_id)
        print(f"  READ org1: {result}")
        assert result == True, "❌ Admin global devrait pouvoir lire org1"
        
        # Test READ org2 (pas de rôle org): DOIT pouvoir (fallback admin global)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org2_id)
        print(f"  READ org2: {result}")
        assert result == True, "❌ Admin global devrait pouvoir lire org2"
        
        # Test READ org3 (pas de rôle org): DOIT pouvoir (fallback admin global)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org3_id)
        print(f"  READ org3: {result}")
        assert result == True, "❌ Admin global devrait pouvoir lire org3"
        
        # Test DELETE org2 (permission haute): DOIT pouvoir (admin global bypass)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_DELETE, self.org2_id)
        print(f"  DELETE org2: {result}")
        assert result == True, "❌ Admin global devrait pouvoir supprimer partout"
        
        # Test READ global: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, None)
        print(f"  READ global: {result}")
        assert result == True, "❌ Admin global devrait pouvoir lire ressources globales"
        
        print("\n✅ SCÉNARIO 2 PASS\n")
    
    
    # ========================================================================
    # SCÉNARIO 3: User viewer dans PLUSIEURS organisations
    # ========================================================================
    
    def test_scenario_3_viewer_in_multiple_orgs(self):
        """
        ✅ SCÉNARIO 3: User viewer dans org1 ET org2
        
        Comportement attendu:
        - ✅ Peut accéder aux ressources de org1 et org2
        - ✅ Peut accéder aux ressources globales
        - ❌ NE PEUT PAS accéder aux ressources de org3 (pas membre)
        - ❌ Permissions viewer uniquement (lecture)
        """
        print("\n" + "="*80)
        print("📋 SCÉNARIO 3: Viewer dans plusieurs organisations")
        print("="*80)
        
        user_id = str(uuid.uuid4())
        self.assign_role(user_id, RoleEnum.VIEWER, self.org1_id)
        self.assign_role(user_id, RoleEnum.VIEWER, self.org2_id)
        
        # Test READ org1: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org1_id)
        print(f"\n  READ org1: {result}")
        assert result == True, "❌ Viewer devrait pouvoir lire org1"
        
        # Test READ org2: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org2_id)
        print(f"  READ org2: {result}")
        assert result == True, "❌ Viewer devrait pouvoir lire org2"
        
        # Test READ org3 (pas membre): NE DOIT PAS pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org3_id)
        print(f"  READ org3: {result}")
        assert result == False, "❌ Viewer ne devrait PAS pouvoir lire org3"
        
        # Test CREATE org1: NE DOIT PAS pouvoir (viewer uniquement)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_CREATE, self.org1_id)
        print(f"  CREATE org1: {result}")
        assert result == False, "❌ Viewer ne devrait PAS pouvoir créer"
        
        # Test READ global: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, None)
        print(f"  READ global: {result}")
        assert result == True, "❌ Viewer devrait pouvoir lire ressources globales"
        
        print("\n✅ SCÉNARIO 3 PASS\n")
    
    
    # ========================================================================
    # SCÉNARIO 4: User admin dans UNE org, viewer dans UNE AUTRE
    # ========================================================================
    
    def test_scenario_4_admin_in_one_viewer_in_another(self):
        """
        ✅ SCÉNARIO 4: User admin dans org1, viewer dans org2, rien dans org3
        
        Comportement attendu:
        - ✅ Peut TOUT faire dans org1 (admin)
        - ✅ Peut uniquement lire dans org2 (viewer)
        - ✅ Peut accéder aux ressources globales
        - ❌ NE PEUT PAS accéder à org3 (pas de rôle)
        - ❌ NE PEUT PAS créer/modifier/supprimer dans org2 (viewer)
        """
        print("\n" + "="*80)
        print("📋 SCÉNARIO 4: Admin dans org1, viewer dans org2")
        print("="*80)
        
        user_id = str(uuid.uuid4())
        self.assign_role(user_id, RoleEnum.ADMIN, self.org1_id)
        self.assign_role(user_id, RoleEnum.VIEWER, self.org2_id)
        
        # Test READ org1: DOIT pouvoir (admin)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org1_id)
        print(f"\n  READ org1: {result}")
        assert result == True, "❌ Admin org1 devrait pouvoir lire org1"
        
        # Test CREATE org1: DOIT pouvoir (admin)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_CREATE, self.org1_id)
        print(f"  CREATE org1: {result}")
        assert result == True, "❌ Admin org1 devrait pouvoir créer dans org1"
        
        # Test DELETE org1: DOIT pouvoir (admin)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_DELETE, self.org1_id)
        print(f"  DELETE org1: {result}")
        assert result == True, "❌ Admin org1 devrait pouvoir supprimer dans org1"
        
        # Test READ org2: DOIT pouvoir (viewer)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org2_id)
        print(f"  READ org2: {result}")
        assert result == True, "❌ Viewer org2 devrait pouvoir lire org2"
        
        # Test CREATE org2: NE DOIT PAS pouvoir (viewer uniquement)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_CREATE, self.org2_id)
        print(f"  CREATE org2: {result}")
        assert result == False, "❌ Viewer org2 ne devrait PAS pouvoir créer dans org2"
        
        # Test DELETE org2: NE DOIT PAS pouvoir (viewer uniquement)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_DELETE, self.org2_id)
        print(f"  DELETE org2: {result}")
        assert result == False, "❌ Viewer org2 ne devrait PAS pouvoir supprimer dans org2"
        
        # Test READ org3: NE DOIT PAS pouvoir (pas de rôle)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org3_id)
        print(f"  READ org3: {result}")
        assert result == False, "❌ Ne devrait PAS pouvoir lire org3"
        
        # Test READ global: DOIT pouvoir
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, None)
        print(f"  READ global: {result}")
        assert result == True, "❌ Devrait pouvoir lire ressources globales"
        
        print("\n✅ SCÉNARIO 4 PASS\n")
    
    
    # ========================================================================
    # EDGE CASE: User sans aucun rôle
    # ========================================================================
    
    def test_edge_case_no_role_can_access_global(self):
        """
        ✅ EDGE CASE: User SANS AUCUN rôle
        
        Comportement attendu:
        - ✅ Peut accéder aux ressources globales (organization_id=NULL)
        - ❌ NE PEUT PAS accéder aux ressources d'organisations
        """
        print("\n" + "="*80)
        print("📋 EDGE CASE: User sans rôle - ressources globales accessibles")
        print("="*80)
        
        user_id = str(uuid.uuid4())
        # Pas d'assignation de rôle
        
        # Test READ global: DOIT pouvoir (ressources globales accessibles à tous)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, None)
        print(f"\n  READ global: {result}")
        assert result == True, "❌ Ressources globales devraient être accessibles à tous"
        
        # Test READ org1: NE DOIT PAS pouvoir (pas de rôle)
        result = PermissionService.user_has_permission(user_id, PermissionEnum.TEMPLATE_READ, self.org1_id)
        print(f"  READ org1: {result}")
        assert result == False, "❌ User sans rôle ne devrait PAS accéder aux orgs"
        
        print("\n✅ EDGE CASE PASS\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
