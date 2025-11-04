# chuk-mcp-remotion/tests/test_tokens.py
"""
Tests for design tokens (colors, typography, motion).
"""

from chuk_mcp_remotion.tokens.colors import COLOR_TOKENS
from chuk_mcp_remotion.tokens.motion import MOTION_TOKENS
from chuk_mcp_remotion.tokens.typography import TYPOGRAPHY_TOKENS


class TestColorTokens:
    """Test color token structure and values."""

    def test_color_tokens_exist(self):
        """Test that COLOR_TOKENS dictionary exists and is not empty."""
        assert COLOR_TOKENS is not None
        assert isinstance(COLOR_TOKENS, dict)
        assert len(COLOR_TOKENS) > 0

    def test_all_themes_present(self):
        """Test that all expected themes are present."""
        expected_themes = [
            "tech",
            "finance",
            "education",
            "lifestyle",
            "gaming",
            "minimal",
            "business",
        ]
        for theme in expected_themes:
            assert theme in COLOR_TOKENS, f"Theme '{theme}' not found"

    def test_theme_structure(self):
        """Test that each theme has required color categories."""
        required_keys = [
            "name",
            "description",
            "primary",
            "accent",
            "gradient",
            "background",
            "text",
            "semantic",
        ]

        for theme_key, theme in COLOR_TOKENS.items():
            for key in required_keys:
                assert key in theme, f"Theme '{theme_key}' missing key '{key}'"

    def test_primary_colors_are_three_scale(self):
        """Test that primary colors are 3-step scales."""
        for theme_key, theme in COLOR_TOKENS.items():
            assert isinstance(theme["primary"], list), f"{theme_key} primary should be list"
            assert len(theme["primary"]) == 3, f"{theme_key} should have 3 primary colors"

    def test_accent_colors_are_three_scale(self):
        """Test that accent colors are 3-step scales."""
        for theme_key, theme in COLOR_TOKENS.items():
            assert isinstance(theme["accent"], list), f"{theme_key} accent should be list"
            assert len(theme["accent"]) == 3, f"{theme_key} should have 3 accent colors"

    def test_hex_color_format(self):
        """Test that colors are in valid hex format."""
        import re

        hex_pattern = re.compile(r"^#[0-9A-Fa-f]{6}$")

        for theme_key, theme in COLOR_TOKENS.items():
            # Check primary colors
            for color in theme["primary"]:
                assert hex_pattern.match(color), f"Invalid hex color: {color} in {theme_key}"

            # Check accent colors
            for color in theme["accent"]:
                assert hex_pattern.match(color), f"Invalid hex color: {color} in {theme_key}"

    def test_background_colors(self):
        """Test background color structure."""
        for theme_key, theme in COLOR_TOKENS.items():
            bg = theme["background"]
            assert "dark" in bg, f"{theme_key} missing dark background"
            assert "light" in bg, f"{theme_key} missing light background"
            assert "glass" in bg, f"{theme_key} missing glass background"

    def test_text_colors(self):
        """Test text color structure."""
        for theme_key, theme in COLOR_TOKENS.items():
            text = theme["text"]
            assert "on_dark" in text, f"{theme_key} missing on_dark text color"
            assert "on_light" in text, f"{theme_key} missing on_light text color"
            assert "muted" in text, f"{theme_key} missing muted text color"

    def test_semantic_colors(self):
        """Test semantic color structure."""
        for theme_key, theme in COLOR_TOKENS.items():
            semantic = theme["semantic"]
            assert "success" in semantic, f"{theme_key} missing success color"
            assert "warning" in semantic, f"{theme_key} missing warning color"
            assert "error" in semantic, f"{theme_key} missing error color"
            assert "info" in semantic, f"{theme_key} missing info color"

    def test_gradient_is_string(self):
        """Test that gradient is a CSS gradient string."""
        for theme_key, theme in COLOR_TOKENS.items():
            assert isinstance(theme["gradient"], str), f"{theme_key} gradient should be string"
            assert "linear-gradient" in theme["gradient"], f"{theme_key} should use linear-gradient"

    def test_specific_theme_colors(self):
        """Test specific theme color values."""
        # Tech theme should be blue
        assert COLOR_TOKENS["tech"]["primary"][0] == "#0066FF"

        # Finance theme should be green
        assert COLOR_TOKENS["finance"]["primary"][0] == "#00C853"

        # Gaming theme should be neon green
        assert COLOR_TOKENS["gaming"]["primary"][0] == "#00E676"


