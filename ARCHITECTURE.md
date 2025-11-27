# Backend Architecture

## Overview

The backend follows a clean layered architecture with clear separation of concerns:

```
Routes → Services → Repositories → Database
         ↓
    Permissions Service
```

## Directory Structure

```
backend-fastapi/
├── routes/               # HTTP endpoints
│   ├── templates/
│   ├── folders/
│   └── blocks/
├── services/            # Business logic
│   ├── permissions/     # Authorization logic
│   ├── templates/       # Template business logic
│   ├── folders/         # Folder business logic
│   └── blocks/          # Block business logic
├── repositories/        # Database operations
│   ├── templates/       # Template DB operations
│   ├── folders/         # Folder DB operations
│   └── blocks/          # Block DB operations
├── dtos/                # Data Transfer Objects
├── domains/             # Domain entities
└── mappers/             # Entity ↔ DTO conversions
```

## Layer Responsibilities

### 1. Routes Layer (`routes/`)

**Purpose**: Handle HTTP requests/responses

**Responsibilities**:
- Request validation
- Call appropriate services
- Format responses
- Error handling

**Example**:
```python
@router.get("", response_model=list[TemplateTitleResponseDTO])
async def get_all_templates(
    request: Request,
    organization_id: str | None = None,
    folder_ids: str | None = Query(None),
    published: bool | None = None
) -> list[TemplateTitleResponseDTO]:
    client = request.state.supabase_client
    locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

    # Parse query parameters
    folder_id_list = parse_folder_ids(folder_ids)

    # Call service
    templates = TemplateService.get_templates_titles(
        client,
        locale,
        organization_id,
        folder_id_list,
        published
    )

    return templates
```

### 2. Services Layer (`services/`)

**Purpose**: Business logic and orchestration

**Responsibilities**:
- Implement business rules
- Call repositories for data
- Use permission service for authorization
- Transform data between layers
- Localization

**Structure**:
- `services/permissions/` - Authorization logic
- `services/templates/` - Template business logic
  - `title_service.py` - List operations
  - More services for detail, version, etc. (future)
- `services/folders/` - Folder business logic
  - `title_service.py` - List operations
- `services/blocks/` - Block business logic
  - `title_service.py` - List operations

**Example**:
```python
class TemplateTitleService:
    @staticmethod
    def get_titles(
        client: Client,
        locale: str = LocaleService.DEFAULT_LOCALE,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        workspace_type: str | None = None
    ) -> list[TemplateTitleResponseDTO]:
        # Permission checks
        or_conditions = None
        if user_id and workspace_type:
            filter_result = UserPermissionsService.build_workspace_filter_conditions(
                client, user_id, workspace_type, organization_id
            )
            # Handle filter result...

        # Fetch from repository
        templates = TemplateBaseRepository.get_templates_titles(
            client,
            organization_id=organization_id,
            folder_ids=folder_ids,
            published=published,
            or_conditions=or_conditions
        )

        # Localize and return DTOs
        return [
            TemplateTitleResponseDTO(**localize_object(t.__dict__, locale, ["title"]))
            for t in templates
        ]
```

### 3. Repositories Layer (`repositories/`)

**Purpose**: Pure database operations

**Responsibilities**:
- Execute database queries
- Convert DB results to domain entities
- **NO** business logic
- **NO** permission checks
- **NO** validation (except DB-level)

**Structure**:
- `repositories/templates/`
  - `base_repository.py` - Core template DB operations
  - `version_repository.py` - Version DB operations
- `repositories/folders/`
  - `base_repository.py` - Folder DB operations
- `repositories/blocks/`
  - `base_repository.py` - Block DB operations

**Example**:
```python
class TemplateBaseRepository:
    @staticmethod
    def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        or_conditions: list[str] | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        """Pure database query - no permission checks"""
        query = client.table("prompt_templates").select("id, title")

        # Apply filters
        if or_conditions:
            query = query.or_(",".join(or_conditions))
        elif organization_id:
            query = query.eq("organization_id", organization_id)

        if folder_ids is not None:
            if len(folder_ids) == 0:
                query = query.is_("folder_id", "null")
            else:
                query = query.in_("folder_id", folder_ids)

        # Execute and return entities
        response = query.execute()
        return [TemplateTitle(**item) for item in response.data]
```

### 4. Permissions Service (`services/permissions/`)

**Purpose**: Centralize authorization logic

