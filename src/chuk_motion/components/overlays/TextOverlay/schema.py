# chuk-motion/src/chuk_motion/components/overlays/TextOverlay/schema.py
"""TextOverlay component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TextOverlayProps(BaseModel):
    """Properties for TextOverlay component."""

    text: str = Field(..., min_length=1, description="Text content")
    style: Literal["emphasis", "caption", "callout", "subtitle", "quote"] | None = Field(
        "emphasis", description="Text style"
    )
    animation: Literal["blur_in", "slide_up", "fade", "typewriter", "scale_in"] | None = Field(
        "blur_in", description="Animation style"
    )
    start_time: float = Field(..., ge=0.0, description="When to show (seconds)")
    duration: float | None = Field(3.0, gt=0.0, description="How long to show (seconds)")
    position: Literal["center", "top", "bottom", "custom"] | None = Field(
        "center", description="Position (center, top, bottom, custom)"
    )

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="TextOverlay",
    description="Animated text overlay for emphasis and captions",
    category="overlay",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated text overlay for emphasis and captions",
    "category": "overlay",
    "styles": {
        "emphasis": "Large text for key points",
        "caption": "Subtitle-style text at bottom",
        "callout": "Attention-grabbing highlight",
        "subtitle": "Standard subtitle formatting",
        "quote": "Quotation styling with attribution",
    },
    "animations": {
        "blur_in": "Blur to focus",
        "slide_up": "Slide from bottom",
        "fade": "Simple fade in/out",
        "typewriter": "Character reveal",
        "scale_in": "Scale from center",
    },
    "schema": {
        "text": {"type": "string", "required": True, "description": "Text content"},
        "style": {
            "type": "enum",
            "default": "emphasis",
            "values": ["emphasis", "caption", "callout", "subtitle", "quote"],
            "description": "Text style",
        },
        "animation": {
            "type": "enum",
            "default": "blur_in",
            "values": ["blur_in", "slide_up", "fade", "typewriter", "scale_in"],
            "description": "Animation style",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 3.0, "description": "How long to show (seconds)"},
        "position": {
            "type": "string",
            "default": "center",
            "description": "Position (center, top, bottom, custom)",
        },
    },
    "example": {
        "text": "Mind. Blown. \ud83e\udd2f",
        "style": "emphasis",
        "animation": "scale_in",
        "start_time": 5.0,
        "duration": 2.0,
        "position": "center",
    },
}
