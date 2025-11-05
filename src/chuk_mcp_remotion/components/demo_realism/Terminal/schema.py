"""Terminal component schema and metadata."""

from typing import Literal, Optional, List
from pydantic import BaseModel, Field
from chuk_mcp_remotion.components.base import ComponentMetadata

class CommandBlock(BaseModel):
    """Configuration for a command and its output."""
    command: str = Field(..., description="Command to display/type")
    output: str = Field(default="", description="Command output/result")
    typeOn: bool = Field(default=True, description="Animate typing of command")

class TerminalProps(BaseModel):
    """Props for Terminal component."""

    startFrame: int = Field(..., description="Frame when component becomes visible")
    durationInFrames: int = Field(..., description="Duration in frames")
    commands: List[dict] = Field(
        default=[],
        description="List of command blocks (each with command, output, and typeOn)"
    )
    prompt: Literal["bash", "zsh", "powershell", "custom"] = Field(
        default="bash",
        description="Terminal prompt style"
    )
    customPrompt: str = Field(
        default="$",
        description="Custom prompt string (used when prompt is 'custom')"
    )
    title: str = Field(
        default="Terminal",
        description="Title shown in terminal window header"
    )
    theme: Literal["dark", "light", "dracula", "monokai", "nord", "solarized"] = Field(
        default="dark",
        description="Terminal color theme"
    )
    width: int = Field(
        default=900,
        description="Terminal window width in pixels",
        ge=400,
        le=1600
    )
    height: int = Field(
        default=600,
        description="Terminal window height in pixels",
        ge=300,
        le=1000
    )
    position: Literal[
        "center",
        "top-left", "top-center", "top-right",
        "center-left", "center-right",
        "bottom-left", "bottom-center", "bottom-right"
    ] = Field(
        default="center",
        description="Position of terminal window on screen"
    )
    showCursor: bool = Field(
        default=True,
        description="Show blinking cursor"
    )
    typeSpeed: float = Field(
        default=0.05,
        description="Typing animation speed (seconds per character)",
        ge=0.01,
        le=0.5
    )

METADATA = ComponentMetadata(
    name="Terminal",
    description="Realistic terminal/console with typing animation, command output blocks, and multiple prompt variants (bash, zsh, PowerShell)",
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
    "commands": {
        "type": "array",
        "description": "List of command blocks (objects with command, output, typeOn)",
        "default": [],
    },
    "prompt": {
        "type": "string",
        "description": "Terminal prompt style: bash, zsh, powershell, custom",
        "default": "bash",
        "enum": ["bash", "zsh", "powershell", "custom"],
    },
    "customPrompt": {
        "type": "string",
        "description": "Custom prompt string (when prompt is 'custom')",
        "default": "$",
    },
    "title": {
        "type": "string",
        "description": "Title shown in terminal window header",
        "default": "Terminal",
    },
    "theme": {
        "type": "string",
        "description": "Terminal color theme",
        "default": "dark",
        "enum": ["dark", "light", "dracula", "monokai", "nord", "solarized"],
    },
    "width": {
        "type": "number",
        "description": "Terminal window width in pixels (400-1600)",
        "default": 900,
    },
    "height": {
        "type": "number",
        "description": "Terminal window height in pixels (300-1000)",
        "default": 600,
    },
    "position": {
        "type": "string",
        "description": "Position of terminal window on screen",
        "default": "center",
        "enum": [
            "center",
            "top-left", "top-center", "top-right",
            "center-left", "center-right",
            "bottom-left", "bottom-center", "bottom-right"
        ],
    },
    "showCursor": {
        "type": "boolean",
        "description": "Show blinking cursor",
        "default": True,
    },
    "typeSpeed": {
        "type": "number",
        "description": "Typing animation speed (seconds per character, 0.01-0.5)",
        "default": 0.05,
    },
}
