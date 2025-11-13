# chuk-motion/src/chuk_motion/components/content/StylizedWebPage/schema.py
"""StylizedWebPage component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class StylizedWebPageProps(BaseModel):
    """Properties for StylizedWebPage component."""

    title: str = Field("Website Title", description="Page title displayed in header")
    subtitle: str = Field("Tagline or description", description="Hero section subtitle")
    show_header: bool = Field(True, description="Show header/navbar")
    show_sidebar: bool = Field(False, description="Show sidebar navigation")
    show_footer: bool = Field(False, description="Show footer")
    header_text: str = Field("Navigation", description="Text in header nav area")
    sidebar_items: list[str] = Field(
        ["Dashboard", "Analytics", "Settings"],
        description="List of sidebar navigation items"
    )
    content_lines: list[str] = Field(
        ["Welcome to our site", "Explore our features", "Get started today"],
        description="Main content block text lines"
    )
    footer_text: str = Field("© 2024 Company", description="Footer text")
    theme: Literal["light", "dark"] = Field("light", description="Visual theme")
    accent_color: Literal["primary", "accent", "secondary"] = Field(
        "primary", description="Accent color theme"
    )
    start_time: float | None = Field(None, description="When to show (seconds)")
    duration: float | None = Field(None, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="StylizedWebPage",
    description="Stylized webpage mockup with header, sidebar, content blocks, and footer",
    category="content",
)


# MCP schema
MCP_SCHEMA = {
    "description": "Stylized webpage mockup with header, sidebar, content blocks, and footer",
    "category": "content",
    "schema": {
        "title": {
            "type": "string",
            "default": "Website Title",
            "description": "Page title displayed in header"
        },
        "subtitle": {
            "type": "string",
            "default": "Tagline or description",
            "description": "Hero section subtitle"
        },
        "show_header": {
            "type": "boolean",
            "default": True,
            "description": "Show header/navbar"
        },
        "show_sidebar": {
            "type": "boolean",
            "default": False,
            "description": "Show sidebar navigation"
        },
        "show_footer": {
            "type": "boolean",
            "default": False,
            "description": "Show footer"
        },
        "header_text": {
            "type": "string",
            "default": "Navigation",
            "description": "Text in header nav area"
        },
        "sidebar_items": {
            "type": "array",
            "default": ["Dashboard", "Analytics", "Settings"],
            "description": "List of sidebar navigation items"
        },
        "content_lines": {
            "type": "array",
            "default": ["Welcome to our site", "Explore our features", "Get started today"],
            "description": "Main content block text lines"
        },
        "footer_text": {
            "type": "string",
            "default": "© 2024 Company",
            "description": "Footer text"
        },
        "theme": {
            "type": "enum",
            "default": "light",
            "values": ["light", "dark"],
            "description": "Visual theme"
        },
        "accent_color": {
            "type": "enum",
            "default": "primary",
            "values": ["primary", "accent", "secondary"],
            "description": "Accent color theme"
        },
        "start_time": {
            "type": "float",
            "description": "When to show (seconds)"
        },
        "duration": {
            "type": "float",
            "description": "How long to show (seconds)"
        },
    },
    "example": {
        "title": "My Amazing App",
        "subtitle": "Build something incredible",
        "show_header": True,
        "show_sidebar": True,
        "show_footer": True,
        "header_text": "Home • About • Contact",
        "sidebar_items": ["Dashboard", "Analytics", "Settings", "Profile"],
        "content_lines": [
            "Welcome to our platform",
            "Discover powerful features",
            "Get started in minutes"
        ],
        "footer_text": "© 2024 My Company",
        "theme": "light",
        "accent_color": "primary",
        "start_time": 0.0,
        "duration": 5.0,
    },
}
