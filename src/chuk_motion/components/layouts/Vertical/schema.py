# chuk-motion/src/chuk_motion/components/layouts/Vertical/schema.py
"""Vertical component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class VerticalProps(BaseModel):
    """Properties for Vertical component."""

    top: Any | None = Field(None, description="Top content")
    bottom: Any | None = Field(None, description="Bottom content")
    layout_style: str | None = Field(
        "top-bottom",
        description="Layout style: top-bottom, caption-content, content-caption, split-vertical",
    )
    top_ratio: float | None = Field(50, description="Top section ratio (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap between sections (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="Vertical",
    description="9:16 optimized for Shorts/TikTok/Reels with multiple layout styles",
    category="layout",
)


# MCP schema
MCP_SCHEMA = {
    "description": "9:16 optimized for Shorts/TikTok/Reels with multiple layout styles",
    "category": "layout",
    "schema": {
        "top": {"type": "component", "description": "Top content"},
        "bottom": {"type": "component", "description": "Bottom content"},
        "layout_style": {
            "type": "enum",
            "default": "top-bottom",
            "values": ["top-bottom", "caption-content", "content-caption", "split-vertical"],
            "description": "Layout style",
        },
        "top_ratio": {
            "type": "number",
            "default": 50,
            "description": "Top section ratio (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between sections (pixels)"},
        "padding": {
            "type": "number",
            "default": 40,
            "description": "Padding around layout (pixels)",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "top": {"type": "CodeBlock", "code": "// Content"},
        "bottom": {"type": "CodeBlock", "code": "// Caption"},
        "layout_style": "content-caption",
        "top_ratio": 70,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "YouTube Shorts",
            "TikTok videos",
            "Instagram Reels",
            "Mobile-first content",
        ],
    },
}