class TestTypographyTokens:
    """Test typography token structure and values."""

    def test_typography_tokens_exist(self):
        """Test that TYPOGRAPHY_TOKENS exists."""
        assert TYPOGRAPHY_TOKENS is not None
        assert isinstance(TYPOGRAPHY_TOKENS, dict)

    def test_required_categories(self):
        """Test that all required typography categories exist."""
        required = [
            "font_families",
            "font_sizes",
            "font_weights",
            "line_heights",
            "letter_spacing",
            "text_styles",
        ]
        for category in required:
            assert category in TYPOGRAPHY_TOKENS, f"Missing category: {category}"

    def test_font_families(self):
        """Test font family structure."""
        families = TYPOGRAPHY_TOKENS["font_families"]
        required_families = ["display", "body", "mono", "decorative"]

        for family in required_families:
            assert family in families, f"Missing font family: {family}"
            assert "name" in families[family]
            assert "fonts" in families[family]
            assert isinstance(families[family]["fonts"], list)

    def test_font_sizes_resolutions(self):
        """Test font sizes for all resolutions."""
        sizes = TYPOGRAPHY_TOKENS["font_sizes"]
        required_resolutions = ["video_1080p", "video_4k", "video_720p"]

        for resolution in required_resolutions:
            assert resolution in sizes, f"Missing resolution: {resolution}"

    def test_font_size_scale(self):
        """Test font size scale completeness."""
        expected_sizes = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl"]

        for resolution, size_map in TYPOGRAPHY_TOKENS["font_sizes"].items():
            for size in expected_sizes:
                assert size in size_map, f"Missing size {size} in {resolution}"
                assert size_map[size].endswith("px"), f"Size should be in px: {size_map[size]}"

    def test_font_weights(self):
        """Test font weight scale."""
        weights = TYPOGRAPHY_TOKENS["font_weights"]
        expected_weights = {
            "thin": 100,
            "extralight": 200,
            "light": 300,
            "regular": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700,
            "extrabold": 800,
            "black": 900,
        }

        for weight, value in expected_weights.items():
            assert weight in weights
            assert weights[weight] == value

    def test_line_heights(self):
        """Test line height scale."""
        line_heights = TYPOGRAPHY_TOKENS["line_heights"]
        expected = ["tight", "snug", "normal", "relaxed", "loose"]

        for lh in expected:
            assert lh in line_heights
            assert isinstance(line_heights[lh], (int, float))

    def test_letter_spacing(self):
        """Test letter spacing scale."""
        spacing = TYPOGRAPHY_TOKENS["letter_spacing"]
        expected = ["tighter", "tight", "normal", "wide", "wider", "widest"]

        for sp in expected:
            assert sp in spacing
            assert isinstance(spacing[sp], str)

    def test_text_styles(self):
        """Test text style presets."""
        styles = TYPOGRAPHY_TOKENS["text_styles"]
        expected_styles = [
            "hero_title",
            "title",
            "heading",
            "subheading",
            "body",
            "caption",
            "small",
        ]

        for style in expected_styles:
            assert style in styles, f"Missing text style: {style}"
            style_obj = styles[style]
            assert "fontSize" in style_obj
            assert "fontWeight" in style_obj
            assert "lineHeight" in style_obj
            assert "fontFamily" in style_obj

    def test_1080p_sizes_scale_correctly(self):
        """Test that 1080p font sizes scale appropriately."""
        sizes_1080p = TYPOGRAPHY_TOKENS["font_sizes"]["video_1080p"]

        # xs should be smallest
        xs = int(sizes_1080p["xs"].rstrip("px"))
        sm = int(sizes_1080p["sm"].rstrip("px"))
        base = int(sizes_1080p["base"].rstrip("px"))
        xl = int(sizes_1080p["xl"].rstrip("px"))
        four_xl = int(sizes_1080p["4xl"].rstrip("px"))

        assert xs < sm < base < xl < four_xl, "Font sizes should scale correctly"


