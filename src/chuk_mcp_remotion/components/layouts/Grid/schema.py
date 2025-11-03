# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Grid/schema.py
"""Grid component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class GridProps(BaseModel):
    """Properties for Grid component."""

    layout: Any | None = Field("3x3", description="Grid dimensions")
    gap: float | None = Field(20, description="Gap between items (pixels)")
    padding: float | None = Field(40, description="Padding around grid (pixels)")
    items: list[Any] = Field(description="Array of components to display")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="Grid", description="Grid layout for multiple items", category="layout"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Grid layout for multiple items",
    "category": "layout",
    "layouts": {
        "1x2": "1 column, 2 rows (simple stack)",
        "2x1": "2 columns, 1 row (side-by-side)",
        "2x2": "2 columns, 2 rows (4 items)",
        "3x2": "3 columns, 2 rows (6 items)",
        "2x3": "2 columns, 3 rows (6 items)",
        "3x3": "3 columns, 3 rows (9 items) - Instagram style",
        "4x2": "4 columns, 2 rows (8 items)",
        "2x4": "2 columns, 4 rows (8 items)",
    },
    "schema": {
        "layout": {
            "type": "enum",
            "default": "3x3",
            "values": ["1x2", "2x1", "2x2", "3x2", "2x3", "3x3", "4x2", "2x4"],
            "description": "Grid dimensions",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between items (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding around grid (pixels)"},
        "items": {
            "type": "array",
            "required": True,
            "description": "Array of components to display",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "layout": "3x3",
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
            "Before/after transformations",
            "Feature grid",
            "Social media style display",
        ],
    },
}
