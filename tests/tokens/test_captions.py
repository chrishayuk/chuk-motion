# tests/tokens/test_captions.py
"""
Comprehensive tests for caption style system.
"""

import pytest
from pydantic import ValidationError

from chuk_motion.tokens.captions import (
    CAPTION_STYLES,
    AnimationConfig,
    BackgroundConfig,
    CaptionStyle,
    ColorsConfig,
    HighlightConfig,
    PositionConfig,
    TypographyConfig,
    get_caption_style,
    get_style_for_platform,
    list_caption_styles,
)


class TestPydanticModels:
    """Test all Pydantic models are properly defined."""

    def test_typography_config_model(self):
        """Test TypographyConfig model validation."""
        typography = TypographyConfig(
            font_family=["Inter", "sans-serif"],
            font_weight=700,
            font_size=42,
            text_transform="uppercase",
            letter_spacing="0.05em",
            line_height=1.2,
        )
        assert typography.font_weight == 700
        assert typography.text_transform == "uppercase"

    def test_typography_config_literal_validation(self):
        """Test TypographyConfig rejects invalid text_transform."""
        with pytest.raises(ValidationError):
            TypographyConfig(
                font_family=["Inter"],
                font_weight=700,
                font_size=42,
                text_transform="invalid",  # Should fail
                letter_spacing="0.05em",
                line_height=1.2,
            )

    def test_colors_config_model(self):
        """Test ColorsConfig model validation."""
        colors = ColorsConfig(
            text="#ffffff", stroke="#000000", stroke_width=8, shadow="0 4px 8px rgba(0,0,0,0.8)"
        )
        assert colors.text == "#ffffff"
        assert colors.stroke_width == 8

    def test_colors_config_optional_stroke(self):
        """Test ColorsConfig with optional stroke."""
        colors = ColorsConfig(
            text="#ffffff", stroke=None, stroke_width=0, shadow="0 2px 4px rgba(0,0,0,0.3)"
        )
        assert colors.stroke is None

    def test_background_config_model(self):
        """Test BackgroundConfig model validation."""
        background = BackgroundConfig(
            enabled=True,
            style="pill",
            color="rgba(0, 0, 0, 0.8)",
            padding="8px 24px",
            border_radius="1000px",
            blur=0,
        )
        assert background.enabled is True
        assert background.style == "pill"

    def test_background_config_literal_validation(self):
        """Test BackgroundConfig rejects invalid style."""
        with pytest.raises(ValidationError):
            BackgroundConfig(
                enabled=True,
                style="invalid",  # Should fail
                color="rgba(0, 0, 0, 0.8)",
                padding="8px",
                border_radius="8px",
            )

    def test_position_config_model(self):
        """Test PositionConfig model validation."""
        position = PositionConfig(vertical="center", horizontal="center", offset_y=0)
        assert position.vertical == "center"
        assert position.horizontal == "center"

    def test_position_config_literal_validation(self):
        """Test PositionConfig rejects invalid positions."""
        with pytest.raises(ValidationError):
            PositionConfig(vertical="invalid", horizontal="center")

    def test_animation_config_model(self):
        """Test AnimationConfig model validation."""
        animation = AnimationConfig(
            enter="scale_in",
            exit="scale_out",
            enter_duration=0.15,
            exit_duration=0.1,
            scale_emphasis=1.15,
        )
        assert animation.enter == "scale_in"
        assert animation.scale_emphasis == 1.15

    def test_highlight_config_model(self):
        """Test HighlightConfig model validation."""
        highlight = HighlightConfig(
            enabled=True,
            trigger="emphasis",
            color="#ffff00",
            background="rgba(255, 255, 0, 0.3)",
            scale=1.2,
            animation="bounce",
        )
        assert highlight.enabled is True
        assert highlight.trigger == "emphasis"

    def test_highlight_config_literal_validation(self):
        """Test HighlightConfig rejects invalid trigger."""
        with pytest.raises(ValidationError):
            HighlightConfig(
                enabled=True,
                trigger="invalid",  # Should fail
                color="#ffff00",
                background="none",
                scale=1.0,
                animation="none",
            )

    def test_caption_style_model(self):
        """Test complete CaptionStyle model validation."""
        style = CaptionStyle(
            name="test",
            display_name="Test Style",
            description="Test description",
            display_mode="word_by_word",
            words_per_burst=1,
            word_duration=0.3,
            gap_duration=0.05,
            typography=TypographyConfig(
                font_family=["Inter"],
                font_weight=700,
                font_size=42,
                text_transform="none",
                letter_spacing="0.02em",
                line_height=1.4,
            ),
            colors=ColorsConfig(
                text="#ffffff", stroke="#000000", stroke_width=3, shadow="0 2px 4px rgba(0,0,0,0.5)"
            ),
            background=BackgroundConfig(
                enabled=True,
                style="box",
                color="rgba(0, 0, 0, 0.85)",
                padding="12px 24px",
                border_radius="8px",
                blur=4,
            ),
            position=PositionConfig(vertical="bottom", horizontal="center", offset_y=120),
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
        )
        assert style.name == "test"
        assert style.display_mode == "word_by_word"


