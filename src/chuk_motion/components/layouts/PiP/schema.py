# chuk-motion/src/chuk_motion/components/layouts/PiP/schema.py
"""PiP component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class PiPProps(BaseModel):
    """Properties for PiP component."""

    main_content: Any | None = Field(None, description="Main background content")
    pip_content: Any | None = Field(None, description="Picture-in-picture overlay content")
    position: str | None = Field(
        "bottom-right",
        description="Overlay position: bottom-right, bottom-left, top-right, top-left",
    )
    overlay_size: float | None = Field(20, description="Overlay size (percentage of screen, 0-100)")
    margin: float | None = Field(40, description="Margin from edges (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="PiP",
    description="Picture-in-Picture webcam overlay with customizable positions",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Picture-in-Picture webcam overlay with customizable positions",
    "category": "layout",
    "schema": {
        "main_content": {"type": "component", "description": "Main background content"},
        "pip_content": {"type": "component", "description": "Picture-in-picture overlay content"},
        "position": {
            "type": "enum",
            "default": "bottom-right",
            "values": ["bottom-right", "bottom-left", "top-right", "top-left"],
            "description": "Overlay position",
        },
        "overlay_size": {
            "type": "number",
            "default": 20,
            "description": "Overlay size (percentage of screen, 0-100)",
        },
        "margin": {
            "type": "number",
            "default": 40,
            "description": "Margin from edges (pixels)",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "main_content": {"type": "CodeBlock", "code": "// Main content"},
        "pip_content": {"type": "CodeBlock", "code": "// Webcam"},
        "position": "bottom-right",
        "overlay_size": 20,
        "margin": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Tutorial with webcam overlay",
            "Screen recording with presenter",
            "Reaction videos",
            "Live commentary over content",
        ],
    },
}
