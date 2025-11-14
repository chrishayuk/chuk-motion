# chuk-motion/src/chuk_motion/components/layouts/StackedReaction/schema.py
"""StackedReaction component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class StackedReactionProps(BaseModel):
    """Properties for StackedReaction component."""

    original_content: Any | None = Field(None, description="Original video/content")
    reaction_content: Any | None = Field(None, description="Reaction video")
    layout: str | None = Field("vertical", description="Layout: vertical, horizontal, pip")
    reaction_size: float | None = Field(40, description="Reaction panel size (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap between panels (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="StackedReaction",
    description="Reaction video style with stacked feeds",
    category="layout",
)


# MCP schema
MCP_SCHEMA = {
    "description": "Reaction video style with stacked feeds",
    "category": "layout",
    "schema": {
        "original_content": {"type": "component", "description": "Original video/content"},
        "reaction_content": {"type": "component", "description": "Reaction video"},
        "layout": {
            "type": "enum",
            "default": "vertical",
            "values": ["vertical", "horizontal", "pip"],
            "description": "Layout style",
        },
        "reaction_size": {
            "type": "number",
            "default": 40,
            "description": "Reaction panel size (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between panels (pixels)"},
        "padding": {
            "type": "number",
            "default": 40,
            "description": "Padding around layout (pixels)",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "original_content": {"type": "CodeBlock", "code": "// Original video"},
        "reaction_content": {"type": "CodeBlock", "code": "// Reaction"},
        "layout": "vertical",
        "reaction_size": 40,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Reaction videos",
            "Commentary videos",
            "Analysis content",
            "Review videos",
        ],
    },
}
