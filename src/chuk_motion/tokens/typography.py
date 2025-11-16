# chuk-motion/src/chuk_motion/tokens/typography.py
"""
Typography tokens for Remotion video design system.

Font scales, weights, and families optimized for video readability.
All sizes are tested for legibility at 1080p and 4K resolutions.
"""

from pydantic import BaseModel, ConfigDict, Field


# Font Family Models
class FontFamily(BaseModel):
    """Font family definition."""

    name: str
    fonts: list[str]
    description: str
    usage: str


class FontFamilies(BaseModel):
    """All font families."""

    display: FontFamily = Field(
        default=FontFamily(
            name="Display",
            fonts=["Inter", "SF Pro Display", "system-ui", "sans-serif"],
            description="Large headings and titles",
            usage="Video titles, main headings",
        )
    )
    body: FontFamily = Field(
        default=FontFamily(
            name="Body",
            fonts=["Inter", "SF Pro Text", "system-ui", "sans-serif"],
            description="Body text and subtitles",
            usage="Captions, descriptions, body content",
        )
    )
    mono: FontFamily = Field(
        default=FontFamily(
            name="Monospace",
            fonts=["JetBrains Mono", "Fira Code", "Monaco", "monospace"],
            description="Code and technical content",
            usage="Code blocks, technical text",
        )
    )
    decorative: FontFamily = Field(
        default=FontFamily(
            name="Decorative",
            fonts=["Poppins", "Montserrat", "Raleway", "sans-serif"],
            description="Special emphasis and style",
            usage="Stylized text, special callouts",
        )
    )


# Font Size Models
class FontSizeScale(BaseModel):
    """Font size scale for a specific resolution."""

    model_config = ConfigDict(populate_by_name=True)

    xs: str  # Small captions
    sm: str  # Regular captions
    base: str  # Body text
    lg: str  # Subheadings
    xl: str  # Headings
    xxl: str = Field(alias="2xl")  # Large headings
    xxxl: str = Field(alias="3xl")  # Title cards
    xxxxl: str = Field(alias="4xl")  # Hero titles
    xxxxxl: str = Field(alias="5xl")  # Dramatic displays
    xxxxxxl: str = Field(alias="6xl")  # Maximum impact


class FontSizes(BaseModel):
    """Font sizes for different video resolutions."""

    video_1080p: FontSizeScale = Field(
        default=FontSizeScale(
            xs="24px",
            sm="32px",
            base="40px",
            lg="48px",
            xl="64px",
            **{"2xl": "80px", "3xl": "96px", "4xl": "120px", "5xl": "180px", "6xl": "240px"},
        )
    )
    video_4k: FontSizeScale = Field(
        default=FontSizeScale(
            xs="48px",
            sm="64px",
            base="80px",
            lg="96px",
            xl="128px",
            **{"2xl": "160px", "3xl": "192px", "4xl": "240px", "5xl": "360px", "6xl": "480px"},
        )
    )
    video_720p: FontSizeScale = Field(
        default=FontSizeScale(
            xs="18px",
            sm="24px",
            base="30px",
            lg="36px",
            xl="48px",
            **{"2xl": "60px", "3xl": "72px", "4xl": "90px", "5xl": "135px", "6xl": "180px"},
        )
    )


# Font Weight Model
class FontWeights(BaseModel):
    """Font weight scale."""

    thin: int = Field(default=100)
    extralight: int = Field(default=200)
    light: int = Field(default=300)
    regular: int = Field(default=400)
    medium: int = Field(default=500)
    semibold: int = Field(default=600)
    bold: int = Field(default=700)
    extrabold: int = Field(default=800)
    black: int = Field(default=900)


# Line Height Model
class LineHeights(BaseModel):
    """Line height scale."""

    tight: float = Field(default=1.1, description="Tight spacing for large headings")
    snug: float = Field(default=1.25, description="Snug spacing for headings")
    normal: float = Field(default=1.5, description="Normal spacing for body text")
    relaxed: float = Field(default=1.75, description="Relaxed for captions")
    loose: float = Field(default=2.0, description="Extra loose for special cases")


# Letter Spacing Model
class LetterSpacing(BaseModel):
    """Letter spacing scale."""

    tighter: str = Field(default="-0.05em")
    tight: str = Field(default="-0.025em")
    normal: str = Field(default="0")
    wide: str = Field(default="0.025em")
    wider: str = Field(default="0.05em")
    widest: str = Field(default="0.1em")


# Text Style Model
class TextStyle(BaseModel):
    """Text style preset."""

    name: str
    fontSize: str
    fontWeight: str
    lineHeight: str
    letterSpacing: str
    fontFamily: str


class TextStyles(BaseModel):
    """Text style presets."""

    hero_title: TextStyle = Field(
        default=TextStyle(
            name="Hero Title",
            fontSize="4xl",
            fontWeight="black",
            lineHeight="tight",
            letterSpacing="tight",
            fontFamily="display",
        )
    )
    title: TextStyle = Field(
        default=TextStyle(
            name="Title",
            fontSize="3xl",
            fontWeight="bold",
            lineHeight="tight",
            letterSpacing="tight",
            fontFamily="display",
        )
    )
    heading: TextStyle = Field(
        default=TextStyle(
            name="Heading",
            fontSize="2xl",
            fontWeight="semibold",
            lineHeight="snug",
            letterSpacing="normal",
            fontFamily="display",
        )
    )
    subheading: TextStyle = Field(
        default=TextStyle(
            name="Subheading",
            fontSize="xl",
            fontWeight="medium",
            lineHeight="snug",
            letterSpacing="normal",
            fontFamily="display",
        )
    )
    body: TextStyle = Field(
        default=TextStyle(
            name="Body",
            fontSize="base",
            fontWeight="regular",
            lineHeight="normal",
            letterSpacing="normal",
            fontFamily="body",
        )
    )
    caption: TextStyle = Field(
        default=TextStyle(
            name="Caption",
            fontSize="sm",
            fontWeight="medium",
            lineHeight="relaxed",
            letterSpacing="wide",
            fontFamily="body",
        )
    )
    small: TextStyle = Field(
        default=TextStyle(
            name="Small",
            fontSize="xs",
            fontWeight="regular",
            lineHeight="relaxed",
            letterSpacing="normal",
            fontFamily="body",
        )
    )


# Main Typography Tokens Model
class TypographyTokens(BaseModel):
    """Complete typography token system."""

    font_families: FontFamilies = Field(default_factory=FontFamilies)
    font_sizes: FontSizes = Field(default_factory=FontSizes)
    font_weights: FontWeights = Field(default_factory=FontWeights)
    line_heights: LineHeights = Field(default_factory=LineHeights)
    letter_spacing: LetterSpacing = Field(default_factory=LetterSpacing)
    text_styles: TextStyles = Field(default_factory=TextStyles)


# Create the singleton instance
TYPOGRAPHY_TOKENS = TypographyTokens()
