# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/spacing.py
"""
Spacing and layout tokens for Remotion video design system.

Safe margins, padding scales, and layout tokens optimized for video.
Includes safe zones for LinkedIn/social media feed cropping.
"""

from typing import Any

SPACING_TOKENS: dict[str, Any] = {
    "spacing": {
        "xxs": "4px",  # Minimal spacing
        "xs": "8px",  # Tight spacing
        "sm": "12px",  # Small spacing
        "md": "16px",  # Base spacing unit
        "lg": "24px",  # Medium spacing
        "xl": "32px",  # Large spacing
        "2xl": "48px",  # Extra large spacing
        "3xl": "64px",  # Very large spacing
        "4xl": "80px",  # Huge spacing
        "5xl": "120px",  # Massive spacing
    },
    "safe_margins": {
        "mobile_vertical": {
            "top": "80px",  # Safe zone from top edge
            "bottom": "100px",  # Safe zone from bottom edge (room for mobile UI)
            "description": "Vertical safe zones for 9:16 mobile/story format",
        },
        "mobile_horizontal": {
            "left": "24px",  # Safe zone from left edge
            "right": "24px",  # Safe zone from right edge
            "description": "Horizontal safe zones for mobile screens",
        },
        "linkedin_feed": {
            "top": "40px",  # LinkedIn crops top
            "bottom": "40px",  # LinkedIn crops bottom
            "left": "24px",  # LinkedIn crops left edge
            "right": "24px",  # LinkedIn crops right edge
            "description": "Safe zones for LinkedIn feed crop (recommended 8-24px)",
        },
        "youtube_standard": {
            "top": "20px",  # YouTube standard safe area
            "bottom": "20px",
            "left": "20px",
            "right": "20px",
            "description": "Standard YouTube safe area margins",
        },
        "instagram_square": {
            "all": "32px",  # Instagram 1:1 safe margin
            "description": "Safe margin for Instagram square posts",
        },
        "instagram_story": {
            "top": "100px",  # Story UI overlays
            "bottom": "120px",  # Story CTA/swipe area
            "left": "24px",
            "right": "24px",
            "description": "Safe zones for Instagram Stories (9:16)",
        },
        "tiktok": {
            "top": "100px",  # TikTok top UI
            "bottom": "180px",  # TikTok bottom UI + CTA
            "left": "24px",
            "right": "80px",  # Account for side buttons
            "description": "Safe zones for TikTok (9:16)",
        },
    },
    "border_radius": {
        "none": "0",
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
        "2xl": "24px",
        "3xl": "32px",
        "full": "9999px",  # Fully rounded
    },
    "border_width": {
        "thin": "1px",
        "base": "2px",
        "thick": "4px",
        "heavy": "8px",
    },
    "layout_widths": {
        "content_narrow": "600px",  # Narrow content column
        "content_medium": "900px",  # Medium content column
        "content_wide": "1200px",  # Wide content column
        "chart_small": "500px",  # Small chart/graphic
        "chart_medium": "700px",  # Medium chart
        "chart_large": "900px",  # Large chart
        "full_hd": "1920px",  # Full HD width
        "4k": "3840px",  # 4K width
    },
    "layout_heights": {
        "full_hd": "1080px",  # Full HD height
        "4k": "2160px",  # 4K height
        "vertical_hd": "1920px",  # Vertical video (9:16)
    },
    "z_index": {
        "background": 0,
        "base": 1,
        "content": 10,
        "overlay": 50,
        "modal": 100,
        "toast": 200,
    },
}
