# chuk-motion/src/chuk_motion/components/layouts/Container/schema.py
"""Container component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ContainerProps(BaseModel):
    """Properties for Container component."""

    position: Any | None = Field("center", description="Position on screen")
    width: str | None = Field("auto", description="Width (px, %, or auto)")
    height: str | None = Field("auto", description="Height (px, %, or auto)")
    padding: float | None = Field(40, description="Internal padding (pixels)")
    content: Any = Field(description="Component to position")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="Container", description="Flexible positioning container for components", category="layout"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Flexible positioning container for components",
    "category": "layout",
    "positions": {
        "center": "Center of screen",
        "top-left": "Top left corner",
        "top-center": "Top center",
        "top-right": "Top right corner",
        "middle-left": "Middle left",
        "middle-right": "Middle right",
        "bottom-left": "Bottom left corner",
        "bottom-center": "Bottom center",
        "bottom-right": "Bottom right corner",
    },
    "schema": {
        "position": {
            "type": "enum",
            "default": "center",
            "values": [
                "center",
                "top-left",
                "top-center",
                "top-right",
                "middle-left",
                "middle-right",
                "bottom-left",
                "bottom-center",
                "bottom-right",
            ],
            "description": "Position on screen",
        },
        "width": {"type": "string", "default": "auto", "description": "Width (px, %, or auto)"},
        "height": {"type": "string", "default": "auto", "description": "Height (px, %, or auto)"},
        "padding": {"type": "number", "default": 40, "description": "Internal padding (pixels)"},
        "content": {"type": "component", "required": True, "description": "Component to position"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "position": "top-right",
        "width": "400px",
        "height": "auto",
        "padding": 20,
        "content": {"type": "CodeBlock", "code": "..."},
        "start_time": 0.0,
        "duration": 5.0,
    },
}
