"""
Onboarding Block Entity

Represents AI-generated blocks during the onboarding chat flow.
These are simplified blocks used for onboarding, different from the main Block entity.
"""

from dataclasses import dataclass
from typing import Any, Literal

OnboardingBlockType = Literal["context", "role", "goal"]


@dataclass
class OnboardingBlock:
    """
    A block generated during onboarding.

    Used for context, role, and goal blocks that are created
    based on the user's job title and organization info.
    """

    id: str
    type: OnboardingBlockType
    title: str
    description: str
    icon: str | None = None
    category: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "icon": self.icon,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OnboardingBlock":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=data["type"],
            title=data["title"],
            description=data["description"],
            icon=data.get("icon"),
            category=data.get("category"),
        )
