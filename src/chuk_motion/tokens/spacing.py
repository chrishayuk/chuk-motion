# chuk-motion/src/chuk_motion/tokens/spacing.py
"""
Spacing, safe areas, and layout tokens for Remotion video design system.

Comprehensive spacing system including:
- Spacing scale
- Safe area / attention zones (platform-specific)
- Border radius and width
- Layout dimensions
- Z-index layers
- Density / layout modes

Critical for multi-platform video generation where UI overlays vary.
"""

from typing import Literal

from pydantic import BaseModel, Field

# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class CriticalZone(BaseModel):
    """Critical zone configuration for platform overlays."""

    top: int | None = None
    bottom: int | None = None
    left: int | None = None
    right: int | None = None
    height: int | None = None
    width: int | None = None


class SafeAreaConfig(BaseModel):
    """Safe area configuration for a platform."""

    top: int = Field(..., description="Top safe area padding in pixels")
    bottom: int = Field(..., description="Bottom safe area padding in pixels")
    left: int = Field(..., description="Left safe area padding in pixels")
    right: int = Field(..., description="Right safe area padding in pixels")
    critical_zones: dict[str, CriticalZone] | None = Field(
        default=None, description="Platform-specific critical zones"
    )
    description: str = Field(..., description="Description of safe area")
    aspect_ratio: str = Field(..., description="Recommended aspect ratio")
    usage: str | None = Field(default=None, description="Usage recommendations")
    ui_overlays: list[str] | None = Field(default=None, description="Platform UI overlays")
    notes: str | None = Field(default=None, description="Additional notes")


class AttentionZone(BaseModel):
    """Attention zone configuration."""

    description: str
    horizontal_start: str | None = None
    horizontal_end: str | None = None
    vertical_start: str | None = None
    vertical_end: str | None = None
    intersections: list[dict[str, str]] | None = None
    top: str | None = None
    bottom: str | None = None
    usage: str | None = None


class LayoutModeCharacteristics(BaseModel):
    """Characteristics of a layout mode."""

    spacing_multiplier: float
    font_size_multiplier: float
    content_density: Literal["very_low", "low", "medium", "high", "very_high"]
    recommended_tempo: str
    safe_area_multiplier: float


class LayoutModeConfig(BaseModel):
    """Layout mode configuration."""

    name: str
    description: str
    characteristics: LayoutModeCharacteristics
    usage: str
    target_platforms: list[str]
    feel: str


class SpacingTokens(BaseModel):
    """Complete spacing token system."""

    spacing: dict[str, str]
    safe_area: dict[str, SafeAreaConfig]
    attention_zone: dict[str, AttentionZone]
    layout_mode: dict[str, LayoutModeConfig]
    border_radius: dict[str, str]
    border_width: dict[str, str]
    layout_widths: dict[str, str]
    layout_heights: dict[str, str]
    z_index: dict[str, int]


# ============================================================================
# SPACING TOKENS DATA
# ============================================================================