**Responsibilities**:
- Check user access to organizations
- Build workspace filter conditions
- Manage user metadata access

**Example**:
```python
class UserPermissionsService:
    @staticmethod
    def user_has_org_access(client: Client, user_id: str, organization_id: str) -> bool:
        """Check if user has access to organization"""
        org_ids = UserPermissionsService.get_user_organization_ids(client, user_id)
        return organization_id in org_ids

    @staticmethod
    def build_workspace_filter_conditions(
        client: Client,
        user_id: str,
        workspace_type: str | None = None,
        organization_id: str | None = None
    ) -> dict:
        """Build filter conditions for workspace queries"""
        # Returns structured filter conditions
        # e.g., {"type": "or", "conditions": [...]}
```

## Key Principles

### 1. Separation of Concerns

Each layer has a single, well-defined responsibility:
- **Routes**: HTTP handling
- **Services**: Business logic
- **Repositories**: Database access
- **Permissions**: Authorization

### 2. Pure Repositories

Repositories are pure database operations with **NO**:
- Business logic
- Permission checks
- User metadata lookups
- Complex transformations

They accept filter parameters and return domain entities.

### 3. Service Composition

Services can call:
- Repositories for data
- Permission service for authorization
- Other services for complex operations
- Mappers for transformations

### 4. Modularity

Large services are split into smaller, focused modules:
- `TemplateTitleService` - List operations
- `TemplateDetailService` - Detail operations (future)
- `TemplateVersionService` - Version operations (future)

### 5. Dependency Direction

```
Routes → Services → Repositories
         ↓
    Permissions Service
```

Dependencies only flow downward. No upward dependencies.

## Data Flow

### List Endpoint Flow

```
1. Route receives request
   ↓
2. Parse query parameters
   ↓
3. Call TitleService.get_titles()
   ├→ Permission check (if needed)
   ├→ Build filter conditions
   └→ Call Repository.get_titles()
      ↓
4. Repository executes DB query
   ↓
5. Return domain entities
   ↓
6. Service localizes and converts to DTOs
   ↓
7. Route returns DTOs
```

### Detail Endpoint Flow

```
1. Route receives request with ID
   ↓
2. Call Service.get_by_id()
   ├→ Permission check
   └→ Call Repository.get_by_id()
      ↓
3. Repository fetches entity
   ↓
4. Service enriches (versions, comments, etc.)
   ↓
5. Service converts to DTO
   ↓
6. Route returns DTO
```

## Benefits

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Clear responsibilities make code easier to understand
3. **Reusability**: Repositories and services can be reused across routes
4. **Flexibility**: Easy to add new routes or modify business logic
5. **Performance**: Can optimize at each layer independently

## Migration Guide

### Old Pattern (Don't Do This)

```python
# Repository with permission checks ❌
class TemplateRepository:
    @staticmethod
    def get_templates(client: Client, user_id: str, ...):
        # Get user metadata ❌
        user_metadata = get_user_metadata(client, user_id)

        # Permission checks ❌
        if organization_id not in user_metadata["roles"]:
            return []

        # Database query
        query = client.table("templates").select("*")
        ...
```

### New Pattern (Do This)

```python
# Pure repository ✅
class TemplateBaseRepository:
    @staticmethod
    def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        or_conditions: list[str] | None = None,
        ...
    ) -> list[TemplateTitle]:
        """Pure database operation"""
        query = client.table("templates").select("id, title")

        if or_conditions:
            query = query.or_(",".join(or_conditions))
        elif organization_id:
            query = query.eq("organization_id", organization_id)

        return [TemplateTitle(**item) for item in query.execute().data]

# Service with business logic ✅
class TemplateTitleService:
    @staticmethod
    def get_titles(
        client: Client,
        user_id: str,
        workspace_type: str,
        ...
    ) -> list[TemplateTitleResponseDTO]:
        # Permission checks in service ✅
        filter_result = UserPermissionsService.build_workspace_filter_conditions(
            client, user_id, workspace_type
        )

        # Call repository ✅
        templates = TemplateBaseRepository.get_templates_titles(
            client,
            or_conditions=filter_result.get("conditions")
        )

        # Localization ✅
        return [TemplateTitleResponseDTO(**localize_object(t)) for t in templates]
```

## Future Enhancements

1. Add detail services (`TemplateDetailService`, etc.)
2. Add mutation services (`TemplateCreateService`, `TemplateUpdateService`)
3. Add caching layer
4. Add event publishing
5. Add audit logging
