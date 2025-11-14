"""CodeDiff component schema and metadata."""

from typing import Literal

from pydantic import BaseModel, Field

from chuk_motion.components.base import ComponentMetadata


class DiffLine(BaseModel):
    """Configuration for a diff line."""

    content: str = Field(..., description="Line content")
    type: Literal["added", "removed", "unchanged", "context"] = Field(
        ..., description="Type of change"
    )
    lineNumber: int | None = Field(None, description="Line number")
    heatLevel: int | None = Field(
        None, description="Heat level for heatmap (0-100, higher = more changes)", ge=0, le=100
    )


class CodeDiffProps(BaseModel):
    """Props for CodeDiff component."""

    startFrame: int = Field(..., description="Frame when component becomes visible")
    durationInFrames: int = Field(..., description="Duration in frames")
    lines: list[DiffLine] = Field(
        default=[],
        description="List of diff lines (each with content, type, lineNumber, heatLevel)",
    )
    mode: Literal["unified", "split"] = Field(
        default="unified", description="Diff display mode: unified or split (side-by-side)"
    )
    language: str = Field(
        default="typescript", description="Programming language for syntax highlighting"
    )
    showLineNumbers: bool = Field(default=True, description="Show line numbers")
    showHeatmap: bool = Field(default=False, description="Show heatmap visualization of changes")
    title: str = Field(default="Code Comparison", description="Title for the diff viewer")
    leftLabel: str = Field(default="Before", description="Label for left side (in split mode)")
    rightLabel: str = Field(default="After", description="Label for right side (in split mode)")
    theme: Literal["dark", "light", "github", "monokai"] = Field(
        default="dark", description="Color theme for the diff viewer"
    )
    width: int = Field(default=1400, description="Diff viewer width in pixels", ge=600, le=1920)
    height: int = Field(default=800, description="Diff viewer height in pixels", ge=400, le=1080)
    position: Literal[
        "center",
        "top-left",
        "top-center",
        "top-right",
        "center-left",
        "center-right",
        "bottom-left",
        "bottom-center",
        "bottom-right",
    ] = Field(default="center", description="Position of diff viewer on screen")
    animateLines: bool = Field(default=True, description="Animate lines appearing one by one")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="CodeDiff",
    description="Code diff viewer with side-by-side or unified view, added/removed line highlighting, optional heatmap visualization, and syntax highlighting",
    category="demo_realism",
)

# MCP schema (backward compatible)
MCP_SCHEMA = {
    "startFrame": {
        "type": "number",
        "description": "Frame when component becomes visible",
        "required": True,
    },
    "durationInFrames": {
        "type": "number",
        "description": "Duration in frames",
        "required": True,
    },
    "lines": {
        "type": "array",
        "description": "List of diff lines (objects with content, type, lineNumber, heatLevel)",
        "default": [],
    },
    "mode": {
        "type": "string",
        "description": "Diff display mode: unified or split",
        "default": "unified",
        "enum": ["unified", "split"],
    },
    "language": {
        "type": "string",
        "description": "Programming language for syntax highlighting",
        "default": "typescript",
    },
    "showLineNumbers": {
        "type": "boolean",
        "description": "Show line numbers",
        "default": True,
    },
    "showHeatmap": {
        "type": "boolean",
        "description": "Show heatmap visualization",
        "default": False,
    },
    "title": {
        "type": "string",
        "description": "Title for the diff viewer",
        "default": "Code Comparison",
    },
    "leftLabel": {
        "type": "string",
        "description": "Label for left side (split mode)",
        "default": "Before",
    },
    "rightLabel": {
        "type": "string",
        "description": "Label for right side (split mode)",
        "default": "After",
    },
    "theme": {
        "type": "string",
        "description": "Color theme: dark, light, github, monokai",
        "default": "dark",
        "enum": ["dark", "light", "github", "monokai"],
    },
    "width": {
        "type": "number",
        "description": "Diff viewer width in pixels (600-1920)",
        "default": 1400,
    },
    "height": {
        "type": "number",
        "description": "Diff viewer height in pixels (400-1080)",
        "default": 800,
    },
    "position": {
        "type": "string",
        "description": "Position of diff viewer on screen",
        "default": "center",
        "enum": [
            "center",
            "top-left",
            "top-center",
            "top-right",
            "center-left",
            "center-right",
            "bottom-left",
            "bottom-center",
            "bottom-right",
        ],
    },
    "animateLines": {
        "type": "boolean",
        "description": "Animate lines appearing one by one",
        "default": True,
    },
}
