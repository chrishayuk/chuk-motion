# chuk-motion/src/chuk_motion/components/base.py
"""Base models for component system."""

from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel, Field


class ComponentMetadata(BaseModel):
    """Base metadata for all components."""

    name: str = Field(description="Component name")
    description: str = Field(description="Human-readable description")
    category: str = Field(description="Component category (chart, overlay, animation, etc.)")

    class Config:
        extra = "forbid"


class ComponentInfo(BaseModel):
    """Complete component information including metadata and functions."""

    metadata: ComponentMetadata
    template_path: Path | None = None
    register_tool: Callable | None = None
    add_to_composition: Callable | None = None
    directory_name: str | None = None  # Actual directory name (e.g., "overlays", "charts")

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"

    @property
    def name(self) -> str:
        """Get component name."""
        return self.metadata.name

    @property
    def category(self) -> str:
        """Get component category."""
        return self.metadata.category
