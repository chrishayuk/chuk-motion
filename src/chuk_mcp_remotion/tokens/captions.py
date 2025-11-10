# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/captions.py
"""
Caption style system for platform-specific caption designs.

Caption styles enable:
- Platform-specific caption formatting (MrBeast, Kurzgesagt, LinkedIn, etc.)
- Transition animations
- Highlight styles
- Background styles
- Word-by-word vs. full-line display
- Scale and positioning presets

Critical for auto-generated captions that match platform best practices.
"""

from typing import Literal

from pydantic import BaseModel, Field

# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class TypographyConfig(BaseModel):
    """Typography configuration for captions."""

    font_family: list[str] = Field(..., description="Font family list with fallbacks")
    font_weight: int = Field(..., description="Font weight (100-900)")
    font_size: int = Field(..., description="Font size in px")
    text_transform: Literal["none", "uppercase", "lowercase", "capitalize"] = Field(
        ..., description="Text transformation"
    )
    letter_spacing: str = Field(..., description="Letter spacing (e.g., '0.05em')")
    line_height: float = Field(..., description="Line height multiplier")


class ColorsConfig(BaseModel):
    """Colors configuration for captions."""

    text: str = Field(..., description="Text color")
    stroke: str | None = Field(None, description="Text stroke color")
    stroke_width: int = Field(0, description="Stroke width in px")
    shadow: str = Field(..., description="Text shadow CSS")


class BackgroundConfig(BaseModel):
    """Background configuration for captions."""

    enabled: bool = Field(..., description="Whether background is enabled")
    style: Literal["pill", "box", "none", "gradient"] = Field(..., description="Background style")
    color: str = Field(..., description="Background color or gradient")
    padding: str = Field(..., description="Padding CSS")
    border_radius: str = Field(..., description="Border radius CSS")
    blur: int = Field(0, description="Backdrop blur in px")
    border: str | None = Field(default=None, description="Border CSS")


class PositionConfig(BaseModel):
    """Position configuration for captions."""

    vertical: Literal["top", "center", "bottom", "lower_third"] = Field(
        ..., description="Vertical position"
    )
    horizontal: Literal["left", "center", "right"] = Field(..., description="Horizontal position")
    offset_y: int = Field(0, description="Vertical offset in px")


class AnimationConfig(BaseModel):
    """Animation configuration for captions."""

    enter: str = Field(..., description="Enter animation name")
    exit: str = Field(..., description="Exit animation name")
    enter_duration: float = Field(..., description="Enter duration in seconds")
    exit_duration: float = Field(..., description="Exit duration in seconds")
    scale_emphasis: float = Field(1.0, description="Scale multiplier for emphasis")


class HighlightConfig(BaseModel):
    """Highlight configuration for captions."""

    enabled: bool = Field(..., description="Whether highlighting is enabled")
    trigger: Literal["emphasis", "keywords", "all", "none"] = Field(
        ..., description="What triggers highlighting"
    )
    color: str = Field(..., description="Highlight text color")
    background: str = Field(..., description="Highlight background color")
    scale: float = Field(1.0, description="Scale multiplier for highlighted words")
    animation: str = Field(..., description="Highlight animation name")


class CaptionStyle(BaseModel):
    """Complete caption style configuration."""

    name: str = Field(..., description="Style identifier")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Description of style")
    display_mode: Literal["word_by_word", "phrase_by_phrase", "line_by_line", "full_sentence"] = (
        Field(..., description="Caption display mode")
    )
    words_per_burst: int | None = Field(
        default=None, description="Words per burst (for word_by_word)"
    )
    words_per_phrase: int | None = Field(
        default=None, description="Words per phrase (for phrase_by_phrase)"
    )
    words_per_line: int | None = Field(
        default=None, description="Words per line (for line_by_line)"
    )
    words_per_sentence: int | None = Field(
        default=None, description="Words per sentence (for full_sentence)"
    )
    word_duration: float | None = Field(default=None, description="Duration per word in seconds")
    phrase_duration: float | None = Field(
        default=None, description="Duration per phrase in seconds"
    )
    line_duration: float | None = Field(default=None, description="Duration per line in seconds")
    sentence_duration: float | None = Field(
        default=None, description="Duration per sentence in seconds"
    )
    gap_duration: float = Field(..., description="Gap between captions in seconds")
    typography: TypographyConfig
    colors: ColorsConfig
    background: BackgroundConfig
    position: PositionConfig
    animation: AnimationConfig
    highlight: HighlightConfig
    platform_optimized: list[str] = Field(..., description="Platforms optimized for")
    recommended_tempo: str = Field(..., description="Recommended tempo token")


# ============================================================================
# CAPTION STYLE PRESETS
# ============================================================================

