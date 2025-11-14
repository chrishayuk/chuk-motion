# chuk-motion/src/chuk_motion/components/layouts/Mosaic/schema.py
"""Mosaic component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ClipConfig(BaseModel):
    """Configuration for a mosaic clip."""

    content: Any = Field(..., description="Clip content (component or element)")
    size: float | None = Field(None, description="Clip size (relative scale, e.g., 1.0, 1.5)")
    position: dict[str, float] | None = Field(None, description="Position override {x, y}")
    z_index: int | None = Field(None, description="Stack order (higher = front)")


class MosaicProps(BaseModel):
    """Properties for Mosaic component."""

    clips: list[ClipConfig] | None = Field(
        [], description="List of clip objects with {content, size, position, z_index}"
    )
    style: str | None = Field("hero-corners", description="Style: hero-corners, stacked, spotlight")
    gap: float | None = Field(10, description="Gap between clips (pixels)")
    padding: float | None = Field(40, description="Padding (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="Mosaic",
    description="Irregular collage with layered clips in various artistic arrangements",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Irregular collage with layered clips in various artistic arrangements",
    "category": "layout",
    "schema": {
        "clips": {
            "type": "array",
            "description": "Clip objects with {content, size, position, z_index}",
        },
        "style": {
            "type": "enum",
            "default": "hero-corners",
            "values": ["hero-corners", "stacked", "spotlight"],
            "description": "Mosaic style",
        },
        "gap": {"type": "number", "default": 10, "description": "Gap (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
}
