# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeByThreeGrid/schema.py
"""ThreeByThreeGrid component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ThreeByThreeGridProps(BaseModel):
    """Properties for ThreeByThreeGrid component."""

    gap: float | None = Field(20, description="Gap between items (pixels)")
    padding: float | None = Field(40, description="Padding around grid (pixels)")
    items: list[Any] = Field(description="Array of up to 9 components to display")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="ThreeByThreeGrid",
    description="Perfect 3x3 grid layout (9 cells)",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Perfect 3x3 grid layout (9 cells)",
    "category": "layout",
    "schema": {
        "gap": {"type": "number", "default": 20, "description": "Gap between items (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding around grid (pixels)"},
        "items": {
            "type": "array",
            "required": True,
            "description": "Array of up to 9 components to display",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "gap": 20,
        "padding": 40,
        "items": [
            {"type": "CodeBlock", "code": "Python"},
            {"type": "CodeBlock", "code": "JavaScript"},
            {"type": "CodeBlock", "code": "Rust"},
            {"type": "CodeBlock", "code": "Go"},
            {"type": "CodeBlock", "code": "TypeScript"},
            {"type": "CodeBlock", "code": "Swift"},
            {"type": "CodeBlock", "code": "Kotlin"},
            {"type": "CodeBlock", "code": "Ruby"},
            {"type": "CodeBlock", "code": "C++"},
        ],
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Portfolio showcase (9 projects)",
            "Language comparison",
            "Instagram-style grid",
            "Feature showcase",
            "Social media style display",
        ],
    },
}
