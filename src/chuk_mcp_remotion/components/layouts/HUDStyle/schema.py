# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/HUDStyle/schema.py
"""HUDStyle component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class HUDStyleProps(BaseModel):
    """Properties for HUDStyle component."""

    main_content: Any | None = Field(None, description="Main background content")
    top_left: Any | None = Field(None, description="Top-left overlay")
    top_right: Any | None = Field(None, description="Top-right overlay")
    bottom_left: Any | None = Field(None, description="Bottom-left overlay")
    bottom_right: Any | None = Field(None, description="Bottom-right overlay")
    center: Any | None = Field(None, description="Center overlay")
    overlay_size: float | None = Field(15, description="Corner overlay size (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap (pixels)")
    padding: float | None = Field(40, description="Padding (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="HUDStyle",
    description="Heads-up display style with overlay elements",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Heads-up display style with overlay elements",
    "category": "layout",
    "schema": {
        "main_content": {"type": "component", "description": "Main background content"},
        "top_left": {"type": "component", "description": "Top-left overlay"},
        "top_right": {"type": "component", "description": "Top-right overlay"},
        "bottom_left": {"type": "component", "description": "Bottom-left overlay"},
        "bottom_right": {"type": "component", "description": "Bottom-right overlay"},
        "center": {"type": "component", "description": "Center overlay"},
        "overlay_size": {"type": "number", "default": 15, "description": "Corner overlay size (%)"},
        "gap": {"type": "number", "default": 20, "description": "Gap (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
}
