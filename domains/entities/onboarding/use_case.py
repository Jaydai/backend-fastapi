"""
Use Case Entity

Represents AI-generated use cases during onboarding.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class UseCase:
    """
    An AI use case generated during onboarding.

    Represents a potential way the user can leverage AI
    based on their role and organization.
    """

    title: str
    description: str
    category: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UseCase":
        """Create from dictionary."""
        return cls(
            title=data["title"],
            description=data["description"],
            category=data["category"],
        )
