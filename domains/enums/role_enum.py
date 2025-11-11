from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    WRITER = "writer"
    VIEWER = "viewer"
    GUEST = "guest"
