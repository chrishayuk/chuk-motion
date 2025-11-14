# chuk-motion/src/chuk_motion/components/layouts/ThreeColumnLayout/schema.py
"""ThreeColumnLayout component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ThreeColumnLayoutProps(BaseModel):
    """Properties for ThreeColumnLayout component."""

    left: Any | None = Field(None, description="Content for left column")
    center: Any | None = Field(None, description="Content for center column")
    right: Any | None = Field(None, description="Content for right column")
    left_width: float | None = Field(25, description="Left column width (percentage, 0-100)")
    center_width: float | None = Field(50, description="Center column width (percentage, 0-100)")
    right_width: float | None = Field(25, description="Right column width (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap between columns (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="ThreeColumnLayout",
    description="Sidebar + Main + Sidebar arrangements with configurable widths",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Sidebar + Main + Sidebar arrangements with configurable widths",
    "category": "layout",
    "schema": {
        "left": {"type": "component", "description": "Content for left column"},
        "center": {"type": "component", "description": "Content for center column"},
        "right": {"type": "component", "description": "Content for right column"},
        "left_width": {
            "type": "number",
            "default": 25,
            "description": "Left column width (percentage, 0-100)",
        },
        "center_width": {
            "type": "number",
            "default": 50,
            "description": "Center column width (percentage, 0-100)",
        },
        "right_width": {
            "type": "number",
            "default": 25,
            "description": "Right column width (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between columns (pixels)"},
        "padding": {
            "type": "number",
            "default": 40,
            "description": "Padding around layout (pixels)",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "left": {"type": "CodeBlock", "code": "// Sidebar"},
        "center": {"type": "CodeBlock", "code": "// Main content"},
        "right": {"type": "CodeBlock", "code": "// Sidebar"},
        "left_width": 25,
        "center_width": 50,
        "right_width": 25,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Dashboard with sidebars",
            "Documentation with table of contents",
            "App with navigation panels",
            "Content with supplementary info",
        ],
    },
}