CAPTION_STYLES: dict[str, CaptionStyle] = {
    # MrBeast / Ali Abdaal - Burst Caption Style
    "burst": CaptionStyle(
        name="burst",
        display_name="Burst Captions",
        description="Word-by-word burst captions (MrBeast, Ali Abdaal style)",
        display_mode="word_by_word",
        words_per_burst=1,
        word_duration=0.3,
        gap_duration=0.05,
        typography=TypographyConfig(
            font_family=["Montserrat", "Impact", "Arial Black", "sans-serif"],
            font_weight=900,
            font_size=72,
            text_transform="uppercase",
            letter_spacing="0.05em",
            line_height=1.2,
        ),
        colors=ColorsConfig(
            text="#ffffff",
            stroke="#000000",
            stroke_width=8,
            shadow="0 4px 8px rgba(0,0,0,0.8)",
        ),
        background=BackgroundConfig(
            enabled=True,
            style="pill",
            color="rgba(0, 0, 0, 0.8)",
            padding="8px 24px",
            border_radius="1000px",
            blur=0,
        ),
        position=PositionConfig(
            vertical="center",
            horizontal="center",
            offset_y=0,
        ),
        animation=AnimationConfig(
            enter="scale_in",
            exit="scale_out",
            enter_duration=0.15,
            exit_duration=0.1,
            scale_emphasis=1.15,
        ),
        highlight=HighlightConfig(
            enabled=True,
            trigger="emphasis",
            color="#ffff00",
            background="rgba(255, 255, 0, 0.3)",
            scale=1.2,
            animation="bounce",
        ),
        platform_optimized=["tiktok", "youtube_shorts", "instagram_reel"],
        recommended_tempo="fast",
    ),
    # Kurzgesagt - Precise Sync Captions
    "precise": CaptionStyle(
        name="precise",
        display_name="Precise Sync",
        description="Precisely timed full-line captions (Kurzgesagt style)",
        display_mode="phrase_by_phrase",
        words_per_phrase=5,
        phrase_duration=2.5,
        gap_duration=0.2,
        typography=TypographyConfig(
            font_family=["Lato", "Open Sans", "sans-serif"],
            font_weight=700,
            font_size=42,
            text_transform="none",
            letter_spacing="0.02em",
            line_height=1.4,
        ),
        colors=ColorsConfig(
            text="#ffffff",
            stroke="#000000",
            stroke_width=3,
            shadow="0 2px 4px rgba(0,0,0,0.5)",
        ),
        background=BackgroundConfig(
            enabled=True,
            style="box",
            color="rgba(0, 0, 0, 0.85)",
            padding="12px 24px",
            border_radius="8px",
            blur=4,
        ),
        position=PositionConfig(
            vertical="bottom",
            horizontal="center",
            offset_y=120,
        ),
        animation=AnimationConfig(
            enter="fade_up",
            exit="fade_out",
            enter_duration=0.3,
            exit_duration=0.2,
            scale_emphasis=1.0,
        ),
        highlight=HighlightConfig(
            enabled=True,
            trigger="keywords",
            color="#ffd700",
            background="none",
            scale=1.0,
            animation="none",
        ),
        platform_optimized=["youtube_long_form", "presentation"],
        recommended_tempo="medium",
    ),
    # LinkedIn - Professional Headline Captions
    "headline": CaptionStyle(
        name="headline",
        display_name="Headline Blocks",
        description="Bold headline-style caption blocks (LinkedIn style)",
        display_mode="line_by_line",
        words_per_line=6,
        line_duration=3.0,
        gap_duration=0.3,
        typography=TypographyConfig(
            font_family=["Inter", "SF Pro Display", "system-ui", "sans-serif"],
            font_weight=800,
            font_size=56,
            text_transform="uppercase",
            letter_spacing="0.03em",
            line_height=1.3,
        ),
        colors=ColorsConfig(
            text="#ffffff",
            stroke=None,
            stroke_width=0,
            shadow="0 8px 16px rgba(0,0,0,0.4)",
        ),
        background=BackgroundConfig(
            enabled=True,
            style="gradient",
            color="linear-gradient(135deg, rgba(79, 70, 229, 0.9), rgba(139, 92, 246, 0.9))",
            padding="16px 32px",
            border_radius="12px",
            blur=0,
        ),
        position=PositionConfig(
            vertical="center",
            horizontal="center",
            offset_y=0,
        ),
        animation=AnimationConfig(
            enter="slide_in_left",
            exit="slide_out_right",
            enter_duration=0.5,
            exit_duration=0.3,
            scale_emphasis=1.0,
        ),
        highlight=HighlightConfig(
            enabled=False,
            trigger="none",
            color="#ffffff",
            background="none",
            scale=1.0,
            animation="none",
        ),
        platform_optimized=["linkedin", "twitter", "instagram_reel"],
        recommended_tempo="medium",
    ),
    # Minimal / Subtle - Clean Professional
    "minimal": CaptionStyle(
        name="minimal",
        display_name="Minimal Clean",
        description="Minimal, clean captions for professional content",
        display_mode="full_sentence",
        words_per_sentence=12,
        sentence_duration=4.0,
        gap_duration=0.5,
        typography=TypographyConfig(
            font_family=["Inter", "system-ui", "sans-serif"],
            font_weight=600,
            font_size=36,
            text_transform="none",
            letter_spacing="0.01em",
            line_height=1.5,
        ),
        colors=ColorsConfig(
            text="#f8fafc",
            stroke=None,
            stroke_width=0,
            shadow="0 2px 8px rgba(0,0,0,0.3)",
        ),
        background=BackgroundConfig(
            enabled=True,
            style="box",
            color="rgba(15, 23, 42, 0.7)",
            padding="10px 20px",
            border_radius="6px",
            blur=8,
        ),
        position=PositionConfig(
            vertical="bottom",
            horizontal="center",
            offset_y=100,
        ),
        animation=AnimationConfig(
            enter="fade_in",
            exit="fade_out",
            enter_duration=0.4,
            exit_duration=0.3,
            scale_emphasis=1.0,
        ),
        highlight=HighlightConfig(
            enabled=False,
            trigger="none",
            color="#ffffff",
            background="none",
            scale=1.0,
            animation="none",
        ),
        platform_optimized=["youtube_long_form", "presentation", "linkedin"],
        recommended_tempo="slow",
    ),
    # Neon / Gaming - High Energy
    "neon": CaptionStyle(
        name="neon",
        display_name="Neon Gaming",
        description="High-energy neon captions for gaming/tech content",
        display_mode="word_by_word",
        words_per_burst=2,
        word_duration=0.4,
        gap_duration=0.1,
        typography=TypographyConfig(
            font_family=["Orbitron", "Rajdhani", "sans-serif"],
            font_weight=800,
            font_size=64,
            text_transform="uppercase",
            letter_spacing="0.1em",
            line_height=1.2,
        ),
        colors=ColorsConfig(
            text="#00ff9f",
            stroke="#00ff9f",
            stroke_width=2,
            shadow="0 0 20px #00ff9f, 0 0 40px #00ff9f",
        ),
        background=BackgroundConfig(
            enabled=True,
            style="box",
            color="rgba(0, 0, 0, 0.9)",
            padding="12px 24px",
            border_radius="4px",
            blur=0,
            border="2px solid #00ff9f",
        ),
        position=PositionConfig(
            vertical="top",
            horizontal="center",
            offset_y=120,
        ),
        animation=AnimationConfig(
            enter="zoom_in",
            exit="zoom_out",
            enter_duration=0.2,
            exit_duration=0.15,
            scale_emphasis=1.3,
        ),
        highlight=HighlightConfig(
            enabled=True,
            trigger="emphasis",
            color="#ff0080",
            background="none",
            scale=1.4,
            animation="pulse",
        ),
        platform_optimized=["tiktok", "youtube_shorts", "twitch"],
        recommended_tempo="sprint",
    ),
    # Vintage / Documentary
    "classic": CaptionStyle(
        name="classic",
        display_name="Classic Documentary",
        description="Classic documentary-style captions",
        display_mode="full_sentence",
        words_per_sentence=15,
        sentence_duration=5.0,
        gap_duration=0.8,
        typography=TypographyConfig(
            font_family=["Georgia", "Times New Roman", "serif"],
            font_weight=400,
            font_size=38,
            text_transform="none",
            letter_spacing="0em",
            line_height=1.6,
        ),
        colors=ColorsConfig(
            text="#f5f5dc",
            stroke=None,
            stroke_width=0,
            shadow="2px 2px 4px rgba(0,0,0,0.8)",
        ),
        background=BackgroundConfig(
            enabled=False,
            style="none",
            color="transparent",
            padding="0",
            border_radius="0",
            blur=0,
        ),
        position=PositionConfig(
            vertical="bottom",
            horizontal="center",
            offset_y=80,
        ),
        animation=AnimationConfig(
            enter="fade_in",
            exit="fade_out",
            enter_duration=0.8,
            exit_duration=0.6,
            scale_emphasis=1.0,
        ),
        highlight=HighlightConfig(
            enabled=False,
            trigger="none",
            color="#ffffff",
            background="none",
            scale=1.0,
            animation="none",
        ),
        platform_optimized=["youtube_long_form", "presentation"],
        recommended_tempo="cinematic",
    ),
}


# ============================================================================
# CAPTION UTILITIES
# ============================================================================


def get_caption_style(name: str) -> CaptionStyle:
    """Get a caption style by name, fallback to minimal if not found."""
    return CAPTION_STYLES.get(name, CAPTION_STYLES["minimal"])


def get_style_for_platform(platform: str) -> str:
    """Get recommended caption style for a platform."""
    platform_map = {
        "tiktok": "burst",
        "youtube_shorts": "burst",
        "instagram_reel": "headline",
        "instagram_story": "burst",
        "youtube_long_form": "precise",
        "linkedin": "headline",
        "twitter": "headline",
        "presentation": "minimal",
        "twitch": "neon",
    }
    return platform_map.get(platform, "minimal")


def list_caption_styles() -> list[dict[str, str]]:
    """List all available caption styles."""
    return [
        {
            "name": style.name,
            "display_name": style.display_name,
            "description": style.description,
            "display_mode": style.display_mode,
            "recommended_tempo": style.recommended_tempo,
        }
        for style in CAPTION_STYLES.values()
    ]