class TestCaptionStylesStructure:
    """Test CAPTION_STYLES structure and completeness."""

    def test_all_caption_styles_present(self):
        """Test all expected caption styles exist."""
        expected_styles = ["burst", "precise", "headline", "minimal", "neon", "classic"]
        for style in expected_styles:
            assert style in CAPTION_STYLES, f"Caption style '{style}' not found"
            assert isinstance(CAPTION_STYLES[style], CaptionStyle)

    def test_style_names_match_keys(self):
        """Test that caption style names match their dictionary keys."""
        for key, style in CAPTION_STYLES.items():
            assert style.name == key, f"Caption style key '{key}' doesn't match name '{style.name}'"

    def test_all_styles_have_display_modes(self):
        """Test all styles have valid display modes."""
        valid_modes = ["word_by_word", "phrase_by_phrase", "line_by_line", "full_sentence"]
        for style_name, style in CAPTION_STYLES.items():
            assert style.display_mode in valid_modes, (
                f"Style '{style_name}' has invalid display mode '{style.display_mode}'"
            )

    def test_word_by_word_styles_have_word_duration(self):
        """Test word_by_word styles have word_duration set."""
        for style_name, style in CAPTION_STYLES.items():
            if style.display_mode == "word_by_word":
                assert style.word_duration is not None, (
                    f"Style '{style_name}' is word_by_word but missing word_duration"
                )
                assert style.words_per_burst is not None, (
                    f"Style '{style_name}' is word_by_word but missing words_per_burst"
                )

    def test_phrase_by_phrase_styles_have_phrase_duration(self):
        """Test phrase_by_phrase styles have phrase_duration set."""
        for style_name, style in CAPTION_STYLES.items():
            if style.display_mode == "phrase_by_phrase":
                assert style.phrase_duration is not None, (
                    f"Style '{style_name}' is phrase_by_phrase but missing phrase_duration"
                )
                assert style.words_per_phrase is not None, (
                    f"Style '{style_name}' is phrase_by_phrase but missing words_per_phrase"
                )

    def test_all_styles_have_typography(self):
        """Test all styles have typography configuration."""
        for _style_name, style in CAPTION_STYLES.items():
            assert isinstance(style.typography, TypographyConfig)
            assert len(style.typography.font_family) > 0
            assert style.typography.font_size > 0
            assert style.typography.font_weight >= 100

    def test_all_styles_have_colors(self):
        """Test all styles have color configuration."""
        for style_name, style in CAPTION_STYLES.items():
            assert isinstance(style.colors, ColorsConfig)
            assert style.colors.text, f"Style '{style_name}' missing text color"
            assert style.colors.shadow, f"Style '{style_name}' missing shadow"

    def test_all_styles_have_position(self):
        """Test all styles have position configuration."""
        for _style_name, style in CAPTION_STYLES.items():
            assert isinstance(style.position, PositionConfig)
            assert style.position.vertical in ["top", "center", "bottom", "lower_third"]
            assert style.position.horizontal in ["left", "center", "right"]

    def test_all_styles_have_animation(self):
        """Test all styles have animation configuration."""
        for _style_name, style in CAPTION_STYLES.items():
            assert isinstance(style.animation, AnimationConfig)
            assert style.animation.enter
            assert style.animation.exit
            assert style.animation.enter_duration > 0
            assert style.animation.exit_duration > 0

    def test_all_styles_have_platform_optimization(self):
        """Test all styles specify platform optimization."""
        for style_name, style in CAPTION_STYLES.items():
            assert len(style.platform_optimized) > 0, (
                f"Style '{style_name}' has no platform optimization"
            )


class TestCaptionStyleDifferences:
    """Test that caption styles have meaningful differences."""

    def test_burst_vs_precise_display_mode(self):
        """Test burst and precise have different display modes."""
        burst = CAPTION_STYLES["burst"]
        precise = CAPTION_STYLES["precise"]

        assert burst.display_mode == "word_by_word"
        assert precise.display_mode == "phrase_by_phrase"

    def test_burst_has_uppercase_text(self):
        """Test burst style uses uppercase text."""
        burst = CAPTION_STYLES["burst"]
        assert burst.typography.text_transform == "uppercase"

    def test_neon_has_glow_effect(self):
        """Test neon style has glow effect in shadow."""
        neon = CAPTION_STYLES["neon"]
        assert "0 0" in neon.colors.shadow  # Glow effect signature

    def test_classic_has_no_background(self):
        """Test classic style has no background."""
        classic = CAPTION_STYLES["classic"]
        assert classic.background.enabled is False

    def test_minimal_vs_headline_font_sizes(self):
        """Test minimal and headline have different font sizes."""
        minimal = CAPTION_STYLES["minimal"]
        headline = CAPTION_STYLES["headline"]

        assert headline.typography.font_size > minimal.typography.font_size

    def test_burst_optimized_for_shorts(self):
        """Test burst is optimized for short-form platforms."""
        burst = CAPTION_STYLES["burst"]
        short_platforms = ["tiktok", "youtube_shorts", "instagram_reel"]

        assert any(platform in burst.platform_optimized for platform in short_platforms)

    def test_precise_optimized_for_long_form(self):
        """Test precise is optimized for long-form platforms."""
        precise = CAPTION_STYLES["precise"]
        assert "youtube_long_form" in precise.platform_optimized


