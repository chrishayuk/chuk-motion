# chuk-motion/src/chuk_motion/tokens/colors.py
"""
Color tokens for Remotion video design system.

Organized by theme, optimized for video content and YouTube.
All colors are tested for readability and visual impact on screen.
"""

from pydantic import BaseModel, Field


# Background Color Model
class BackgroundColors(BaseModel):
    """Background color variants."""

    dark: str
    light: str
    glass: str
    darker: str = "rgba(20, 25, 40, 0.98)"
    overlay: str = "rgba(0, 0, 0, 0.5)"
    hacker: str = "rgba(0, 0, 0, 0.95)"


# Text Color Model
class TextColors(BaseModel):
    """Text color variants for different backgrounds."""

    on_dark: str
    on_light: str
    muted: str
    dimmed: str = "rgba(255, 255, 255, 0.3)"


# Semantic Color Model
class SemanticColors(BaseModel):
    """Semantic colors for UI feedback."""

    success: str
    warning: str
    error: str
    info: str


# Border Color Model
class BorderColors(BaseModel):
    """Border color variants with different opacities."""

    subtle: str = "rgba(255, 255, 255, 0.1)"
    light: str = "rgba(255, 255, 255, 0.2)"
    medium: str = "rgba(255, 255, 255, 0.3)"
    strong: str = "rgba(255, 255, 255, 0.4)"


# Shadow Color Model
class ShadowColors(BaseModel):
    """Shadow color variants."""

    light: str = "rgba(0, 0, 0, 0.2)"
    medium: str = "rgba(0, 0, 0, 0.3)"
    dark: str = "rgba(0, 0, 0, 0.5)"


# Highlight Color Model
class HighlightColors(BaseModel):
    """Highlight colors for code and UI."""

    line: str = "rgba(255, 255, 255, 0.2)"


# Gradient Color Model
class GradientColors(BaseModel):
    """Gradient variants."""

    bold: str = ""  # Will be set per theme
    primary_to_secondary: str = ""  # Will be set per theme


# Effect Color Model
class EffectColors(BaseModel):
    """Special effect colors for animations and glitches."""

    glitch_red: str = "#FF0000"  # RGB split red channel
    glitch_cyan: str = "#00FFFF"  # RGB split cyan channel
    scanline: str = "rgba(0, 0, 0, 0.1)"  # CRT scanline overlay
    noise: str = "rgba(255, 255, 255, 0.05)"  # Static noise overlay


# Color Theme Model
class ColorTheme(BaseModel):
    """A complete color theme."""

    name: str
    description: str
    primary: list[str] = Field(description="Primary color scale (3 variants)")
    accent: list[str] = Field(description="Accent color scale (3 variants)")
    gradient: str
    background: BackgroundColors
    text: TextColors
    semantic: SemanticColors
    border: BorderColors = Field(default_factory=BorderColors)
    shadow: ShadowColors = Field(default_factory=ShadowColors)
    highlight: HighlightColors = Field(default_factory=HighlightColors)
    effects: EffectColors = Field(default_factory=EffectColors)


