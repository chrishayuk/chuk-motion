# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/typography.py
"""
Typography tokens for Remotion video design system.

Font scales, weights, and families optimized for video readability.
All sizes are tested for legibility at 1080p and 4K resolutions.
"""

from typing import Any

TYPOGRAPHY_TOKENS: dict[str, Any] = {
    "font_families": {
        "display": {
            "name": "Display",
            "fonts": ["Inter", "SF Pro Display", "system-ui", "sans-serif"],
            "description": "Large headings and titles",
            "usage": "Video titles, main headings",
        },
        "body": {
            "name": "Body",
            "fonts": ["Inter", "SF Pro Text", "system-ui", "sans-serif"],
            "description": "Body text and subtitles",
            "usage": "Captions, descriptions, body content",
        },
        "mono": {
            "name": "Monospace",
            "fonts": ["JetBrains Mono", "Fira Code", "Monaco", "monospace"],
            "description": "Code and technical content",
            "usage": "Code blocks, technical text",
        },
        "decorative": {
            "name": "Decorative",
            "fonts": ["Poppins", "Montserrat", "Raleway", "sans-serif"],
            "description": "Special emphasis and style",
            "usage": "Stylized text, special callouts",
        },
    },
    "font_sizes": {
        "video_1080p": {
            "xs": "24px",  # Small captions
            "sm": "32px",  # Regular captions
            "base": "40px",  # Body text
            "lg": "48px",  # Subheadings
            "xl": "64px",  # Headings
            "2xl": "80px",  # Large headings
            "3xl": "96px",  # Title cards
            "4xl": "120px",  # Hero titles
        },
        "video_4k": {
            "xs": "48px",
            "sm": "64px",
            "base": "80px",
            "lg": "96px",
            "xl": "128px",
            "2xl": "160px",
            "3xl": "192px",
            "4xl": "240px",
        },
        "video_720p": {
            "xs": "18px",
            "sm": "24px",
            "base": "30px",
            "lg": "36px",
            "xl": "48px",
            "2xl": "60px",
            "3xl": "72px",
            "4xl": "90px",
        },
    },
    "font_weights": {
        "thin": 100,
        "extralight": 200,
        "light": 300,
        "regular": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700,
        "extrabold": 800,
        "black": 900,
    },
    "line_heights": {
        "tight": 1.1,  # Tight spacing for large headings
        "snug": 1.25,  # Snug spacing for headings
        "normal": 1.5,  # Normal spacing for body text
        "relaxed": 1.75,  # Relaxed for captions
        "loose": 2.0,  # Extra loose for special cases
    },
    "letter_spacing": {
        "tighter": "-0.05em",
        "tight": "-0.025em",
        "normal": "0",
        "wide": "0.025em",
        "wider": "0.05em",
        "widest": "0.1em",
    },
    "text_styles": {
        "hero_title": {
            "fontSize": "4xl",
            "fontWeight": "black",
            "lineHeight": "tight",
            "letterSpacing": "tight",
            "fontFamily": "display",
        },
        "title": {
            "fontSize": "3xl",
            "fontWeight": "bold",
            "lineHeight": "tight",
            "letterSpacing": "tight",
            "fontFamily": "display",
        },
        "heading": {
            "fontSize": "2xl",
            "fontWeight": "semibold",
            "lineHeight": "snug",
            "letterSpacing": "normal",
            "fontFamily": "display",
        },
        "subheading": {
            "fontSize": "xl",
            "fontWeight": "medium",
            "lineHeight": "snug",
            "letterSpacing": "normal",
            "fontFamily": "display",
        },
        "body": {
            "fontSize": "base",
            "fontWeight": "regular",
            "lineHeight": "normal",
            "letterSpacing": "normal",
            "fontFamily": "body",
        },
        "caption": {
            "fontSize": "sm",
            "fontWeight": "medium",
            "lineHeight": "relaxed",
            "letterSpacing": "wide",
            "fontFamily": "body",
        },
        "small": {
            "fontSize": "xs",
            "fontWeight": "regular",
            "lineHeight": "relaxed",
            "letterSpacing": "normal",
            "fontFamily": "body",
        },
    },
}
