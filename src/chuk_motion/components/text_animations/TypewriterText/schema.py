"""TypewriterText component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TypewriterTextProps(BaseModel):
    """Properties for TypewriterText component."""

    text: str = Field(description="Text to type out (supports multiline with \\n)")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(default="4xl", description="Font size")
    fontWeight: Literal["normal", "medium", "semibold", "bold"] = Field(
        default="medium", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    cursorColor: str | None = Field(None, description="Cursor color")
    showCursor: bool = Field(default=True, description="Whether to show blinking cursor")
    typeSpeed: float = Field(default=2.0, description="Characters per second", ge=0.1, le=20.0)
    position: Literal["center", "top", "bottom", "left"] = Field(
        default="center", description="Screen position"
    )
    align: Literal["left", "center", "right"] = Field(default="left", description="Text alignment")
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=3.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="TypewriterText",
    description="Classic typewriter animation with cursor",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Classic typewriter animation with cursor. Characters appear one-by-one as if being typed",
    "category": "text-animation",
    "tags": ["text", "typing", "typewriter", "cursor", "animation", "reveal"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to type out (supports multiline with \\n)",
        },
        "font_size": {
            "type": "string",
            "default": "4xl",
            "description": "Font size (xl, 2xl, 3xl, 4xl)",
        },
        "font_weight": {
            "type": "string",
            "default": "medium",
            "description": "Font weight (normal, medium, semibold, bold)",
        },
        "text_color": {
            "type": "string",
            "optional": True,
            "description": "Text color (uses on_dark color if not specified)",
        },
        "cursor_color": {
            "type": "string",
            "optional": True,
            "description": "Cursor color (uses text color if not specified)",
        },
        "show_cursor": {
            "type": "boolean",
            "default": True,
            "description": "Whether to show blinking cursor",
        },
        "type_speed": {
            "type": "number",
            "default": 2.0,
            "description": "Characters per second",
        },
        "position": {
            "type": "string",
            "default": "center",
            "values": ["center", "top", "bottom", "left"],
            "description": "Screen position",
        },
        "align": {
            "type": "string",
            "default": "left",
            "values": ["left", "center", "right"],
            "description": "Text alignment",
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)",
        },
        "duration": {
            "type": "float",
            "default": 3.0,
            "description": "Total duration (seconds)",
        },
    },
    "example": {
        "text": "Hello, World!",
        "font_size": "4xl",
        "type_speed": 2.0,
        "show_cursor": True,
        "start_time": 0.0,
        "duration": 3.0,
    },
    "use_cases": [
        "Code demonstrations",
        "Dialogue and captions",
        "Storytelling sequences",
        "Terminal/CLI effects",
        "Step-by-step instructions",
    ],
    "design_tokens_used": {
        "typography": [
            "font_sizes['4xl']",
            "font_weights.medium",
            "primary_font",
            "letter_spacing.normal",
        ],
        "colors": ["text.on_dark"],
        "spacing": ["spacing.xs", "spacing['2xl']", "spacing['4xl']"],
    },
}
