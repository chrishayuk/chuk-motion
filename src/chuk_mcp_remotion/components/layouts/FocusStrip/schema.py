# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/FocusStrip/schema.py
"""FocusStrip component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class FocusStripProps(BaseModel):
    """Properties for FocusStrip component."""

    main_content: Any | None = Field(None, description="Background/context content")
    focus_content: Any | None = Field(None, description="Focused strip content")
    position: str | None = Field("center", description="Position: top, center, bottom")
    strip_height: float | None = Field(30, description="Strip height (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="FocusStrip",
    description="Focused strip/banner layout for highlighting key content",
    category="layout",
)


# MCP schema
MCP_SCHEMA = {
    "description": "Focused strip/banner layout for highlighting key content",
    "category": "layout",
    "schema": {
        "main_content": {"type": "component", "description": "Background/context content"},
        "focus_content": {"type": "component", "description": "Focused strip content"},
        "position": {
            "type": "enum",
            "default": "center",
            "values": ["top", "center", "bottom"],
            "description": "Strip position",
        },
        "strip_height": {
            "type": "number",
            "default": 30,
            "description": "Strip height (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding around layout (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "main_content": {"type": "CodeBlock", "code": "// Background"},
        "focus_content": {"type": "CodeBlock", "code": "// Key message"},
        "position": "center",
        "strip_height": 30,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Caption overlays",
            "Quote highlights",
            "Code snippets",
            "Key message banners",
        ],
    },
}
