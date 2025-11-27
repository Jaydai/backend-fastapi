# Backend FastAPI - Standards de développement

> Standards spécifiques au backend FastAPI de JayDAI

---

## Architecture du backend

### Structure du projet

```
backend-fastapi/
├── config/          → Configuration (settings, env)
├── core/            → Core business logic, clients (Supabase, OpenAI)
├── domains/         → Entités métier et enums
├── dtos/            → Data Transfer Objects (Pydantic models)
├── mappers/         → Conversion entre entités et DTOs
├── middleware/      → Middlewares (auth, CORS, etc.)
├── repositories/    → Accès base de données
├── routes/          → Endpoints API (controllers)
├── services/        → Logique métier
├── utils/           → Utilitaires
├── tests/           → Tests unitaires et d'intégration
└── main.py          → Point d'entrée de l'application
```

### Principes d'architecture

**Separation of Concerns :**
- **Routes** : Validation des inputs, appel des services, retour des réponses
- **Services** : Logique métier, orchestration
- **Repositories** : Accès base de données uniquement
- **Mappers** : Conversion entités ↔ DTOs

**Flux de données :**
```
Client → Route → Service → Repository → DB
                   ↓
                Mapper ← Entity
                   ↓
Client ← DTO ← Route
```

---

## Standards Python

### Type hints OBLIGATOIRES

**Tous les paramètres et retours doivent être typés :**

```python
# ✅ Correct
async def get_user_by_id(user_id: str) -> User | None:
    """Récupère un utilisateur par son ID."""
    ...

# ❌ Incorrect
async def get_user_by_id(user_id):  # Pas de types
    ...
```

**Types complexes :**
```python
from typing import Optional, List, Dict

async def get_users(
    filters: Dict[str, str],
    limit: int = 100
) -> List[User]:
    ...
```

### Async/Await pour I/O

**Toutes les opérations I/O doivent être async :**

```python
# ✅ Correct - Async pour DB
async def get_user(client, user_id: str) -> User:
    response = await client.from_("users").select("*").eq("id", user_id).execute()
    return response.data[0]

# ✅ Correct - Async pour API externes
async def enrich_message(message: str) -> str:
    response = await openai_client.chat.completions.create(...)
    return response.choices[0].message.content

# ❌ Incorrect - Bloquant
def get_user(client, user_id: str) -> User:
    response = client.from_("users").select("*").eq("id", user_id).execute()
    return response.data[0]
```

### Pydantic pour validation

**Tous les DTOs doivent être des Pydantic models :**

```python
from pydantic import BaseModel, Field, EmailStr, validator

class CreateUserRequest(BaseModel):
    """DTO pour création d'utilisateur."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=120)

    @validator("name")
    def validate_name(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("Name cannot have leading/trailing spaces")
        return v

class UserResponse(BaseModel):
    """DTO pour réponse utilisateur."""
    id: str
    email: str
    name: str
    created_at: str

    class Config:
        from_attributes = True  # Permet conversion depuis ORM
```

---

## Structure des routes

### Organisation

**Une route = un fichier dans un dossier thématique :**

```
routes/
├── __init__.py          → Router principal
├── auth/                → Routes d'authentification
│   ├── __init__.py
│   ├── sign_in.py
│   └── sign_up.py
├── users/               → Routes utilisateurs
│   ├── __init__.py
│   ├── get_by_id.py
│   ├── list.py
│   └── update.py
└── blocks/              → Routes blocks
    ├── __init__.py
    ├── create.py
    └── delete.py
```

### Template d'une route

```python
"""
Route : GET /users/{user_id}
Récupère un utilisateur par son ID.
"""
from fastapi import Request, HTTPException, status
from routes.users import router
from services import UserService
from dtos import UserResponse

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(request: Request, user_id: str) -> UserResponse:
    """
    Récupère un utilisateur par son ID.

    Args:
        request: FastAPI request (contient user_id, supabase_client via middleware)
        user_id: UUID de l'utilisateur

    Returns:
        UserResponse: Données de l'utilisateur

    Raises:
        HTTPException 404: Utilisateur non trouvé
        HTTPException 403: Pas de permission
    """
    # Récupérer client et user authentifié depuis middleware
    client = request.state.supabase_client
    current_user_id = request.state.user_id

    # Appeler le service
    user = await UserService.get_by_id(client, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    # Vérifier permissions (exemple)
    if user.id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's data"
        )

    return UserResponse.from_entity(user)
```