SPACING_TOKENS = SpacingTokens(
    # ============================================================================
    # SPACING SCALE - Base spacing units
    # ============================================================================
    spacing={
        "none": "0",
        "xxs": "4px",
        "xs": "8px",
        "sm": "12px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
        "2xl": "48px",
        "3xl": "64px",
        "4xl": "80px",
        "5xl": "120px",
        "6xl": "160px",
        "7xl": "200px",
    },
    # ============================================================================
    # SAFE AREAS / ATTENTION ZONES - Platform-specific cropping
    # ============================================================================
    safe_area={
        "desktop": SafeAreaConfig(
            top=64,
            bottom=64,
            left=96,
            right=96,
            description="Desktop/presentation safe zone",
            aspect_ratio="16:9",
            usage="YouTube desktop, standard presentations",
        ),
        "mobile": SafeAreaConfig(
            top=96,
            bottom=144,
            left=64,
            right=64,
            description="Mobile vertical safe zone",
            aspect_ratio="9:16",
            usage="Stories, Shorts, Reels",
        ),
        "youtube_long_form": SafeAreaConfig(
            top=60,
            bottom=60,
            left=80,
            right=80,
            critical_zones={
                "title_safe": CriticalZone(top=100, bottom=100, left=120, right=120),
                "action_safe": CriticalZone(top=60, bottom=60, left=80, right=80),
            },
            description="YouTube desktop player safe zones",
            aspect_ratio="16:9",
            ui_overlays=["player controls (bottom 80px)", "recommended videos (right side)"],
        ),
        "youtube_shorts": SafeAreaConfig(
            top=120,
            bottom=200,
            left=48,
            right=48,
            critical_zones={
                "header": CriticalZone(top=0, height=120),
                "controls": CriticalZone(bottom=0, height=200),
                "swipe_zone": CriticalZone(bottom=200, height=100),
            },
            description="YouTube Shorts safe zones",
            aspect_ratio="9:16",
            ui_overlays=["top bar (120px)", "bottom controls (200px)"],
        ),
        "tiktok": SafeAreaConfig(
            top=100,
            bottom=180,
            left=24,
            right=80,
            critical_zones={
                "top_bar": CriticalZone(top=0, height=100),
                "side_controls": CriticalZone(right=0, width=80, top=200, bottom=300),
                "bottom_info": CriticalZone(bottom=0, height=180),
                "caption_zone": CriticalZone(bottom=180, height=100, left=24, right=80),
            },
            description="TikTok UI safe zones",
            aspect_ratio="9:16",
            ui_overlays=[
                "top info (100px)",
                "right controls (80px)",
                "bottom caption + CTA (180px)",
            ],
        ),
        "instagram_reel": SafeAreaConfig(
            top=120,
            bottom=160,
            left=32,
            right=32,
            critical_zones={
                "top_bar": CriticalZone(top=0, height=120),
                "bottom_controls": CriticalZone(bottom=0, height=160),
                "swipe_up": CriticalZone(bottom=160, height=80),
            },
            description="Instagram Reels safe zones",
            aspect_ratio="9:16",
            ui_overlays=["top bar (120px)", "bottom controls (160px)"],
        ),
        "instagram_story": SafeAreaConfig(
            top=100,
            bottom=120,
            left=24,
            right=24,
            critical_zones={
                "progress_bar": CriticalZone(top=0, height=40),
                "profile_info": CriticalZone(top=40, height=60),
                "reply_bar": CriticalZone(bottom=0, height=80),
                "swipe_up": CriticalZone(bottom=80, height=40),
            },
            description="Instagram Story safe zones",
            aspect_ratio="9:16",
            ui_overlays=["top progress (100px)", "bottom CTA/swipe (120px)"],
        ),
        "linkedin": SafeAreaConfig(
            top=40,
            bottom=40,
            left=24,
            right=24,
            critical_zones={
                "crop_safe": CriticalZone(top=40, bottom=40, left=24, right=24),
                "title_safe": CriticalZone(top=60, bottom=60, left=40, right=40),
            },
            description="LinkedIn feed safe zones (important for cropping)",
            aspect_ratio="16:9 or 1:1",
            ui_overlays=["feed crops aggressively (40px all sides)"],
            notes="LinkedIn often crops content in feed - be conservative",
        ),
        "twitter": SafeAreaConfig(
            top=32,
            bottom=32,
            left=32,
            right=32,
            critical_zones={
                "timeline_safe": CriticalZone(top=32, bottom=32, left=32, right=32),
            },
            description="Twitter/X safe zones",
            aspect_ratio="16:9 or 1:1",
            ui_overlays=["minimal UI overlay"],
        ),
        "presentation": SafeAreaConfig(
            top=80,
            bottom=80,
            left=120,
            right=120,
            critical_zones={
                "title_safe": CriticalZone(top=100, bottom=100, left=150, right=150),
                "action_safe": CriticalZone(top=80, bottom=80, left=120, right=120),
            },
            description="Presentation/slide safe zones",
            aspect_ratio="16:9",
            usage="Keynote, PowerPoint, Google Slides",
            notes="Conservative margins for projector cutoff",
        ),
        "square": SafeAreaConfig(
            top=32,
            bottom=32,
            left=32,
            right=32,
            description="Square format safe zones",
            aspect_ratio="1:1",
            usage="Instagram feed, LinkedIn square posts",
        ),
        "ultrawide": SafeAreaConfig(
            top=40,
            bottom=40,
            left=160,
            right=160,
            description="Ultra-wide cinematic safe zones",
            aspect_ratio="21:9",
            usage="Cinematic content, wide presentations",
        ),
    },
    # ============================================================================
    # ATTENTION ZONES - Where viewer's eyes naturally focus
    # ============================================================================
    attention_zone={
        "center_third": AttentionZone(
            description="Central third of screen - primary attention area",
            horizontal_start="33.33%",
            horizontal_end="66.67%",
            vertical_start="33.33%",
            vertical_end="66.67%",
            usage="Place key information, CTAs, primary content",
        ),
        "rule_of_thirds": AttentionZone(
            description="Rule of thirds grid intersections",
            intersections=[
                {"x": "33.33%", "y": "33.33%"},
                {"x": "66.67%", "y": "33.33%"},
                {"x": "33.33%", "y": "66.67%"},
                {"x": "66.67%", "y": "66.67%"},
            ],
            usage="Position focal points, important elements",
        ),
        "lower_third": AttentionZone(
            description="Bottom third - traditional broadcast zone",
            top="66.67%",
            bottom="100%",
            usage="Captions, lower thirds, channel info",
        ),
        "upper_banner": AttentionZone(
            description="Top banner zone",
            top="0%",
            bottom="15%",
            usage="Headers, titles, alerts",
        ),
    },
    # ============================================================================
    # LAYOUT MODES / DENSITY - Platform-specific layout approaches
    # ============================================================================
    layout_mode={
        "presentation": LayoutModeConfig(
            name="Presentation",
            description="Large negative space, slower motion, readable from distance",
            characteristics=LayoutModeCharacteristics(
                spacing_multiplier=1.5,
                font_size_multiplier=1.3,
                content_density="low",
                recommended_tempo="slow",
                safe_area_multiplier=1.2,
            ),
            usage="YouTube desktop, business presentations, educational content",
            target_platforms=["youtube_long_form", "presentation"],
            feel="Professional, spacious, easy to read",
        ),
        "feed_grab": LayoutModeConfig(
            name="Feed Grab",
            description="Big headlines, tighter spacing, attention-grabbing",
            characteristics=LayoutModeCharacteristics(
                spacing_multiplier=0.8,
                font_size_multiplier=1.5,
                content_density="high",
                recommended_tempo="fast",
                safe_area_multiplier=0.8,
            ),
            usage="LinkedIn feed, social media thumbnails, scroll-stopping content",
            target_platforms=["linkedin", "twitter", "instagram_reel"],
            feel="Bold, punchy, eye-catching",
        ),
        "mobile_readable": LayoutModeConfig(
            name="Mobile Readable",
            description="Very large type, progressive captions, thumb-friendly",
            characteristics=LayoutModeCharacteristics(
                spacing_multiplier=1.0,
                font_size_multiplier=1.8,
                content_density="very_low",
                recommended_tempo="fast",
                safe_area_multiplier=1.5,
            ),
            usage="Shorts, Reels, TikTok, Stories",
            target_platforms=[
                "youtube_shorts",
                "tiktok",
                "instagram_reel",
                "instagram_story",
            ],
            feel="Mobile-first, thumb-stopping, easy to scan",
        ),
        "technical_detail": LayoutModeConfig(
            name="Technical Detail",
            description="Code, diagrams, data - needs space and time",
            characteristics=LayoutModeCharacteristics(
                spacing_multiplier=1.2,
                font_size_multiplier=1.0,
                content_density="medium",
                recommended_tempo="slow",
                safe_area_multiplier=1.0,
            ),
            usage="Code walkthroughs, technical tutorials, data visualization",
            target_platforms=["youtube_long_form", "presentation"],
            feel="Methodical, clear, detailed",
        ),
    },
    # ============================================================================
    # BORDER TOKENS
    # ============================================================================
    border_radius={
        "none": "0",
        "xs": "2px",
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
        "2xl": "24px",
        "3xl": "32px",
        "full": "9999px",
    },
    border_width={
        "none": "0",
        "thin": "1px",
        "base": "2px",
        "thick": "4px",
        "heavy": "8px",
        "ultra": "12px",
    },
    # ============================================================================
    # LAYOUT DIMENSIONS
    # ============================================================================
    layout_widths={
        "content_narrow": "600px",
        "content_medium": "900px",
        "content_wide": "1200px",
        "content_ultra_wide": "1600px",
        "chart_small": "500px",
        "chart_medium": "700px",
        "chart_large": "900px",
        "chart_full": "1400px",
        "full_hd": "1920px",
        "qhd": "2560px",
        "4k": "3840px",
    },
    layout_heights={
        "full_hd": "1080px",
        "vertical_hd": "1920px",
        "qhd": "1440px",
        "4k": "2160px",
        "square_hd": "1080px",
    },
    # ============================================================================
    # Z-INDEX LAYERS
    # ============================================================================
    z_index={
        "underground": -10,
        "background": 0,
        "base": 1,
        "content": 10,
        "elevated": 20,
        "overlay": 50,
        "dropdown": 75,
        "modal": 100,
        "toast": 200,
        "tooltip": 300,
        "debug": 9999,
    },
)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_safe_area(platform: str) -> SafeAreaConfig:
    """Get safe area config by platform, fallback to 'desktop' if not found."""
    return SPACING_TOKENS.safe_area.get(platform, SPACING_TOKENS.safe_area["desktop"])