class TestMotionTokens:
    """Test motion token structure and values."""

    def test_motion_tokens_exist(self):
        """Test that MOTION_TOKENS exists."""
        assert MOTION_TOKENS is not None
        assert isinstance(MOTION_TOKENS, dict)

    def test_required_categories(self):
        """Test that all required motion categories exist."""
        required = [
            "spring_configs",
            "easing_curves",
            "durations",
            "animation_presets",
            "youtube_optimizations",
        ]
        for category in required:
            assert category in MOTION_TOKENS, f"Missing category: {category}"

    def test_spring_configs(self):
        """Test spring configuration structure."""
        springs = MOTION_TOKENS["spring_configs"]
        expected_springs = ["gentle", "smooth", "bouncy", "snappy", "elastic"]

        for spring in expected_springs:
            assert spring in springs, f"Missing spring: {spring}"
            config = springs[spring]
            assert "name" in config
            assert "description" in config
            assert "config" in config
            assert "usage" in config

            # Check spring config values
            spring_config = config["config"]
            assert "damping" in spring_config
            assert "mass" in spring_config
            assert "stiffness" in spring_config
            assert "overshootClamping" in spring_config

    def test_easing_curves(self):
        """Test easing curve structure."""
        easings = MOTION_TOKENS["easing_curves"]
        expected_easings = [
            "linear",
            "ease_in",
            "ease_out",
            "ease_in_out",
            "ease_in_back",
            "ease_out_back",
        ]

        for easing in expected_easings:
            assert easing in easings, f"Missing easing: {easing}"
            curve = easings[easing]
            assert "name" in curve
            assert "curve" in curve
            assert "css" in curve
            assert "description" in curve
            assert isinstance(curve["curve"], list)
            assert len(curve["curve"]) == 4, "Bezier curve should have 4 points"

    def test_durations(self):
        """Test duration preset structure."""
        durations = MOTION_TOKENS["durations"]
        expected_durations = [
            "instant",
            "ultra_fast",
            "fast",
            "normal",
            "moderate",
            "slow",
            "very_slow",
            "dramatic",
        ]

        for duration in expected_durations:
            assert duration in durations, f"Missing duration: {duration}"
            dur = durations[duration]
            assert "frames" in dur
            assert "seconds" in dur
            assert "description" in dur
            assert "usage" in dur
            assert isinstance(dur["frames"], (int, float))
            assert isinstance(dur["seconds"], (int, float))

    def test_duration_consistency(self):
        """Test that frames and seconds are consistent (30fps)."""
        durations = MOTION_TOKENS["durations"]

        for key, dur in durations.items():
            # Calculate expected seconds from frames (30fps)
            expected_seconds = dur["frames"] / 30
            # Allow small floating point difference
            assert abs(dur["seconds"] - expected_seconds) < 0.01, (
                f"{key}: seconds doesn't match frames at 30fps"
            )

    def test_animation_presets(self):
        """Test animation preset structure."""
        presets = MOTION_TOKENS["animation_presets"]
        expected_presets = [
            "fade_in",
            "fade_out",
            "slide_up",
            "slide_down",
            "scale_in",
            "bounce_in",
        ]

        for preset in expected_presets:
            assert preset in presets, f"Missing preset: {preset}"
            anim = presets[preset]
            assert "name" in anim
            assert "properties" in anim
            assert isinstance(anim["properties"], list)

    def test_youtube_optimizations(self):
        """Test YouTube optimization structure."""
        youtube = MOTION_TOKENS["youtube_optimizations"]

        assert "hook_timing" in youtube
        assert "pattern_interrupt" in youtube
        assert "retention_timing" in youtube

        # Check hook timing
        hook = youtube["hook_timing"]
        assert "description" in hook
        assert "max_frames" in hook
        assert hook["max_frames"] == 90, "Hook should be 3 seconds (90 frames)"

    def test_spring_values_are_numeric(self):
        """Test that spring config values are numeric."""
        for _spring_name, spring in MOTION_TOKENS["spring_configs"].items():
            config = spring["config"]
            assert isinstance(config["damping"], (int, float))
            assert isinstance(config["mass"], (int, float))
            assert isinstance(config["stiffness"], (int, float))
            assert isinstance(config["overshootClamping"], bool)

    def test_specific_spring_values(self):
        """Test specific spring configuration values."""
        # Bouncy should have low damping for overshoot
        bouncy = MOTION_TOKENS["spring_configs"]["bouncy"]
        assert bouncy["config"]["damping"] < 20, "Bouncy should have low damping"

        # Snappy should have high stiffness
        snappy = MOTION_TOKENS["spring_configs"]["snappy"]
        assert snappy["config"]["stiffness"] >= 400, "Snappy should have high stiffness"


class TestTokenIntegration:
    """Test integration between different token systems."""

    def test_theme_count_consistency(self):
        """Test that color tokens match expected theme count."""
        # Should have 7 themes
        assert len(COLOR_TOKENS) == 7

    def test_all_themes_have_all_tokens(self):
        """Test that all themes have complete token sets."""
        for theme_key in COLOR_TOKENS:
            theme = COLOR_TOKENS[theme_key]

            # Should have all required color categories
            assert len(theme["primary"]) == 3
            assert len(theme["accent"]) == 3
            assert len(theme["background"]) == 3
            assert len(theme["text"]) == 3
            assert len(theme["semantic"]) == 4

    def test_resolution_scaling(self):
        """Test that font sizes scale appropriately across resolutions."""
        sizes_720p = TYPOGRAPHY_TOKENS["font_sizes"]["video_720p"]
        sizes_1080p = TYPOGRAPHY_TOKENS["font_sizes"]["video_1080p"]
        sizes_4k = TYPOGRAPHY_TOKENS["font_sizes"]["video_4k"]

        for size_key in ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl"]:
            val_720p = int(sizes_720p[size_key].rstrip("px"))
            val_1080p = int(sizes_1080p[size_key].rstrip("px"))
            val_4k = int(sizes_4k[size_key].rstrip("px"))

            # Higher resolutions should have larger sizes
            assert val_720p < val_1080p < val_4k, f"{size_key}: sizes should scale with resolution"

    def test_no_missing_references(self):
        """Test that text styles reference valid tokens."""
        text_styles = TYPOGRAPHY_TOKENS["text_styles"]
        font_families = TYPOGRAPHY_TOKENS["font_families"]
        line_heights = TYPOGRAPHY_TOKENS["line_heights"]

        for style_name, style in text_styles.items():
            # Font family should exist
            assert style["fontFamily"] in font_families, (
                f"{style_name} references unknown font family: {style['fontFamily']}"
            )

            # Line height should exist
            assert style["lineHeight"] in line_heights, (
                f"{style_name} references unknown line height: {style['lineHeight']}"
            )
