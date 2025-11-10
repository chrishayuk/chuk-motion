# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/PerformanceMultiCam/schema.py
"""PerformanceMultiCam component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class PerformanceMultiCamProps(BaseModel):
    """Properties for PerformanceMultiCam component."""

    primary_cam: Any | None = Field(None, description="Main camera feed")
    secondary_cams: list[Any] | None = Field(
        [], description="List of secondary camera feeds (up to 4)"
    )
    layout: str | None = Field("primary-main", description="Layout: primary-main, grid, filmstrip")
    gap: float | None = Field(20, description="Gap between cameras (pixels)")
    padding: float | None = Field(40, description="Padding (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="PerformanceMultiCam",
    description="Multi-camera performance view with primary + secondary cameras",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Multi-camera performance view with primary + secondary cameras",
    "category": "layout",
    "schema": {
        "primary_cam": {"type": "component", "description": "Main camera feed"},
        "secondary_cams": {"type": "array", "description": "Secondary camera feeds (up to 4)"},
        "layout": {
            "type": "enum",
            "default": "primary-main",
            "values": ["primary-main", "grid", "filmstrip"],
            "description": "Layout style",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
}
