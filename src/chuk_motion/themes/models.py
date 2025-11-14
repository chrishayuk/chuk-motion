# chuk-motion/src/chuk_motion/themes/models.py
"""
Pydantic models for the theme system.

These models provide type-safe theme definitions that combine
color, typography, motion, and spacing tokens into cohesive
design systems optimized for video content.
"""

from pydantic import BaseModel, Field

from ..tokens.colors import ColorTheme
from ..tokens.motion import DurationConfig, EasingConfig, SpringConfig
from ..tokens.spacing import SpacingTokens
from ..tokens.typography import FontFamily

# ============================================================================
# THEME COMPONENT MODELS
# ============================================================================


class ThemeTypography(BaseModel):
    """Typography configuration for a theme."""

    primary_font: FontFamily = Field(..., description="Primary font for headings and titles")
    body_font: FontFamily = Field(..., description="Body font for general text")
    code_font: FontFamily = Field(..., description="Monospace font for code")
    default_resolution: str = Field(
        default="video_1080p",
        description="Default video resolution (video_1080p, video_4k, video_720p)",
    )


class ThemeMotion(BaseModel):
    """Motion configuration for a theme."""

    default_spring: SpringConfig = Field(..., description="Default spring animation config")
    default_easing: EasingConfig = Field(..., description="Default easing curve")
    default_duration: DurationConfig = Field(..., description="Default animation duration")


# ============================================================================
# MAIN THEME MODEL
# ============================================================================


class Theme(BaseModel):
    """
    Complete theme definition combining all design tokens.

    A theme is a cohesive design system that combines colors, typography,
    motion, and spacing tokens for consistent video production.
    """

    name: str = Field(..., description="Theme display name")
    description: str = Field(..., description="Human-readable theme description")
    colors: ColorTheme = Field(..., description="Color palette for the theme")
    typography: ThemeTypography = Field(..., description="Typography configuration")
    motion: ThemeMotion = Field(..., description="Motion design configuration")
    spacing: SpacingTokens = Field(..., description="Spacing and layout tokens")
    use_cases: list[str] = Field(
        default_factory=list, description="Recommended use cases for this theme"
    )

    class Config:
        """Pydantic configuration."""

        # Allow arbitrary types for complex nested models
        arbitrary_types_allowed = True


# ============================================================================
# THEME COLLECTION MODEL
# ============================================================================


class ThemeCollection(BaseModel):
    """Collection of themes indexed by key."""

    themes: dict[str, Theme] = Field(
        default_factory=dict,
        description="Dictionary of themes indexed by key (e.g., 'tech', 'finance')",
    )

    def get(self, key: str, default: Theme | None = None) -> Theme | None:
        """Get a theme by key with optional default."""
        return self.themes.get(key, default)

    def keys(self) -> list[str]:
        """Get all theme keys."""
        return list(self.themes.keys())

    def values(self) -> list[Theme]:
        """Get all themes."""
        return list(self.themes.values())

    def items(self) -> list[tuple[str, Theme]]:
        """Get all theme key-value pairs."""
        return list(self.themes.items())

    def __getitem__(self, key: str) -> Theme:
        """Allow dictionary-style access."""
        return self.themes[key]

    def __contains__(self, key: str) -> bool:
        """Check if theme key exists."""
        return key in self.themes

    def __len__(self) -> int:
        """Return number of themes in collection."""
        return len(self.themes)

    def __iter__(self):
        """Iterate over theme keys."""
        return iter(self.themes)
