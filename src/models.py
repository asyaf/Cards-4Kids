"""
Vehicle data model with Pydantic validation.
"""

import re
from pydantic import BaseModel, Field, field_validator


class Vehicle(BaseModel):
    """Represents a vehicle with multilingual names and styling info."""

    id: str = Field(description="Unique identifier (e.g., 'excavator')")
    english: str = Field(description="English display name")
    hebrew: str = Field(description="Hebrew translation")
    russian: str = Field(description="Russian translation")
    color: str = Field(description="Hex color code for styling")
    description: str = Field(default="", description="Detailed description for image generation")

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Ensure ID is lowercase with underscores only."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                f"ID must be lowercase letters, numbers, and underscores: {v}"
            )
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Ensure color is valid hex format."""
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError(f"Color must be hex format (#RRGGBB): {v}")
        return v.upper()

    @property
    def image_filename(self) -> str:
        """Get the expected image filename for this vehicle."""
        return f"{self.id}.png"

    @property
    def display_name(self) -> str:
        """Get the display name (English with spaces instead of underscores)."""
        return self.english