# Color Tokens Model
class ColorTokens(BaseModel):
    """All color themes."""

    tech: ColorTheme = Field(
        default=ColorTheme(
            name="Tech",
            description="Modern tech aesthetic with blue/cyan palette",
            primary=["#0066FF", "#0052CC", "#003D99"],
            accent=["#00D9FF", "#00B8D4", "#0097A7"],
            gradient="linear-gradient(135deg, #0066FF 0%, #00D9FF 100%)",
            background=BackgroundColors(
                dark="#0A0E1A", light="#F5F7FA", glass="rgba(10, 14, 26, 0.85)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#1A1A1A", muted="#8B92A4"),
            semantic=SemanticColors(
                success="#00C853", warning="#FFB300", error="#FF3D00", info="#00B8D4"
            ),
        )
    )
    finance: ColorTheme = Field(
        default=ColorTheme(
            name="Finance",
            description="Professional finance theme with green/gold",
            primary=["#00C853", "#00A843", "#008833"],
            accent=["#FFD600", "#FFAB00", "#FF6F00"],
            gradient="linear-gradient(135deg, #00C853 0%, #FFD600 100%)",
            background=BackgroundColors(
                dark="#0D1B0D", light="#F8FAF8", glass="rgba(13, 27, 13, 0.85)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#1A1A1A", muted="#7A8A7A"),
            semantic=SemanticColors(
                success="#00C853", warning="#FFB300", error="#D32F2F", info="#1976D2"
            ),
        )
    )
    education: ColorTheme = Field(
        default=ColorTheme(
            name="Education",
            description="Friendly education theme with purple/orange",
            primary=["#7C4DFF", "#651FFF", "#6200EA"],
            accent=["#FF6E40", "#FF5722", "#F4511E"],
            gradient="linear-gradient(135deg, #7C4DFF 0%, #FF6E40 100%)",
            background=BackgroundColors(
                dark="#1A0F2E", light="#FAF7FC", glass="rgba(26, 15, 46, 0.85)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#1A1A1A", muted="#9B8AA9"),
            semantic=SemanticColors(
                success="#4CAF50", warning="#FF9800", error="#F44336", info="#7C4DFF"
            ),
        )
    )
    lifestyle: ColorTheme = Field(
        default=ColorTheme(
            name="Lifestyle",
            description="Warm lifestyle theme with coral/pink",
            primary=["#FF6B9D", "#E91E63", "#C2185B"],
            accent=["#FFB74D", "#FFA726", "#FF9800"],
            gradient="linear-gradient(135deg, #FF6B9D 0%, #FFB74D 100%)",
            background=BackgroundColors(
                dark="#2E1A26", light="#FFF9FA", glass="rgba(46, 26, 38, 0.85)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#2E1A26", muted="#B39AA6"),
            semantic=SemanticColors(
                success="#66BB6A", warning="#FFA726", error="#EF5350", info="#29B6F6"
            ),
        )
    )
    gaming: ColorTheme = Field(
        default=ColorTheme(
            name="Gaming",
            description="High-energy gaming theme with neon accents",
            primary=["#00E676", "#00C853", "#00BFA5"],
            accent=["#E040FB", "#D500F9", "#AA00FF"],
            gradient="linear-gradient(135deg, #00E676 0%, #E040FB 100%)",
            background=BackgroundColors(
                dark="#0F0F1A", light="#F0F0F5", glass="rgba(15, 15, 26, 0.9)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#1A1A1A", muted="#8B8BA0"),
            semantic=SemanticColors(
                success="#00E676", warning="#FFD740", error="#FF1744", info="#00E5FF"
            ),
        )
    )
    minimal: ColorTheme = Field(
        default=ColorTheme(
            name="Minimal",
            description="Clean minimal theme with monochrome palette",
            primary=["#212121", "#424242", "#616161"],
            accent=["#FFFFFF", "#F5F5F5", "#EEEEEE"],
            gradient="linear-gradient(135deg, #212121 0%, #616161 100%)",
            background=BackgroundColors(
                dark="#000000", light="#FFFFFF", glass="rgba(0, 0, 0, 0.8)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#000000", muted="#757575"),
            semantic=SemanticColors(
                success="#4CAF50", warning="#FFC107", error="#F44336", info="#2196F3"
            ),
        )
    )
    business: ColorTheme = Field(
        default=ColorTheme(
            name="Business",
            description="Professional business theme with navy/teal",
            primary=["#1565C0", "#0D47A1", "#01579B"],
            accent=["#00ACC1", "#0097A7", "#00838F"],
            gradient="linear-gradient(135deg, #1565C0 0%, #00ACC1 100%)",
            background=BackgroundColors(
                dark="#0A1929", light="#F5F8FA", glass="rgba(10, 25, 41, 0.85)"
            ),
            text=TextColors(on_dark="#FFFFFF", on_light="#0A1929", muted="#718096"),
            semantic=SemanticColors(
                success="#10B981", warning="#F59E0B", error="#EF4444", info="#0EA5E9"
            ),
        )
    )


# Create the singleton instance
COLOR_TOKENS = ColorTokens()
