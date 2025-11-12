# chuk-motion/src/chuk_motion/components/charts/BarChart/schema.py
"""BarChart component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class BarDataPoint(BaseModel):
    """A single data point with label and value."""

    label: str
    value: float
    color: str | None = None


class BarChartProps(BaseModel):
    """Properties for BarChart component."""

    data: list[BarDataPoint] = Field(
        description="List of objects with label, value, and optional color"
    )
    title: str | None = Field(None, description="Optional chart title")
    xlabel: str | None = Field(None, description="Optional x-axis label")
    ylabel: str | None = Field(None, description="Optional y-axis label")
    start_time: float = Field(0.0, description="When to show (seconds)")
    duration: float = Field(4.0, description="How long to animate (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="BarChart",
    description="Animated vertical bar chart for comparing categories",
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
        "xlabel": {"type": "string", "default": "", "description": "Optional x-axis label"},
        "ylabel": {"type": "string", "default": "", "description": "Optional y-axis label"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {
            "type": "float",
            "required": True,
            "description": "How long to animate (seconds)",
        },
    },
    "example": [{"label": "Q1", "value": 45}, {"label": "Q2", "value": 67}],
}
