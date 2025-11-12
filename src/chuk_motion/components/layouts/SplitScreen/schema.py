# chuk-motion/src/chuk_motion/components/layouts/SplitScreen/schema.py
"""SplitScreen component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class SplitScreenProps(BaseModel):
    """Properties for SplitScreen component."""

    orientation: Any | None = Field("horizontal", description="Split direction")
    layout: Any | None = Field("50-50", description="Size ratio")
    gap: float | None = Field(20, description="Gap between panels (pixels)")
    left_content: Any = Field(description="Component for left/top panel")
    right_content: Any = Field(description="Component for right/bottom panel")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="SplitScreen", description="Layout component for side-by-side content", category="layout"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Layout component for side-by-side content",
    "category": "layout",
    "layouts": {
        "50-50": "Equal split",
        "60-40": "Larger left side",
        "40-60": "Larger right side",
        "70-30": "Emphasis on left",
        "30-70": "Emphasis on right",
    },
    "orientations": {"horizontal": "Left and right panels", "vertical": "Top and bottom panels"},
    "schema": {
        "orientation": {
            "type": "enum",
            "default": "horizontal",
            "values": ["horizontal", "vertical"],
            "description": "Split direction",
        },
        "layout": {
            "type": "enum",
            "default": "50-50",
            "values": ["50-50", "60-40", "40-60", "70-30", "30-70"],
            "description": "Size ratio",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between panels (pixels)"},
        "left_content": {
            "type": "component",
            "required": True,
            "description": "Component for left/top panel",
        },
        "right_content": {
            "type": "component",
            "required": True,
            "description": "Component for right/bottom panel",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "orientation": "horizontal",
        "layout": "50-50",
        "gap": 20,
        "left_content": {"type": "CodeBlock", "code": "..."},
        "right_content": {"type": "Terminal", "output": "..."},
        "start_time": 0.0,
        "duration": 10.0,
    },
}
