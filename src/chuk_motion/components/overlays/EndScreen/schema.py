# chuk-motion/src/chuk_motion/components/overlays/EndScreen/schema.py
"""EndScreen component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class EndScreenProps(BaseModel):
    """Properties for EndScreen component."""

    cta_text: str = Field(description="Call-to-action text")
    thumbnail_url: str | None = Field(None, description="Video thumbnail URL")
    variant: Literal["standard", "split", "carousel", "minimal"] = Field(
        "standard", description="Layout variant"
    )
    duration_seconds: float = Field(10.0, description="Duration (seconds)", gt=0.0)

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="EndScreen",
    description="YouTube end screen with CTAs and video suggestions",
    category="scene",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "YouTube end screen with CTAs and video suggestions",
    "category": "scene",
    "variants": {
        "standard": "Simple layout with video thumbnail and subscribe",
        "split": "Split screen with multiple CTAs",
        "carousel": "Sliding carousel of videos",
        "minimal": "Clean single CTA",
    },
    "schema": {
        "cta_text": {"type": "string", "required": True, "description": "Call-to-action text"},
        "thumbnail_url": {"type": "string", "default": None, "description": "Video thumbnail URL"},
        "variant": {
            "type": "enum",
            "default": "standard",
            "values": ["standard", "split", "carousel", "minimal"],
            "description": "Layout variant",
        },
        "duration_seconds": {"type": "float", "default": 10.0, "description": "Duration (seconds)"},
    },
    "example": {
        "cta_text": "Watch Next",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "variant": "split",
        "duration_seconds": 10.0,
    },
}