---

## Services

### Responsabilités

**Services = logique métier uniquement :**
- Orchestration de plusieurs repositories
- Validation métier complexe
- Transformations de données
- Gestion des transactions

**Services NE font PAS :**
- ❌ Accès direct à la DB (utiliser repositories)
- ❌ Validation de format (utiliser Pydantic)
- ❌ Gestion HTTP (codes, headers) → ça reste dans les routes

### Template d'un service

```python
"""
Service de gestion des utilisateurs.
Contient la logique métier liée aux utilisateurs.
"""
from typing import Optional
from domains.entities import User
from repositories import UserRepository
from core.supabase import Client

class UserService:
    """Service pour opérations sur les utilisateurs."""

    @staticmethod
    async def get_by_id(client: Client, user_id: str) -> Optional[User]:
        """
        Récupère un utilisateur par ID.

        Args:
            client: Client Supabase authentifié
            user_id: UUID de l'utilisateur

        Returns:
            User si trouvé, None sinon
        """
        return await UserRepository.get_by_id(client, user_id)

    @staticmethod
    async def create_user(
        client: Client,
        email: str,
        name: str
    ) -> User:
        """
        Crée un nouvel utilisateur.

        Args:
            client: Client Supabase authentifié
            email: Email de l'utilisateur
            name: Nom de l'utilisateur

        Returns:
            User créé

        Raises:
            ValueError: Si email déjà existant
        """
        # Logique métier : vérifier unicité
        existing = await UserRepository.get_by_email(client, email)
        if existing:
            raise ValueError(f"User with email {email} already exists")

        # Créer l'utilisateur
        user = await UserRepository.create(client, {
            "email": email,
            "name": name
        })

        # Logique métier : envoyer email de bienvenue
        await EmailService.send_welcome_email(email, name)

        return user
```

---

## Repositories

### Responsabilités

**Repositories = accès DB uniquement :**
- Requêtes Supabase
- Mapping DB → Entities
- AUCUNE logique métier

### Template d'un repository

```python
"""
Repository pour accès aux utilisateurs en DB.
"""
from typing import Optional, List
from domains.entities import User
from core.supabase import Client

class UserRepository:
    """Repository pour la table users."""

    TABLE = "users"

    @staticmethod
    async def get_by_id(client: Client, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par ID."""
        response = await client.from_(UserRepository.TABLE)\
            .select("*")\
            .eq("id", user_id)\
            .execute()

        if not response.data:
            return None

        return User(**response.data[0])

    @staticmethod
    async def list_all(client: Client, limit: int = 100) -> List[User]:
        """Liste tous les utilisateurs (paginé)."""
        response = await client.from_(UserRepository.TABLE)\
            .select("*")\
            .limit(limit)\
            .execute()

        return [User(**row) for row in response.data]

    @staticmethod
    async def create(client: Client, data: dict) -> User:
        """Crée un nouvel utilisateur."""
        response = await client.from_(UserRepository.TABLE)\
            .insert(data)\
            .execute()

        return User(**response.data[0])

    @staticmethod
    async def update(client: Client, user_id: str, data: dict) -> User:
        """Met à jour un utilisateur."""
        response = await client.from_(UserRepository.TABLE)\
            .update(data)\
            .eq("id", user_id)\
            .execute()

        return User(**response.data[0])

    @staticmethod
    async def delete(client: Client, user_id: str) -> None:
        """Supprime un utilisateur."""
        await client.from_(UserRepository.TABLE)\
            .delete()\
            .eq("id", user_id)\
            .execute()
```

---

## Tests

### Structure des tests

```
tests/
├── unit/              → Tests unitaires (services, utils)
├── integration/       → Tests d'intégration (API + DB)
├── fixtures/          → Fixtures pytest
└── conftest.py        → Configuration pytest
```

### Tests unitaires (services)

