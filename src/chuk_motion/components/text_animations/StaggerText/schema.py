"""StaggerText component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class StaggerTextProps(BaseModel):
    """Properties for StaggerText component."""

    text: str = Field(description="Text to animate")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(default="3xl", description="Font size")
    fontWeight: Literal["normal", "medium", "semibold", "bold", "extrabold", "black"] = Field(
        default="bold", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    staggerBy: Literal["char", "word"] = Field(
        default="char", description="Stagger by character or word"
    )
    staggerDelay: float = Field(
        default=2.0, description="Delay in frames between units", ge=0.5, le=10.0
    )
    animationType: Literal["fade", "slide-up", "slide-down", "scale"] = Field(
        default="fade", description="Animation style"
    )
    position: Literal["center", "top", "bottom"] = Field(
        default="center", description="Vertical position"
    )
    align: Literal["left", "center", "right"] = Field(
        default="center", description="Text alignment"
    )
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=3.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="StaggerText",
    description="Staggered reveal animation where characters or words appear one-by-one with spring physics",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Staggered reveal animation where characters or words appear one-by-one with spring physics for smooth, professional appearance",
    "category": "text-animation",
    "tags": ["text", "stagger", "reveal", "animation", "spring", "professional"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to animate",
        },
        "font_size": {
            "type": "string",
            "default": "3xl",
            "description": "Font size (xl, 2xl, 3xl, 4xl)",
        },
        "font_weight": {
            "type": "string",
            "default": "bold",
            "description": "Font weight (normal, medium, semibold, bold, extrabold, black)",
        },
        "text_color": {
            "type": "string",
            "optional": True,
            "description": "Text color (uses on_dark color if not specified)",
        },
        "stagger_by": {
            "type": "string",
            "default": "char",
            "values": ["char", "word"],
            "description": "Stagger by character or word",
        },
        "stagger_delay": {
            "type": "number",
            "default": 2.0,
            "description": "Delay in frames between units",
        },
        "animation_type": {
            "type": "string",
            "default": "fade",
            "values": ["fade", "slide-up", "slide-down", "scale"],
            "description": "Animation style",
        },
        "position": {
            "type": "string",
            "default": "center",
            "values": ["center", "top", "bottom"],
            "description": "Vertical position",
        },
        "align": {
            "type": "string",
            "default": "center",
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
        "text": "Welcome",
        "font_size": "3xl",
        "stagger_by": "char",
        "stagger_delay": 2.0,
        "animation_type": "slide-up",
        "start_time": 0.0,
        "duration": 3.0,
    },
    "use_cases": [
        "Title reveals",
        "Bullet point lists",
        "Professional presentations",
        "Step-by-step reveals",
        "Impact statements",
    ],
    "design_tokens_used": {
        "typography": [
            "font_sizes['3xl']",
            "font_weights.bold",
            "primary_font",
            "letter_spacing.wide",
            "line_heights.relaxed",
        ],
        "colors": ["text.on_dark"],
        "spacing": ["spacing.xl", "spacing['4xl']"],
        "motion": [
            "default_spring.damping",
            "default_spring.stiffness",
            "default_spring.mass",
        ],
    },
}
