"""BrowserFrame component schema and metadata."""

from typing import Literal, Optional, List
from pydantic import BaseModel, Field
from chuk_mcp_remotion.components.base import ComponentMetadata

class TabConfig(BaseModel):
    """Configuration for a browser tab."""
    title: str = Field(default="New Tab", description="Tab title")
    active: bool = Field(default=False, description="Whether this tab is active")

class BrowserFrameProps(BaseModel):
    """Props for BrowserFrame component."""

    startFrame: int = Field(..., description="Frame when component becomes visible")
    durationInFrames: int = Field(..., description="Duration in frames")
    url: str = Field(
        default="https://example.com",
        description="URL to display in the address bar"
    )
    theme: Literal["light", "dark", "chrome", "firefox", "safari", "arc"] = Field(
        default="chrome",
        description="Browser theme style"
    )
    tabs: Optional[List[dict]] = Field(
        default=None,
        description="List of tabs to display (each with title and active status)"
    )
    showStatus: bool = Field(
        default=False,
        description="Show status bar at bottom"
    )
    statusText: str = Field(
        default="",
        description="Status bar text to display"
    )
    content: str = Field(
        default="",
        description="Content to display in browser window (image path or text)"
    )
    width: int = Field(
        default=1200,
        description="Browser window width in pixels",
        ge=400,
        le=1920
    )
    height: int = Field(
        default=800,
        description="Browser window height in pixels",
        ge=300,
        le=1080
    )
    position: Literal[
        "center",
        "top-left", "top-center", "top-right",
        "center-left", "center-right",
        "bottom-left", "bottom-center", "bottom-right"
    ] = Field(
        default="center",
        description="Position of browser window on screen"
    )
    shadow: bool = Field(
        default=True,
        description="Enable window shadow"
    )

METADATA = ComponentMetadata(
    name="BrowserFrame",
    description="Realistic browser window with URL bar, tabs, swappable themes (Chrome, Firefox, Safari, Arc), and optional status bar",
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
    "url": {
        "type": "string",
        "description": "URL to display in the address bar",
        "default": "https://example.com",
    },
    "theme": {
        "type": "string",
        "description": "Browser theme: light, dark, chrome, firefox, safari, arc",
        "default": "chrome",
        "enum": ["light", "dark", "chrome", "firefox", "safari", "arc"],
    },
    "tabs": {
        "type": "array",
        "description": "List of tabs (objects with title and active properties)",
        "default": None,
    },
    "showStatus": {
        "type": "boolean",
        "description": "Show status bar at bottom",
        "default": False,
    },
    "statusText": {
        "type": "string",
        "description": "Status bar text to display",
        "default": "",
    },
    "content": {
        "type": "string",
        "description": "Content to display in browser window",
        "default": "",
    },
    "width": {
        "type": "number",
        "description": "Browser window width in pixels (400-1920)",
        "default": 1200,
    },
    "height": {
        "type": "number",
        "description": "Browser window height in pixels (300-1080)",
        "default": 800,
    },
    "position": {
        "type": "string",
        "description": "Position of browser window on screen",
        "default": "center",
        "enum": [
            "center",
            "top-left", "top-center", "top-right",
            "center-left", "center-right",
            "bottom-left", "bottom-center", "bottom-right"
        ],
    },
    "shadow": {
        "type": "boolean",
        "description": "Enable window shadow",
        "default": True,
    },
}
