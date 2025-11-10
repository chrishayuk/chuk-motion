# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/brand.py
"""
Brand pack system for white-labeling and client-specific deliverables.

Brand packs enable:
- Logo and asset overrides
- Color palette customization
- Typography overrides
- Intro/outro bumpers
- CTA style variants
- Theme inheritance

This allows MCP servers to load brand packs dynamically per client.
"""

from typing import Any

from pydantic import BaseModel, Field

# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class LogoConfig(BaseModel):
    """Logo configuration."""

    url: str | None = Field(None, description="Logo asset URL or path")
    width: int = Field(..., description="Logo width in px")
    height: int = Field(..., description="Logo height in px")
    position: str = Field(..., description="Logo position (top-left, top-right, center, etc.)")
    scale: float = Field(1.0, description="Scale multiplier (default 1.0)")


class ColorsConfig(BaseModel):
    """Color palette configuration."""

    primary: list[str] = Field(..., description="Gradient steps for primary color")
    secondary: list[str] = Field(..., description="Secondary color gradient")
    accent: list[str] = Field(..., description="Accent color gradient")
    text: str = Field(..., description="Main text color")
    background: str = Field(..., description="Background color")
    success: str = Field(..., description="Success state color")
    warning: str = Field(..., description="Warning state color")
    error: str = Field(..., description="Error state color")


class FontConfig(BaseModel):
    """Font configuration."""

    fonts: list[str] = Field(..., description="Font family list")
    fallback: str = Field(..., description="Fallback font family")


class TypographyConfig(BaseModel):
    """Typography configuration."""

    heading_font: FontConfig
    body_font: FontConfig
    code_font: FontConfig
    font_weights: dict[str, int] = Field(
        default_factory=lambda: {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}
    )


class MotionConfig(BaseModel):
    """Motion overrides configuration."""

    default_spring: str = Field(..., description="Default spring preset name")
    default_easing: str = Field(..., description="Default easing preset name")
    default_tempo: str = Field(..., description="Default tempo preset name")


class AssetsConfig(BaseModel):
    """Brand assets configuration."""

    intro_bumper: str | None = Field(None, description="Path to intro video/animation")
    outro_bumper: str | None = Field(None, description="Path to outro video/animation")
    watermark: str | None = Field(None, description="Path to watermark image")
    background_music: str | None = Field(None, description="Default background music")


class CTAStyleConfig(BaseModel):
    """Call-to-action style configuration."""

    variant: str = Field(..., description="CTA variant (minimal, bold, gradient, neon)")
    position: str = Field(..., description="Default CTA position")
    animation: str = Field(..., description="Enter animation for CTAs")


class PlatformPreferencesConfig(BaseModel):
    """Platform preferences configuration."""

    default_platform: str = Field(
        ..., description="Default platform (youtube_long_form, linkedin, etc.)"
    )
    safe_area_mode: str = Field(
        ..., description="Safe area mode (conservative, standard, aggressive)"
    )
    layout_mode: str = Field(
        ..., description="Layout mode (presentation, feed_grab, mobile_readable)"
    )


class BrandPack(BaseModel):
    """Complete brand pack configuration."""

    name: str = Field(..., description="Brand pack identifier")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Description of brand")
    logo: LogoConfig
    colors: ColorsConfig
    typography: TypographyConfig
    motion: MotionConfig
    assets: AssetsConfig
    cta_style: CTAStyleConfig
    platform_preferences: PlatformPreferencesConfig


# ============================================================================
# DEFAULT BRAND PACKS
# ============================================================================

