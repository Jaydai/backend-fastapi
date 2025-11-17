# Test Suite - Backend FastAPI Permissions

## 📋 Description

Cette suite de tests vérifie la **cohérence entre les permissions au niveau DB (RLS policies) et les endpoints FastAPI**.

## 🎯 Scénarios testés

### ✅ Scénario 1: User dans une organisation SANS rôle global admin
- **Rôle**: Viewer dans org1
- **Attendu**:
  - ✅ Peut lire templates de son organisation
  - ✅ Peut lire templates globaux
  - ❌ Ne peut PAS lire templates d'autres organisations
  - ❌ Ne peut PAS créer/modifier/supprimer

### ✅ Scénario 2: User avec rôle global admin
- **Rôle**: Admin global + Viewer dans org1
- **Attendu**:
  - ✅ Peut lire TOUS les templates (bypass complet)
  - ✅ Peut créer/modifier/supprimer dans TOUTES les organisations
  - ✅ Accès universel (fallback admin global)

### ✅ Scénario 3: User dans plusieurs organizations en viewer
- **Rôles**: Viewer dans org1 + Viewer dans org2
- **Attendu**:
  - ✅ Peut lire templates de org1 et org2
  - ✅ Peut lire templates globaux
  - ❌ Ne peut PAS lire templates de org3 (pas membre)
  - ❌ Ne peut PAS créer/modifier/supprimer

### ✅ Scénario 4: User admin dans une org, viewer dans une autre
- **Rôles**: Admin dans org1 + Viewer dans org2
- **Attendu**:
  - ✅ Peut TOUT faire dans org1 (admin)
  - ✅ Peut seulement lire dans org2 (viewer)
  - ✅ Peut lire templates globaux
  - ❌ Ne peut PAS lire org3 (pas de rôle)
  - ❌ Ne peut PAS créer/modifier/supprimer dans org2

## 🧪 Edge Cases testés

### 1. Ressources globales accessibles à tous
- Ressource avec `organization_id=NULL` ET `user_id=NULL`
- **Attendu**: Accessible même sans aucun rôle

### 2. Ressources globales non modifiables
- Ressource avec `user_id=NULL`
- **Attendu**: Lecture OK, modification/suppression interdite

### 3. Writer permissions
- **Attendu**: Peut créer et modifier dans son organisation

## 🚀 Exécution des tests

### Installation des dépendances
```bash
cd backend-fastapi
pip install -r requirements-tests.txt
```

### Lancer tous les tests
```bash
pytest tests/test_permissions_consistency.py -v -s
```

### Lancer un scénario spécifique
```bash
# Scénario 1 uniquement
pytest tests/test_permissions_consistency.py::TestPermissionsConsistency::test_scenario_1_viewer_in_one_org_no_global_admin -v -s

# Scénario 2 uniquement
pytest tests/test_permissions_consistency.py::TestPermissionsConsistency::test_scenario_2_user_in_org_with_global_admin -v -s

# Scénario 3 uniquement
pytest tests/test_permissions_consistency.py::TestPermissionsConsistency::test_scenario_3_viewer_in_multiple_orgs -v -s

# Scénario 4 uniquement
pytest tests/test_permissions_consistency.py::TestPermissionsConsistency::test_scenario_4_admin_in_one_org_viewer_in_others -v -s
```

### Lancer les edge cases
```bash
pytest tests/test_permissions_consistency.py::TestPermissionsEdgeCases -v -s
```

### Avec couverture de code
```bash
pytest tests/test_permissions_consistency.py --cov=services --cov=repositories --cov=routes --cov-report=html
```

## 📊 Résultats attendus

Tous les tests doivent passer ✅ pour confirmer que:
1. Les RLS policies SQL fonctionnent correctement
2. Les endpoints FastAPI respectent les mêmes règles
3. Le service de permissions Python est cohérent avec la DB
4. Les décorateurs appliquent correctement les vérifications

## 🔍 Debugging

Si un test échoue:
1. Vérifier les logs détaillés avec `-v -s`
2. Vérifier que les RLS policies sont à jour (`supabase db reset`)
3. Vérifier que `permission_service.py` applique la même logique que SQL
4. Comparer les permissions dans `PermissionEnum` vs `permission_type` en DB

## 📝 Notes importantes

- Les tests créent des utilisateurs, organisations et templates temporaires
- Le cleanup automatique supprime les données de test après exécution
- Les tests sont indépendants et peuvent être exécutés dans n'importe quel ordre
- La fixture `test_organizations` crée 3 organisations de test

## 🛠️ Maintenance

Quand ajouter de nouveaux tests:
- ✅ Nouvelle permission ajoutée
- ✅ Nouveau rôle créé
- ✅ Modification de la logique RLS
- ✅ Nouveau endpoint protégé par permissions
- ✅ Changement dans `user_has_permission()`

## 📚 Documentation liée

- `PERMISSIONS_RULES.md` - Règles de permissions complètes
- `PERMISSIONS_OPTIMIZATIONS.md` - Optimisations de performance
- `RLS_COHERENCE.md` - Cohérence RLS policies
- `supabase/migrations/20251113000000_admin_global_bypass.sql` - Fonction SQL principale
