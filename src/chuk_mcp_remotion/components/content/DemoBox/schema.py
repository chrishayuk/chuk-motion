# chuk-mcp-remotion/src/chuk_mcp_remotion/components/content/DemoBox/schema.py
"""DemoBox component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DemoBoxProps(BaseModel):
    """Properties for DemoBox component."""

    label: str = Field(description="Text label to display")
    color: str | None = Field("primary", description="Color theme: primary, accent, secondary")
    start_time: float | None = Field(None, description="When to show (seconds)")
    duration: float | None = Field(None, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="DemoBox",
    description="Simple colored box with label for demos and placeholders",
    category="content",
)


# MCP schema
MCP_SCHEMA = {
    "description": "Simple colored box with label for demos and placeholders",
    "category": "content",
    "schema": {
        "label": {"type": "string", "required": True, "description": "Text label to display"},
        "color": {
            "type": "enum",
            "default": "primary",
            "values": ["primary", "accent", "secondary"],
            "description": "Color theme",
        },
        "start_time": {"type": "float", "description": "When to show (seconds)"},
        "duration": {"type": "float", "description": "How long to show (seconds)"},
    },
    "example": {
        "label": "Demo Content",
        "color": "primary",
        "start_time": 0.0,
        "duration": 5.0,
    },
}