def get_layout_mode(mode: str) -> LayoutModeConfig:
    """Get layout mode config by name, fallback to 'presentation' if not found."""
    return SPACING_TOKENS.layout_mode.get(mode, SPACING_TOKENS.layout_mode["presentation"])


def list_platforms() -> list[str]:
    """List all available platform safe area configs."""
    return list(SPACING_TOKENS.safe_area.keys())


def list_layout_modes() -> list[str]:
    """List all available layout modes."""
    return list(SPACING_TOKENS.layout_mode.keys())


def get_spacing(size: str) -> str:
    """Get spacing value by size, fallback to 'md' if not found."""
    return SPACING_TOKENS.spacing.get(size, SPACING_TOKENS.spacing["md"])


def get_border_radius(size: str) -> str:
    """Get border radius by size, fallback to 'md' if not found."""
    return SPACING_TOKENS.border_radius.get(size, SPACING_TOKENS.border_radius["md"])


def get_border_width(size: str) -> str:
    """Get border width by size, fallback to 'base' if not found."""
    return SPACING_TOKENS.border_width.get(size, SPACING_TOKENS.border_width["base"])


def get_z_index(layer: str) -> int:
    """Get z-index value by layer name, fallback to 'base' if not found."""
    return SPACING_TOKENS.z_index.get(layer, SPACING_TOKENS.z_index["base"])
