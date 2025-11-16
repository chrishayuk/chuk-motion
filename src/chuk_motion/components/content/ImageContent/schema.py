"""ImageContent component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class ImageContentProps(BaseModel):
    """Properties for ImageContent component."""

    src: str = Field(description="Image source URL or path to static file (e.g. 'image.png')")
    fit: Literal["contain", "cover", "fill"] = Field(
        default="cover", description="How image fits in container"
    )
    opacity: float = Field(default=1.0, description="Image opacity (0.0 to 1.0)", ge=0.0, le=1.0)
    border_radius: int = Field(default=0, description="Border radius in pixels", ge=0)
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=5.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="ImageContent",
    description="Image display component for showing images",
    category="content",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Image display component for showing images. Supports local files (via staticFile) and remote URLs. Perfect for adding image content to layouts.",
    "category": "content",
    "tags": ["image", "picture", "media", "content", "display"],
    "schema": {
        "src": {
            "type": "string",
            "required": True,
            "description": "Image source URL or path to static file (e.g. 'image.png')",
        },
        "fit": {
            "type": "string",
            "default": "cover",
            "values": ["contain", "cover", "fill"],
            "description": "How image fits in container",
        },
        "opacity": {
            "type": "number",
            "default": 1.0,
            "description": "Image opacity (0.0 to 1.0)",
        },
        "border_radius": {
            "type": "integer",
            "default": 0,
            "description": "Border radius in pixels",
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)",
        },
        "duration": {
            "type": "float",
            "default": 5.0,
            "description": "Total duration (seconds)",
        },
    },
    "example": {
        "src": "image.png",
        "fit": "cover",
        "opacity": 1.0,
        "border_radius": 0,
        "start_time": 0.0,
        "duration": 5.0,
    },
    "use_cases": [
        "Image backgrounds for layouts",
        "Product photos and screenshots",
        "Logo and branding displays",
        "Marketing visual content",
        "Presentation images and slides",
    ],
    "design_tokens_used": {
        "colors": ["background.dark"],
    },
}