BRAND_PACKS: dict[str, BrandPack] = {
    # Generic/Default Pack
    "default": BrandPack(
        name="default",
        display_name="Default Brand",
        description="Clean, professional default styling",
        logo=LogoConfig(
            url=None,
            width=200,
            height=60,
            position="top-left",
            scale=1.0,
        ),
        colors=ColorsConfig(
            primary=["#007bff", "#0056b3", "#004085"],
            secondary=["#6c757d", "#5a6268", "#495057"],
            accent=["#ff4081", "#e91e63", "#c2185b"],
            text="#ffffff",
            background="#000000",
            success="#28a745",
            warning="#ffc107",
            error="#dc3545",
        ),
        typography=TypographyConfig(
            heading_font=FontConfig(
                fonts=["Inter", "SF Pro Display", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            body_font=FontConfig(
                fonts=["Inter", "SF Pro Text", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            code_font=FontConfig(
                fonts=["JetBrains Mono", "Fira Code", "Monaco", "monospace"],
                fallback="monospace",
            ),
            font_weights={
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            },
        ),
        motion=MotionConfig(
            default_spring="smooth",
            default_easing="ease_out",
            default_tempo="medium",
        ),
        assets=AssetsConfig(
            intro_bumper=None,
            outro_bumper=None,
            watermark=None,
            background_music=None,
        ),
        cta_style=CTAStyleConfig(
            variant="gradient",
            position="bottom-center",
            animation="scale_in",
        ),
        platform_preferences=PlatformPreferencesConfig(
            default_platform="youtube_long_form",
            safe_area_mode="standard",
            layout_mode="presentation",
        ),
    ),
    # Tech/SaaS Brand
    "tech_startup": BrandPack(
        name="tech_startup",
        display_name="Tech Startup",
        description="Modern, energetic tech brand styling",
        logo=LogoConfig(
            url=None,
            width=180,
            height=50,
            position="top-left",
            scale=1.0,
        ),
        colors=ColorsConfig(
            primary=["#6366f1", "#4f46e5", "#4338ca"],
            secondary=["#8b5cf6", "#7c3aed", "#6d28d9"],
            accent=["#06b6d4", "#0891b2", "#0e7490"],
            text="#f8fafc",
            background="#0f172a",
            success="#10b981",
            warning="#f59e0b",
            error="#ef4444",
        ),
        typography=TypographyConfig(
            heading_font=FontConfig(
                fonts=["Manrope", "Inter", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            body_font=FontConfig(
                fonts=["Inter", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            code_font=FontConfig(
                fonts=["JetBrains Mono", "monospace"],
                fallback="monospace",
            ),
            font_weights={
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            },
        ),
        motion=MotionConfig(
            default_spring="snappy",
            default_easing="ease_out_expo",
            default_tempo="fast",
        ),
        assets=AssetsConfig(
            intro_bumper=None,
            outro_bumper=None,
            watermark=None,
            background_music=None,
        ),
        cta_style=CTAStyleConfig(
            variant="neon",
            position="bottom-center",
            animation="bounce_in",
        ),
        platform_preferences=PlatformPreferencesConfig(
            default_platform="youtube_long_form",
            safe_area_mode="standard",
            layout_mode="presentation",
        ),
    ),
    # Corporate/Enterprise Brand
    "enterprise": BrandPack(
        name="enterprise",
        display_name="Enterprise",
        description="Professional, corporate styling",
        logo=LogoConfig(
            url=None,
            width=200,
            height=60,
            position="top-left",
            scale=1.0,
        ),
        colors=ColorsConfig(
            primary=["#1e40af", "#1e3a8a", "#1e293b"],
            secondary=["#475569", "#334155", "#1e293b"],
            accent=["#0ea5e9", "#0284c7", "#0369a1"],
            text="#f1f5f9",
            background="#0f172a",
            success="#059669",
            warning="#d97706",
            error="#dc2626",
        ),
        typography=TypographyConfig(
            heading_font=FontConfig(
                fonts=["IBM Plex Sans", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            body_font=FontConfig(
                fonts=["IBM Plex Sans", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            code_font=FontConfig(
                fonts=["IBM Plex Mono", "monospace"],
                fallback="monospace",
            ),
            font_weights={
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            },
        ),
        motion=MotionConfig(
            default_spring="smooth",
            default_easing="ease_in_out",
            default_tempo="slow",
        ),
        assets=AssetsConfig(
            intro_bumper=None,
            outro_bumper=None,
            watermark=None,
            background_music=None,
        ),
        cta_style=CTAStyleConfig(
            variant="minimal",
            position="bottom-right",
            animation="fade_up",
        ),
        platform_preferences=PlatformPreferencesConfig(
            default_platform="linkedin",
            safe_area_mode="conservative",
            layout_mode="presentation",
        ),
    ),
    # Creator/Personal Brand
    "creator": BrandPack(
        name="creator",
        display_name="Creator",
        description="Vibrant, personality-driven styling",
        logo=LogoConfig(
            url=None,
            width=120,
            height=120,
            position="top-left",
            scale=0.8,
        ),
        colors=ColorsConfig(
            primary=["#f59e0b", "#f97316", "#ea580c"],
            secondary=["#ec4899", "#db2777", "#be185d"],
            accent=["#8b5cf6", "#7c3aed", "#6d28d9"],
            text="#fef3c7",
            background="#18181b",
            success="#22c55e",
            warning="#eab308",
            error="#f43f5e",
        ),
        typography=TypographyConfig(
            heading_font=FontConfig(
                fonts=["Montserrat", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            body_font=FontConfig(
                fonts=["Open Sans", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            code_font=FontConfig(
                fonts=["Fira Code", "monospace"],
                fallback="monospace",
            ),
            font_weights={
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 800,
            },
        ),
        motion=MotionConfig(
            default_spring="bouncy",
            default_easing="ease_out_back",
            default_tempo="fast",
        ),
        assets=AssetsConfig(
            intro_bumper=None,
            outro_bumper=None,
            watermark=None,
            background_music=None,
        ),
        cta_style=CTAStyleConfig(
            variant="bold",
            position="center",
            animation="zoom_in",
        ),
        platform_preferences=PlatformPreferencesConfig(
            default_platform="youtube_shorts",
            safe_area_mode="standard",
            layout_mode="mobile_readable",
        ),
    ),
    # Education/Tutorial Brand
    "education": BrandPack(
        name="education",
        display_name="Education",
        description="Clear, approachable educational styling",
        logo=LogoConfig(
            url=None,
            width=180,
            height=60,
            position="top-center",
            scale=1.0,
        ),
        colors=ColorsConfig(
            primary=["#3b82f6", "#2563eb", "#1d4ed8"],
            secondary=["#10b981", "#059669", "#047857"],
            accent=["#f59e0b", "#d97706", "#b45309"],
            text="#f9fafb",
            background="#111827",
            success="#34d399",
            warning="#fbbf24",
            error="#f87171",
        ),
        typography=TypographyConfig(
            heading_font=FontConfig(
                fonts=["Nunito", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            body_font=FontConfig(
                fonts=["Nunito Sans", "system-ui", "sans-serif"],
                fallback="sans-serif",
            ),
            code_font=FontConfig(
                fonts=["Source Code Pro", "monospace"],
                fallback="monospace",
            ),
            font_weights={
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            },
        ),
        motion=MotionConfig(
            default_spring="gentle",
            default_easing="ease_out",
            default_tempo="medium",
        ),
        assets=AssetsConfig(
            intro_bumper=None,
            outro_bumper=None,
            watermark=None,
            background_music=None,
        ),
        cta_style=CTAStyleConfig(
            variant="gradient",
            position="bottom-center",
            animation="slide_in_right",
        ),
        platform_preferences=PlatformPreferencesConfig(
            default_platform="youtube_long_form",
            safe_area_mode="standard",
            layout_mode="technical_detail",
        ),
    ),
}


# ============================================================================
# BRAND PACK UTILITIES
# ============================================================================


def get_brand_pack(name: str) -> BrandPack:
    """Get a brand pack by name, fallback to default if not found."""
    return BRAND_PACKS.get(name, BRAND_PACKS["default"])


def merge_brand_pack(base: str, overrides: dict[str, Any]) -> BrandPack:
    """Merge custom overrides into a base brand pack."""
    import copy

    base_pack = copy.deepcopy(get_brand_pack(base))

    # Convert to dict, merge, then back to Pydantic model
    base_dict = base_pack.model_dump()

    def deep_merge(base_dict: dict, override_dict: dict) -> None:
        for key, value in override_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value

    deep_merge(base_dict, overrides)
    return BrandPack(**base_dict)


def list_brand_packs() -> list[dict[str, str]]:
    """List all available brand packs."""
    return [
        {
            "name": pack.name,
            "display_name": pack.display_name,
            "description": pack.description,
        }
        for pack in BRAND_PACKS.values()
    ]