```python
"""Tests pour UserService."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from services import UserService
from domains.entities import User

@pytest.mark.asyncio
async def test_get_by_id_returns_user():
    """Test : get_by_id retourne l'utilisateur si trouvé."""
    # Arrange
    client = MagicMock()
    user_id = "user-123"
    expected_user = User(id=user_id, email="test@example.com", name="Test")

    # Mock du repository
    with patch('repositories.UserRepository.get_by_id', new_callable=AsyncMock) as mock:
        mock.return_value = expected_user

        # Act
        result = await UserService.get_by_id(client, user_id)

        # Assert
        assert result == expected_user
        mock.assert_called_once_with(client, user_id)

@pytest.mark.asyncio
async def test_create_user_raises_if_email_exists():
    """Test : create_user lève ValueError si email existe déjà."""
    # Arrange
    client = MagicMock()
    email = "existing@example.com"

    with patch('repositories.UserRepository.get_by_email', new_callable=AsyncMock) as mock:
        mock.return_value = User(id="123", email=email, name="Existing")

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            await UserService.create_user(client, email, "Test")
```

### Tests d'intégration (API)

```python
"""Tests d'intégration pour routes utilisateurs."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user_returns_200_if_exists():
    """Test : GET /users/{id} retourne 200 si utilisateur existe."""
    # Arrange
    user_id = "user-123"
    headers = {"Authorization": "Bearer valid_token"}

    # Act
    response = client.get(f"/users/{user_id}", headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_get_user_returns_404_if_not_found():
    """Test : GET /users/{id} retourne 404 si non trouvé."""
    # Arrange
    user_id = "nonexistent"
    headers = {"Authorization": "Bearer valid_token"}

    # Act
    response = client.get(f"/users/{user_id}", headers=headers)

    # Assert
    assert response.status_code == 404
```

### Exécution des tests

```bash
# Tous les tests
pytest

# Avec coverage
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/unit/services/test_user_service.py

# Mode verbose
pytest -v

# Arrêter au premier échec
pytest -x
```

---

## Variables d'environnement

### Fichier .env (jamais commité)

```bash
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# OpenAI
OPENAI_API_KEY=sk-xxx

# Environment
ENVIRONMENT=local  # local, dev, prod
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# App
APP_VERSION=1.0.0
```

### Chargement dans le code

```python
"""Configuration de l'application."""
from pydantic_settings import BaseSettings
from enum import Enum

class Environment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"

class Settings(BaseSettings):
    """Settings de l'application."""
    SUPABASE_URL: str
    SUPABASE_KEY: str
    OPENAI_API_KEY: str
    ENVIRONMENT: Environment = Environment.LOCAL
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Logging

### Configuration

```python
import logging

# Configuration globale
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Usage dans le code

```python
# Dans un service
logger.info(f"Creating user with email: {email}")
logger.warning(f"User {user_id} not found")
logger.error(f"Failed to create user: {str(e)}")

# Jamais de print() en production
# ❌ print("User created")  # NON
# ✅ logger.info("User created")  # OUI
```

---

## Formatage et linting

### Black (formatage)

```bash
# Formatter tout le projet
black .

# Vérifier sans modifier
black --check .

# Configuration dans pyproject.toml
[tool.black]
line-length = 100
target-version = ['py310']
```

### Ruff (linting)

```bash
# Linter
ruff check .

# Auto-fix
ruff check --fix .

# Configuration dans pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I"]  # Erreurs, F-strings, imports
```

### Pre-commit (recommandé)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff
```

---

## Commandes utiles

```bash
# Développement
uvicorn main:app --reload --port 8000

# Tests
pytest
pytest --cov=. --cov-report=html

# Linting
black .
ruff check --fix .

# Type checking (optionnel)
mypy .

# Dépendances
pip install -r requirements.txt
pip freeze > requirements.txt
```

---

## Questions fréquentes

### Dois-je typer tous les paramètres ?

**Oui, absolument.** Type hints obligatoires partout.

### Quand utiliser async/await ?

**Toutes les opérations I/O :**
- Requêtes DB (Supabase)
- Appels API externes (OpenAI, etc.)
- Lecture/écriture fichiers
- Network requests

### Où mettre la validation métier ?

**Dans les services**, pas dans les routes.
- Routes : Validation de format (Pydantic)
- Services : Validation métier (unicité, règles business)

### Quelle est la différence entre Entity et DTO ?

**Entity** : Représentation interne (domaine métier)
**DTO** : Représentation externe (API, requests/responses)

Mapper entre les deux pour isolation.

---

**Dernière mise à jour** : 2025-11-27
**Version** : 2.0 (Backend-specific)
**Référence globale** : `~/.claude/CLAUDE.md`
