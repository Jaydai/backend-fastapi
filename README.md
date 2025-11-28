# backend-fastapi

## Development

### Code Quality Tools

Ce projet utilise **Ruff** pour le linting et le formatage du code Python.

#### Vérifier le code (linting)

```bash
# Vérifier les erreurs de linting
ruff check .

# Appliquer les corrections automatiques
ruff check . --fix

# Appliquer les corrections y compris les unsafe-fixes
ruff check . --fix --unsafe-fixes
```

#### Formater le code

```bash
# Vérifier le formatage sans modifier les fichiers
ruff format --check .

# Appliquer le formatage
ruff format .
```

#### Exécuter les tests

Ce projet supporte deux modes de test :

**1. Mode local avec Supabase (recommandé pour développement)**
```bash
# Exécuter tous les tests avec connexion Supabase réelle
# Nécessite .env avec SUPABASE_URL et SUPABASE_SECRET_KEY
python3 -m pytest -v

# Exécuter un fichier de tests spécifique
python3 -m pytest tests/test_locale_service.py -v

# Exécuter les tests avec coverage
python3 -m pytest --cov=routes --cov=services --cov=repositories --cov=mappers
```

**2. Mode Mock (utilisé en CI, pas de connexion Supabase)**
```bash
# Exécuter les tests en mode mock uniquement (skip tests nécessitant Supabase)
# Pas besoin de .env, utilise des mocks
python3 -m pytest -c pytest.ci.ini tests/

# Les tests marqués @pytest.mark.requires_supabase seront skippés
```

**Markers de tests disponibles :**
- `@pytest.mark.requires_supabase` : Tests nécessitant une vraie connexion Supabase (skippés en CI)
- `@pytest.mark.integration` : Tests d'intégration nécessitant Supabase
- `@pytest.mark.slow` : Tests lents (peuvent être skippés avec `-m "not slow"`)

#### Workflow recommandé avant commit

```bash
# 1. Formater le code
ruff format .

# 2. Corriger les erreurs de linting
ruff check . --fix

# 3. Vérifier qu'il n'y a plus d'erreurs
ruff check .

# 4. Exécuter les tests
python3 -m pytest -v
```

## Supabase CLI troubleshooting

Running `supabase db pull` boots the local Supabase stack using the version
information cached under `supabase/.temp`. The cache currently records the
latest storage migration as `iceberg-catalog-ids` (`supabase/.temp/storage-migration:1`),
but the checked-in CLI binary (`supabase --version` → `2.54.11`) ships an older
storage image that does not include that migration. As a result the pull fails
with `StorageBackendError: Migration iceberg-catalog-ids not found`.

Update the Supabase CLI to `2.58.5` or later so the bundled storage service
knows about that migration:

```bash
brew update
brew upgrade supabase/tap/supabase
supabase --version  # expect >= 2.58.5
```

If the cache under `supabase/.temp` was created with the old binary, remove it so
the CLI refreshes the project metadata after upgrading:

```bash
rm -rf supabase/.temp
supabase login --profile supabase
```

Re-run `supabase db pull --debug` afterwards. The command should reach the
remote database and exit cleanly once the CLI and cached stack metadata are in
sync.
