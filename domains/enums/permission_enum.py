from enum import Enum


class PermissionEnum(str, Enum):
    ADMIN_SETTINGS = "admin:settings"

    COMMENT_CREATE = "comment:create"
    COMMENT_READ = "comment:read"
    COMMENT_UPDATE = "comment:update"
    COMMENT_DELETE = "comment:delete"

    TEMPLATE_CREATE = "template:create"
    TEMPLATE_READ = "template:read"
    TEMPLATE_UPDATE = "template:update"
    TEMPLATE_DELETE = "template:delete"

    BLOCK_CREATE = "block:create"
    BLOCK_READ = "block:read"
    BLOCK_UPDATE = "block:update"
    BLOCK_DELETE = "block:delete"

    # User management permissions
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    ORGANIZATION_CREATE = "organization:create"
    ORGANIZATION_READ = "organization:read"
    ORGANIZATION_UPDATE = "organization:update"
    ORGANIZATION_DELETE = "organization:delete"
