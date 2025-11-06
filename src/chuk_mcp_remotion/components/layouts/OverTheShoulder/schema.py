# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/OverTheShoulder/schema.py
"""OverTheShoulder component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class OverTheShoulderProps(BaseModel):
    """Properties for OverTheShoulder component."""

    screen_content: Any | None = Field(None, description="Main screen content")
    shoulder_overlay: Any | None = Field(None, description="Person/shoulder overlay")
    overlay_position: str | None = Field(
        "bottom-left", description="Position: bottom-left, bottom-right, top-left, top-right"
    )
    overlay_size: float | None = Field(30, description="Overlay size (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="OverTheShoulder",
    description="Looking over someone's shoulder perspective for screen recordings",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Looking over someone's shoulder perspective for screen recordings",
    "category": "layout",
    "schema": {
        "screen_content": {"type": "component", "description": "Main screen content"},
        "shoulder_overlay": {"type": "component", "description": "Person/shoulder overlay"},
        "overlay_position": {
            "type": "enum",
            "default": "bottom-left",
            "values": ["bottom-left", "bottom-right", "top-left", "top-right"],
            "description": "Overlay position",
        },
        "overlay_size": {"type": "number", "default": 30, "description": "Overlay size (percentage)"},
        "gap": {"type": "number", "default": 20, "description": "Gap (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "screen_content": {"type": "CodeBlock", "code": "// Screen"},
        "shoulder_overlay": {"type": "CodeBlock", "code": "// Person"},
        "overlay_position": "bottom-left",
        "overlay_size": 30,
        "start_time": 0.0,
        "duration": 10.0,
    },
}
