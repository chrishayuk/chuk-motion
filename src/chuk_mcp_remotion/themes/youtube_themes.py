# chuk-mcp-remotion/src/chuk_mcp_remotion/themes/youtube_themes.py
"""
YouTube-optimized themes combining color, typography, and motion tokens.

Each theme is a complete design system ready for video production.
"""

from ..tokens.colors import COLOR_TOKENS
from ..tokens.motion import MOTION_TOKENS
from ..tokens.spacing import SPACING_TOKENS
from ..tokens.typography import TYPOGRAPHY_TOKENS
from .models import Theme, ThemeCollection, ThemeMotion, ThemeTypography

# ============================================================================
# YOUTUBE THEME COLLECTION (Pydantic Models)
# ============================================================================

YOUTUBE_THEMES = ThemeCollection(
    themes={
        "tech": Theme(
            name="Tech",
            description="Modern tech aesthetic - perfect for tech reviews, tutorials, coding",
            colors=COLOR_TOKENS.tech,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["smooth"],
                default_easing=MOTION_TOKENS.easing["ease_out"],
                default_duration=MOTION_TOKENS.duration["normal"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Tech reviews",
                "Coding tutorials",
                "Software demos",
                "Tech news",
                "Product launches",
            ],
        ),
        "finance": Theme(
            name="Finance",
            description="Professional finance theme - ideal for investing, trading, business",
            colors=COLOR_TOKENS.finance,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["snappy"],
                default_easing=MOTION_TOKENS.easing["ease_in_out"],
                default_duration=MOTION_TOKENS.duration["normal"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Stock market analysis",
                "Investing advice",
                "Business news",
                "Financial education",
                "Crypto analysis",
            ],
        ),
        "education": Theme(
            name="Education",
            description="Friendly education theme - great for teaching, explainers, courses",
            colors=COLOR_TOKENS.education,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["bouncy"],
                default_easing=MOTION_TOKENS.easing["ease_out_back"],
                default_duration=MOTION_TOKENS.duration["medium"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Educational content",
                "Explainer videos",
                "Course content",
                "Study guides",
                "Academic lectures",
            ],
        ),
        "lifestyle": Theme(
            name="Lifestyle",
            description="Warm lifestyle theme - perfect for vlogs, lifestyle, wellness",
            colors=COLOR_TOKENS.lifestyle,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.decorative,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.body,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["gentle"],
                default_easing=MOTION_TOKENS.easing["ease_in_out"],
                default_duration=MOTION_TOKENS.duration["slow"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Vlogs",
                "Lifestyle content",
                "Wellness videos",
                "Travel vlogs",
                "Daily routines",
            ],
        ),
        "gaming": Theme(
            name="Gaming",
            description="High-energy gaming theme - ideal for gaming, esports, streams",
            colors=COLOR_TOKENS.gaming,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.display,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["bouncy"],
                default_easing=MOTION_TOKENS.easing["ease_out_back"],
                default_duration=MOTION_TOKENS.duration["fast"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Gaming videos",
                "Esports highlights",
                "Stream overlays",
                "Gaming reviews",
                "Let's plays",
            ],
        ),
        "minimal": Theme(
            name="Minimal",
            description="Clean minimal theme - universal, professional, timeless",
            colors=COLOR_TOKENS.minimal,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["smooth"],
                default_easing=MOTION_TOKENS.easing["ease_in_out"],
                default_duration=MOTION_TOKENS.duration["normal"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Professional content",
                "Corporate videos",
                "Documentaries",
                "Interviews",
                "Clean aesthetics",
            ],
        ),
        "business": Theme(
            name="Business",
            description="Professional business theme - corporate, presentations, B2B",
            colors=COLOR_TOKENS.business,
            typography=ThemeTypography(
                primary_font=TYPOGRAPHY_TOKENS.font_families.display,
                body_font=TYPOGRAPHY_TOKENS.font_families.body,
                code_font=TYPOGRAPHY_TOKENS.font_families.mono,
                default_resolution="video_1080p",
            ),
            motion=ThemeMotion(
                default_spring=MOTION_TOKENS.spring_configs["snappy"],
                default_easing=MOTION_TOKENS.easing["ease_in_out"],
                default_duration=MOTION_TOKENS.duration["normal"],
            ),
            spacing=SPACING_TOKENS,
            use_cases=[
                "Corporate videos",
                "Business presentations",
                "B2B content",
                "Company updates",
                "Professional training",
            ],
        ),
    }
)
