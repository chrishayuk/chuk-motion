# chuk-motion/src/chuk_motion/components/overlays/LowerThird/schema.py
"""LowerThird component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class LowerThirdProps(BaseModel):
    """Properties for LowerThird component."""

    name: str = Field(description="Main name/text (larger)")
    title: str | None = Field(None, description="Subtitle/title (smaller, below name)")
    variant: Any | None = Field("glass", description="Visual style")
    position: Any | None = Field("bottom_left", description="Screen position")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="LowerThird",
    description="Name plate overlay with title and subtitle (like TV graphics)",
    category="overlay",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Name plate overlay with title and subtitle (like TV graphics)",
    "category": "overlay",
    "variants": {
        "minimal": "Simple text on subtle background",
        "standard": "Text with clean bar background",
        "glass": "Glassmorphism effect with blur",
        "bold": "High contrast with accent colors",
        "animated": "Dynamic sliding animation",
    },
    "positions": {
        "bottom_left": "Bottom left corner (standard TV position)",
        "bottom_center": "Bottom center",
        "bottom_right": "Bottom right corner",
        "top_left": "Top left corner",
        "top_center": "Top center",
    },
    "schema": {
        "name": {"type": "string", "required": True, "description": "Main name/text (larger)"},
        "title": {
            "type": "string",
            "required": False,
            "description": "Subtitle/title (smaller, below name)",
        },
        "variant": {
            "type": "enum",
            "default": "glass",
            "values": ["minimal", "standard", "glass", "bold", "animated"],
            "description": "Visual style",
        },
        "position": {
            "type": "enum",
            "default": "bottom_left",
            "values": ["bottom_left", "bottom_center", "bottom_right", "top_left", "top_center"],
            "description": "Screen position",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "name": "Dr. Sarah Chen",
        "title": "AI Researcher, Stanford",
        "variant": "glass",
        "position": "bottom_left",
        "start_time": 2.0,
        "duration": 5.0,
    },
}
