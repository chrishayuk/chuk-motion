# chuk-motion/src/chuk_motion/components/code/TypingCode/schema.py
"""TypingCode component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TypingCodeProps(BaseModel):
    """Properties for TypingCode component."""

    code: str = Field(description="Code to type out")
    language: str | None = Field("javascript", description="Programming language")
    title: str | None = Field(None, description="Optional title/filename")
    variant: Any | None = Field("editor", description="Visual style")
    cursor_style: Any | None = Field("line", description="Cursor appearance")
    typing_speed: Any | None = Field("normal", description="Typing animation speed")
    show_line_numbers: bool | None = Field(True, description="Show line numbers")
    start_time: float = Field(description="When to start (seconds)")
    duration: float | None = Field(10.0, description="How long to type (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="TypingCode", description="Animated typing code effect with cursor", category="code"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated typing code effect with cursor",
    "category": "code",
    "variants": {
        "minimal": "Clean typing effect",
        "terminal": "Terminal-style with cursor",
        "editor": "IDE-style typing",
        "hacker": "Matrix/hacker style",
    },
    "cursor_styles": {
        "block": "Solid block cursor",
        "line": "Vertical line cursor",
        "underline": "Underscore cursor",
        "none": "No cursor",
    },
    "schema": {
        "code": {"type": "string", "required": True, "description": "Code to type out"},
        "language": {
            "type": "string",
            "default": "javascript",
            "description": "Programming language",
        },
        "title": {"type": "string", "default": "", "description": "Optional title/filename"},
        "variant": {
            "type": "enum",
            "default": "editor",
            "values": ["minimal", "terminal", "editor", "hacker"],
            "description": "Visual style",
        },
        "cursor_style": {
            "type": "enum",
            "default": "line",
            "values": ["block", "line", "underline", "none"],
            "description": "Cursor appearance",
        },
        "typing_speed": {
            "type": "enum",
            "default": "normal",
            "values": ["slow", "normal", "fast", "instant"],
            "description": "Typing animation speed",
        },
        "show_line_numbers": {
            "type": "boolean",
            "default": True,
            "description": "Show line numbers",
        },
        "start_time": {"type": "float", "required": True, "description": "When to start (seconds)"},
        "duration": {"type": "float", "default": 10.0, "description": "How long to type (seconds)"},
    },
    "example": {
        "code": "function fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n-1) + fibonacci(n-2);\n}",
        "language": "javascript",
        "title": "fibonacci.js",
        "variant": "editor",
        "cursor_style": "line",
        "typing_speed": "normal",
        "show_line_numbers": True,
        "start_time": 2.0,
        "duration": 8.0,
    },
}
