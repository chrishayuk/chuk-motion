# chuk-motion/src/chuk_motion/components/overlays/TitleScene/schema.py
"""TitleScene component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TitleSceneProps(BaseModel):
    """Properties for TitleScene component."""

    text: str = Field(..., min_length=1, description="Main title text")
    subtitle: str | None = Field(None, min_length=1, description="Optional subtitle text")
    variant: Literal["minimal", "standard", "bold", "kinetic"] | None = Field(
        "standard", description="Visual style variant"
    )
    animation: Literal["fade_zoom", "slide_up", "typewriter", "blur_in", "split"] | None = Field(
        "fade_zoom", description="Animation style"
    )
    duration_seconds: float | None = Field(3.0, gt=0.0, description="Duration in seconds")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="TitleScene",
    description="Full-screen animated title card for video openings",
    category="scene",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Full-screen animated title card for video openings",
    "category": "scene",
    "variants": {
        "minimal": "Clean, simple text on solid background",
        "standard": "Text with gradient background",
        "bold": "Large text with animated gradient and effects",
        "kinetic": "Dynamic text with motion typography",
    },
    "animations": {
        "fade_zoom": "Fade in with subtle zoom",
        "slide_up": "Slide up from bottom with blur",
        "typewriter": "Character-by-character reveal",
        "blur_in": "Blur to sharp focus",
        "split": "Text splits from center",
    },
    "schema": {
        "text": {"type": "string", "required": True, "description": "Main title text"},
        "subtitle": {"type": "string", "required": False, "description": "Optional subtitle text"},
        "variant": {
            "type": "enum",
            "default": "standard",
            "values": ["minimal", "standard", "bold", "kinetic"],
            "description": "Visual style variant",
        },
        "animation": {
            "type": "enum",
            "default": "fade_zoom",
            "values": ["fade_zoom", "slide_up", "typewriter", "blur_in", "split"],
            "description": "Animation style",
        },
        "duration_seconds": {"type": "float", "default": 3.0, "description": "Duration in seconds"},
    },
    "example": {
        "text": "The Future of AI",
        "subtitle": "Transforming Technology",
        "variant": "bold",
        "animation": "fade_zoom",
        "duration_seconds": 3.0,
    },
}
