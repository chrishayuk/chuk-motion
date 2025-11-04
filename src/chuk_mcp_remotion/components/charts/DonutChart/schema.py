# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/DonutChart/schema.py
"""DonutChart component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DonutDataPoint(BaseModel):
    """A single data point with label and value."""

    label: str
    value: float
    color: str | None = None


class DonutChartProps(BaseModel):
    """Properties for DonutChart component."""

    data: list[DonutDataPoint] = Field(
        description="List of objects with label, value, and optional color"
    )
    title: str | None = Field(None, description="Optional chart title")
    center_text: str | None = Field(None, description="Text to display in center")
    start_time: float = Field(0.0, description="When to show (seconds)")
    duration: float = Field(4.0, description="How long to animate (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="DonutChart",
    description="Animated donut chart with center text for showing proportions",
    category="chart",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": METADATA.description,
    "category": METADATA.category,
    "animations": {
        "draw": "Chart draws with animation",
        "fade_in": "Chart fades in",
        "scale_in": "Chart scales from center",
    },
    "schema": {
        "data": {
            "type": "array",
            "required": True,
            "description": "List of objects with label, value, and optional color",
        },
        "title": {"type": "string", "default": "", "description": "Optional chart title"},
        "center_text": {
            "type": "string",
            "default": "",
            "description": "Text to display in center",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {
            "type": "float",
            "required": True,
            "description": "How long to animate (seconds)",
        },
    },
    "example": [{"label": "Complete", "value": 75}, {"label": "In Progress", "value": 15}],
}
