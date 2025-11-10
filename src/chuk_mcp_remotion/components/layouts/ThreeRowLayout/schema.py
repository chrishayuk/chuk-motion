# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeRowLayout/schema.py
"""ThreeRowLayout component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ThreeRowLayoutProps(BaseModel):
    """Properties for ThreeRowLayout component."""

    top: Any | None = Field(None, description="Content for top row")
    middle: Any | None = Field(None, description="Content for middle row")
    bottom: Any | None = Field(None, description="Content for bottom row")
    top_height: float | None = Field(25, description="Top row height (percentage, 0-100)")
    middle_height: float | None = Field(50, description="Middle row height (percentage, 0-100)")
    bottom_height: float | None = Field(25, description="Bottom row height (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap between rows (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="ThreeRowLayout",
    description="Header + Main + Footer arrangements with configurable heights",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Header + Main + Footer arrangements with configurable heights",
    "category": "layout",
    "schema": {
        "top": {"type": "component", "description": "Content for top row"},
        "middle": {"type": "component", "description": "Content for middle row"},
        "bottom": {"type": "component", "description": "Content for bottom row"},
        "top_height": {
            "type": "number",
            "default": 25,
            "description": "Top row height (percentage, 0-100)",
        },
        "middle_height": {
            "type": "number",
            "default": 50,
            "description": "Middle row height (percentage, 0-100)",
        },
        "bottom_height": {
            "type": "number",
            "default": 25,
            "description": "Bottom row height (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between rows (pixels)"},
        "padding": {
            "type": "number",
            "default": 40,
            "description": "Padding around layout (pixels)",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "top": {"type": "CodeBlock", "code": "// Header"},
        "middle": {"type": "CodeBlock", "code": "// Main content"},
        "bottom": {"type": "CodeBlock", "code": "// Footer"},
        "top_height": 25,
        "middle_height": 50,
        "bottom_height": 25,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "App with header and footer",
            "Dashboard with title bar",
            "Slides with header/footer",
            "Content with navigation bars",
        ],
    },
}
