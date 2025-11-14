# chuk-motion/src/chuk_motion/components/content/WebPage/schema.py
"""WebPage component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class WebPageProps(BaseModel):
    """Properties for WebPage component."""

    html: str = Field(
        '<div style="padding: 40px; text-align: center;"><h1>Hello World</h1><p>This is a web page.</p></div>',
        description="HTML content to render",
    )
    css: str = Field("", description="Custom CSS styles")
    base_styles: bool = Field(True, description="Include default styling for common HTML elements")
    scale: float = Field(1.0, description="Zoom level (1.0 = 100%)")
    scroll_y: float = Field(0, description="Vertical scroll position in pixels")
    animate_scroll: bool = Field(False, description="Animate scroll from 0 to scroll_y")
    scroll_duration: float = Field(60, description="Duration of scroll animation in frames")
    theme: str = Field("light", description="Visual theme: light or dark")
    start_time: float | None = Field(None, description="When to show (seconds)")
    duration: float | None = Field(None, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="WebPage",
    description="Render real HTML content with CSS styling - perfect for showing actual web pages",
    category="content",
)


# MCP schema
MCP_SCHEMA = {
    "description": "Render real HTML content with CSS styling - perfect for showing actual web pages",
    "category": "content",
    "schema": {
        "html": {
            "type": "string",
            "default": '<div style="padding: 40px; text-align: center;"><h1>Hello World</h1><p>This is a web page.</p></div>',
            "description": "HTML content to render",
        },
        "css": {"type": "string", "default": "", "description": "Custom CSS styles"},
        "base_styles": {
            "type": "boolean",
            "default": True,
            "description": "Include default styling for common HTML elements",
        },
        "scale": {"type": "float", "default": 1.0, "description": "Zoom level (1.0 = 100%)"},
        "scroll_y": {
            "type": "float",
            "default": 0,
            "description": "Vertical scroll position in pixels",
        },
        "animate_scroll": {
            "type": "boolean",
            "default": False,
            "description": "Animate scroll from 0 to scroll_y",
        },
        "scroll_duration": {
            "type": "float",
            "default": 60,
            "description": "Duration of scroll animation in frames",
        },
        "theme": {
            "type": "enum",
            "default": "light",
            "values": ["light", "dark"],
            "description": "Visual theme",
        },
        "start_time": {"type": "float", "description": "When to show (seconds)"},
        "duration": {"type": "float", "description": "How long to show (seconds)"},
    },
    "example": {
        "html": """
<div style="max-width: 1200px; margin: 0 auto;">
  <header style="text-align: center; padding: 60px 0;">
    <h1>Welcome to Our Product</h1>
    <p style="font-size: 20px; opacity: 0.8;">The best solution for your needs</p>
    <button>Get Started</button>
  </header>

  <section style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 40px;">
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature One</h3>
      <p>Amazing capability that solves your problem.</p>
    </div>
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature Two</h3>
      <p>Another incredible feature you'll love.</p>
    </div>
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature Three</h3>
      <p>The feature that ties it all together.</p>
    </div>
  </section>
</div>
        """.strip(),
        "css": """
h1 { color: #333; font-size: 48px; }
button { background: #0066ff; color: white; padding: 12px 24px; border-radius: 6px; }
        """.strip(),
        "base_styles": True,
        "scale": 1.0,
        "scroll_y": 0,
        "animate_scroll": False,
        "theme": "light",
        "start_time": 0.0,
        "duration": 5.0,
    },
}
