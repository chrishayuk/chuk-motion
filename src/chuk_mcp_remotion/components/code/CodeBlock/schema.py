# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/CodeBlock/schema.py
"""CodeBlock component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class CodeBlockProps(BaseModel):
    """Properties for CodeBlock component."""

    code: str = Field(description="Code content to display")
    language: str | None = Field(
        "javascript", description="Programming language (for syntax highlighting)"
    )
    title: str | None = Field(None, description="Optional title/filename")
    variant: Any | None = Field("editor", description="Visual style")
    animation: Any | None = Field("fade_in", description="Entrance animation")
    show_line_numbers: bool | None = Field(True, description="Show line numbers")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="CodeBlock",
    description="Syntax-highlighted code display with animated entrance",
    category="code",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Syntax-highlighted code display with animated entrance",
    "category": "code",
    "variants": {
        "minimal": "Clean code with subtle background",
        "terminal": "Terminal/console styling",
        "editor": "IDE/editor styling with line numbers",
        "glass": "Glassmorphism effect",
    },
    "animations": {
        "fade_in": "Simple fade in",
        "slide_up": "Slide from bottom",
        "scale_in": "Scale from center",
        "blur_in": "Blur to focus",
    },
    "schema": {
        "code": {"type": "string", "required": True, "description": "Code content to display"},
        "language": {
            "type": "string",
            "default": "javascript",
            "description": "Programming language (for syntax highlighting)",
        },
        "title": {"type": "string", "default": "", "description": "Optional title/filename"},
        "variant": {
            "type": "enum",
            "default": "editor",
            "values": ["minimal", "terminal", "editor", "glass"],
            "description": "Visual style",
        },
        "animation": {
            "type": "enum",
            "default": "fade_in",
            "values": ["fade_in", "slide_up", "scale_in", "blur_in"],
            "description": "Entrance animation",
        },
        "show_line_numbers": {
            "type": "boolean",
            "default": True,
            "description": "Show line numbers",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "code": "const greeting = 'Hello, World!';\nconsole.log(greeting);",
        "language": "javascript",
        "title": "hello.js",
        "variant": "editor",
        "animation": "slide_up",
        "show_line_numbers": True,
        "start_time": 3.0,
        "duration": 5.0,
    },
}