class TestUtilityFunctions:
    """Test all utility functions."""

    def test_get_caption_style(self):
        """Test get_caption_style utility function."""
        style = get_caption_style("burst")
        assert isinstance(style, CaptionStyle)
        assert style.name == "burst"

    def test_get_caption_style_fallback(self):
        """Test get_caption_style falls back to 'minimal' for unknown styles."""
        style = get_caption_style("unknown_style")
        assert style.name == "minimal"

    def test_get_style_for_platform_tiktok(self):
        """Test get_style_for_platform returns correct style for TikTok."""
        style_name = get_style_for_platform("tiktok")
        assert style_name == "burst"

    def test_get_style_for_platform_youtube(self):
        """Test get_style_for_platform returns correct style for YouTube."""
        style_name = get_style_for_platform("youtube_long_form")
        assert style_name == "precise"

    def test_get_style_for_platform_linkedin(self):
        """Test get_style_for_platform returns correct style for LinkedIn."""
        style_name = get_style_for_platform("linkedin")
        assert style_name == "headline"

    def test_get_style_for_platform_fallback(self):
        """Test get_style_for_platform falls back to 'minimal' for unknown platforms."""
        style_name = get_style_for_platform("unknown_platform")
        assert style_name == "minimal"

    def test_list_caption_styles(self):
        """Test list_caption_styles returns all style info."""
        styles = list_caption_styles()
        assert isinstance(styles, list)
        assert len(styles) == 6

        # Check structure
        for style in styles:
            assert "name" in style
            assert "display_name" in style
            assert "description" in style
            assert "display_mode" in style
            assert "recommended_tempo" in style


class TestCaptionStyleConsistency:
    """Test consistency across caption styles."""

    def test_all_font_weights_reasonable(self):
        """Test all font weights are reasonable."""
        for style_name, style in CAPTION_STYLES.items():
            assert 100 <= style.typography.font_weight <= 900, (
                f"Style '{style_name}' has unreasonable font weight"
            )

    def test_all_font_sizes_reasonable(self):
        """Test all font sizes are reasonable."""
        for style_name, style in CAPTION_STYLES.items():
            assert 24 <= style.typography.font_size <= 100, (
                f"Style '{style_name}' has unreasonable font size"
            )

    def test_all_animation_durations_reasonable(self):
        """Test all animation durations are reasonable."""
        for style_name, style in CAPTION_STYLES.items():
            assert 0.05 <= style.animation.enter_duration <= 2.0, (
                f"Style '{style_name}' has unreasonable enter duration"
            )
            assert 0.05 <= style.animation.exit_duration <= 2.0, (
                f"Style '{style_name}' has unreasonable exit duration"
            )

    def test_all_gap_durations_reasonable(self):
        """Test all gap durations are reasonable."""
        for style_name, style in CAPTION_STYLES.items():
            assert 0.0 <= style.gap_duration <= 2.0, (
                f"Style '{style_name}' has unreasonable gap duration"
            )

    def test_background_styles_valid(self):
        """Test all background styles are valid."""
        valid_styles = ["pill", "box", "none", "gradient"]
        for style_name, style in CAPTION_STYLES.items():
            assert style.background.style in valid_styles, (
                f"Style '{style_name}' has invalid background style"
            )

    def test_stroke_width_matches_stroke_presence(self):
        """Test stroke_width is 0 when stroke is None."""
        for style_name, style in CAPTION_STYLES.items():
            if style.colors.stroke is None:
                assert style.colors.stroke_width == 0, (
                    f"Style '{style_name}' has stroke_width but no stroke"
                )

    def test_platform_optimizations_are_strings(self):
        """Test all platform optimizations are valid strings."""
        for style_name, style in CAPTION_STYLES.items():
            for platform in style.platform_optimized:
                assert isinstance(platform, str), (
                    f"Style '{style_name}' has non-string platform optimization"
                )
                assert len(platform) > 0

    def test_recommended_tempos_valid(self):
        """Test all recommended tempos reference valid tempo names."""
        valid_tempos = ["sprint", "fast", "medium", "slow", "cinematic"]
        for style_name, style in CAPTION_STYLES.items():
            assert style.recommended_tempo in valid_tempos, (
                f"Style '{style_name}' has invalid recommended tempo '{style.recommended_tempo}'"
            )

    def test_faster_tempos_have_shorter_durations(self):
        """Test styles with faster tempos have shorter caption durations."""
        burst = CAPTION_STYLES["burst"]  # recommended_tempo: "fast"
        classic = CAPTION_STYLES["classic"]  # recommended_tempo: "cinematic"

        # Burst should have shorter word duration than classic's sentence duration
        assert burst.word_duration < classic.sentence_duration
