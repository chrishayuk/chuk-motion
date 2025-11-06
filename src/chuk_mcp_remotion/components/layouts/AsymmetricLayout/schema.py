# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/AsymmetricLayout/schema.py
"""AsymmetricLayout component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class AsymmetricLayoutProps(BaseModel):
    """Properties for AsymmetricLayout component."""

    main: Any | None = Field(None, description="Main content area")
    top_side: Any | None = Field(None, description="Top sidebar content")
    bottom_side: Any | None = Field(None, description="Bottom sidebar content")
    layout: str | None = Field(
        "main-left", description="Layout variant: main-left or main-right"
    )
    main_ratio: float | None = Field(
        66.67, description="Main content width (percentage, 0-100)"
    )
    gap: float | None = Field(20, description="Gap between panels (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="AsymmetricLayout",
    description="Main feed (2/3) + two demo panels (1/3 stacked) - perfect for tutorials",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Main feed (2/3) + two demo panels (1/3 stacked) - perfect for tutorials",
    "category": "layout",
    "schema": {
        "main": {"type": "component", "description": "Main content area"},
        "top_side": {"type": "component", "description": "Top sidebar content"},
        "bottom_side": {"type": "component", "description": "Bottom sidebar content"},
        "layout": {
            "type": "enum",
            "default": "main-left",
            "values": ["main-left", "main-right"],
            "description": "Layout variant",
        },
        "main_ratio": {
            "type": "number",
            "default": 66.67,
            "description": "Main content width (percentage, 0-100)",
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
        "main": {"type": "CodeBlock", "code": "// Main tutorial content"},
        "top_side": {"type": "CodeBlock", "code": "// Output"},
        "bottom_side": {"type": "CodeBlock", "code": "// Preview"},
        "layout": "main-left",
        "main_ratio": 66.67,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Code tutorials with output/preview",
            "Main content with supplementary panels",
            "Demo videos with multi-view",
            "Before/after comparisons",
        ],
    },
}
