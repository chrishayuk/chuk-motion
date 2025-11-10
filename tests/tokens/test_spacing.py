# tests/tokens/test_spacing.py
"""
Comprehensive tests for spacing token system.
"""

import pytest
from pydantic import ValidationError

from chuk_mcp_remotion.tokens.spacing import (
    SPACING_TOKENS,
    AttentionZone,
    CriticalZone,
    LayoutModeCharacteristics,
    LayoutModeConfig,
    SafeAreaConfig,
    SpacingTokens,
    get_border_radius,
    get_border_width,
    get_layout_mode,
    get_safe_area,
    get_spacing,
    get_z_index,
    list_layout_modes,
    list_platforms,
)


class TestPydanticModels:
    """Test all Pydantic models are properly defined."""

    def test_critical_zone_model(self):
        """Test CriticalZone model validation."""
        zone = CriticalZone(top=100, bottom=100, left=120, right=120)
        assert zone.top == 100
        assert zone.bottom == 100

    def test_critical_zone_optional_fields(self):
        """Test CriticalZone with optional fields."""
        zone = CriticalZone(top=0, height=120)
        assert zone.top == 0
        assert zone.height == 120
        assert zone.bottom is None

    def test_safe_area_config_model(self):
        """Test SafeAreaConfig model validation."""
        safe_area = SafeAreaConfig(
            top=64,
            bottom=64,
            left=96,
            right=96,
            description="Test safe area",
            aspect_ratio="16:9",
            usage="Testing",
        )
        assert safe_area.top == 64
        assert safe_area.aspect_ratio == "16:9"

    def test_safe_area_with_critical_zones(self):
        """Test SafeAreaConfig with critical zones."""
        safe_area = SafeAreaConfig(
            top=60,
            bottom=60,
            left=80,
            right=80,
            critical_zones={
                "title_safe": CriticalZone(top=100, bottom=100, left=120, right=120),
            },
            description="Test",
            aspect_ratio="16:9",
        )
        assert "title_safe" in safe_area.critical_zones
        assert safe_area.critical_zones["title_safe"].top == 100

    def test_attention_zone_model(self):
        """Test AttentionZone model validation."""
        zone = AttentionZone(
            description="Center third",
            horizontal_start="33.33%",
            horizontal_end="66.67%",
            usage="Primary content",
        )
        assert zone.description == "Center third"
        assert zone.horizontal_start == "33.33%"

    def test_layout_mode_characteristics_model(self):
        """Test LayoutModeCharacteristics model with Literal types."""
        chars = LayoutModeCharacteristics(
            spacing_multiplier=1.5,
            font_size_multiplier=1.3,
            content_density="low",
            recommended_tempo="slow",
            safe_area_multiplier=1.2,
        )
        assert chars.content_density == "low"
        assert chars.spacing_multiplier == 1.5

    def test_layout_mode_characteristics_validation(self):
        """Test LayoutModeCharacteristics rejects invalid density."""
        with pytest.raises(ValidationError):
            LayoutModeCharacteristics(
                spacing_multiplier=1.0,
                font_size_multiplier=1.0,
                content_density="invalid",  # Should fail
                recommended_tempo="medium",
                safe_area_multiplier=1.0,
            )

    def test_layout_mode_config_model(self):
        """Test LayoutModeConfig model validation."""
        mode = LayoutModeConfig(
            name="Test Mode",
            description="Test description",
            characteristics=LayoutModeCharacteristics(
                spacing_multiplier=1.0,
                font_size_multiplier=1.0,
                content_density="medium",
                recommended_tempo="medium",
                safe_area_multiplier=1.0,
            ),
            usage="Testing",
            target_platforms=["youtube_long_form"],
            feel="Professional",
        )
        assert mode.name == "Test Mode"
        assert mode.characteristics.content_density == "medium"


class TestSpacingTokensStructure:
    """Test SPACING_TOKENS structure and completeness."""

    def test_spacing_tokens_is_pydantic_model(self):
        """Test that SPACING_TOKENS is a Pydantic model instance."""
        assert isinstance(SPACING_TOKENS, SpacingTokens)

    def test_all_spacing_sizes_present(self):
        """Test all expected spacing sizes exist."""
        expected_sizes = [
            "none",
            "xxs",
            "xs",
            "sm",
            "md",
            "lg",
            "xl",
            "2xl",
            "3xl",
            "4xl",
            "5xl",
            "6xl",
            "7xl",
        ]
        for size in expected_sizes:
            assert size in SPACING_TOKENS.spacing, f"Spacing size '{size}' not found"

    def test_spacing_values_have_units(self):
        """Test that spacing values include units (except 'none')."""
        for size, value in SPACING_TOKENS.spacing.items():
            if size != "none":
                assert value.endswith("px"), f"Spacing '{size}' should end with 'px'"

    def test_spacing_progression(self):
        """Test that spacing values increase logically."""
        xs = int(SPACING_TOKENS.spacing["xs"].rstrip("px"))
        sm = int(SPACING_TOKENS.spacing["sm"].rstrip("px"))
        md = int(SPACING_TOKENS.spacing["md"].rstrip("px"))
        lg = int(SPACING_TOKENS.spacing["lg"].rstrip("px"))

        assert xs < sm < md < lg, "Spacing should progress logically"

    def test_all_platform_safe_areas_present(self):
        """Test all expected platform safe areas exist."""
        expected_platforms = [
            "desktop",
            "mobile",
            "youtube_long_form",
            "youtube_shorts",
            "tiktok",
            "instagram_reel",
            "instagram_story",
            "linkedin",
            "twitter",
            "presentation",
            "square",
            "ultrawide",
        ]
        for platform in expected_platforms:
            assert platform in SPACING_TOKENS.safe_area, f"Platform '{platform}' not found"
            assert isinstance(SPACING_TOKENS.safe_area[platform], SafeAreaConfig)

    def test_safe_area_margins_are_positive(self):
        """Test that all safe area margins are positive numbers."""
        for platform, safe_area in SPACING_TOKENS.safe_area.items():
            assert safe_area.top >= 0, f"Platform '{platform}' top margin should be >= 0"
            assert safe_area.bottom >= 0, f"Platform '{platform}' bottom margin should be >= 0"
            assert safe_area.left >= 0, f"Platform '{platform}' left margin should be >= 0"
            assert safe_area.right >= 0, f"Platform '{platform}' right margin should be >= 0"

    def test_tiktok_critical_zones(self):
        """Test TikTok safe area has expected critical zones."""
        tiktok = SPACING_TOKENS.safe_area["tiktok"]
        assert tiktok.critical_zones is not None
        assert "top_bar" in tiktok.critical_zones
        assert "side_controls" in tiktok.critical_zones
        assert "bottom_info" in tiktok.critical_zones
        assert "caption_zone" in tiktok.critical_zones

    def test_youtube_shorts_vs_tiktok_differences(self):
        """Test that YouTube Shorts and TikTok have different safe areas."""
        yt_shorts = SPACING_TOKENS.safe_area["youtube_shorts"]
        tiktok = SPACING_TOKENS.safe_area["tiktok"]

        # TikTok has more aggressive right margin due to side controls
        assert tiktok.right > yt_shorts.right

    def test_all_attention_zones_present(self):
        """Test all expected attention zones exist."""
        expected_zones = ["center_third", "rule_of_thirds", "lower_third", "upper_banner"]
        for zone in expected_zones:
            assert zone in SPACING_TOKENS.attention_zone, f"Attention zone '{zone}' not found"
            assert isinstance(SPACING_TOKENS.attention_zone[zone], AttentionZone)

    def test_rule_of_thirds_intersections(self):
        """Test rule of thirds has 4 intersection points."""
        rule_of_thirds = SPACING_TOKENS.attention_zone["rule_of_thirds"]
        assert rule_of_thirds.intersections is not None
        assert len(rule_of_thirds.intersections) == 4

    def test_all_layout_modes_present(self):
        """Test all expected layout modes exist."""
        expected_modes = ["presentation", "feed_grab", "mobile_readable", "technical_detail"]
        for mode in expected_modes:
            assert mode in SPACING_TOKENS.layout_mode, f"Layout mode '{mode}' not found"
            assert isinstance(SPACING_TOKENS.layout_mode[mode], LayoutModeConfig)

    def test_layout_mode_multipliers(self):
        """Test layout mode multipliers are reasonable."""
        for mode_name, mode in SPACING_TOKENS.layout_mode.items():
            chars = mode.characteristics
            assert 0.5 <= chars.spacing_multiplier <= 2.0, (
                f"Mode '{mode_name}' spacing multiplier should be between 0.5 and 2.0"
            )
            assert 0.5 <= chars.font_size_multiplier <= 2.0, (
                f"Mode '{mode_name}' font size multiplier should be between 0.5 and 2.0"
            )
            assert 0.5 <= chars.safe_area_multiplier <= 2.0, (
                f"Mode '{mode_name}' safe area multiplier should be between 0.5 and 2.0"
            )

    def test_mobile_readable_has_larger_text(self):
        """Test mobile_readable mode has larger font size multiplier."""
        mobile = SPACING_TOKENS.layout_mode["mobile_readable"]
        presentation = SPACING_TOKENS.layout_mode["presentation"]

        assert (
            mobile.characteristics.font_size_multiplier
            > presentation.characteristics.font_size_multiplier
        )

    def test_all_border_radius_sizes_present(self):
        """Test all expected border radius sizes exist."""
        expected_sizes = ["none", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "full"]
        for size in expected_sizes:
            assert size in SPACING_TOKENS.border_radius, f"Border radius '{size}' not found"

    def test_all_border_width_sizes_present(self):
        """Test all expected border width sizes exist."""
        expected_sizes = ["none", "thin", "base", "thick", "heavy", "ultra"]
        for size in expected_sizes:
            assert size in SPACING_TOKENS.border_width, f"Border width '{size}' not found"

    def test_all_z_index_layers_present(self):
        """Test all expected z-index layers exist."""
        expected_layers = [
            "underground",
            "background",
            "base",
            "content",
            "elevated",
            "overlay",
            "dropdown",
            "modal",
            "toast",
            "tooltip",
            "debug",
        ]
        for layer in expected_layers:
            assert layer in SPACING_TOKENS.z_index, f"Z-index layer '{layer}' not found"

    def test_z_index_progression(self):
        """Test that z-index values progress logically."""
        assert SPACING_TOKENS.z_index["underground"] < SPACING_TOKENS.z_index["background"]
        assert SPACING_TOKENS.z_index["background"] < SPACING_TOKENS.z_index["base"]
        assert SPACING_TOKENS.z_index["base"] < SPACING_TOKENS.z_index["content"]
        assert SPACING_TOKENS.z_index["content"] < SPACING_TOKENS.z_index["modal"]
        assert SPACING_TOKENS.z_index["modal"] < SPACING_TOKENS.z_index["tooltip"]


class TestUtilityFunctions:
    """Test all utility functions."""

    def test_get_safe_area(self):
        """Test get_safe_area utility function."""
        safe_area = get_safe_area("tiktok")
        assert isinstance(safe_area, SafeAreaConfig)
        assert safe_area.aspect_ratio == "9:16"

    def test_get_safe_area_fallback(self):
        """Test get_safe_area falls back to 'desktop' for unknown platforms."""
        safe_area = get_safe_area("unknown_platform")
        assert safe_area.aspect_ratio == "16:9"  # Should return desktop

    def test_get_layout_mode(self):
        """Test get_layout_mode utility function."""
        mode = get_layout_mode("mobile_readable")
        assert isinstance(mode, LayoutModeConfig)
        assert mode.name == "Mobile Readable"

    def test_get_layout_mode_fallback(self):
        """Test get_layout_mode falls back to 'presentation' for unknown modes."""
        mode = get_layout_mode("unknown_mode")
        assert mode.name == "Presentation"

    def test_list_platforms(self):
        """Test list_platforms returns all platform names."""
        platforms = list_platforms()
        assert isinstance(platforms, list)
        assert "tiktok" in platforms
        assert "youtube_long_form" in platforms
        assert len(platforms) == 12

    def test_list_layout_modes(self):
        """Test list_layout_modes returns all mode names."""
        modes = list_layout_modes()
        assert isinstance(modes, list)
        assert "presentation" in modes
        assert "mobile_readable" in modes
        assert len(modes) == 4

    def test_get_spacing(self):
        """Test get_spacing utility function."""
        spacing = get_spacing("md")
        assert spacing == "16px"

    def test_get_spacing_fallback(self):
        """Test get_spacing falls back to 'md' for unknown sizes."""
        spacing = get_spacing("unknown_size")
        assert spacing == "16px"

    def test_get_border_radius(self):
        """Test get_border_radius utility function."""
        radius = get_border_radius("lg")
        assert radius == "12px"

    def test_get_border_radius_fallback(self):
        """Test get_border_radius falls back to 'md' for unknown sizes."""
        radius = get_border_radius("unknown_size")
        assert radius == "8px"

    def test_get_border_width(self):
        """Test get_border_width utility function."""
        width = get_border_width("thick")
        assert width == "4px"

    def test_get_border_width_fallback(self):
        """Test get_border_width falls back to 'base' for unknown sizes."""
        width = get_border_width("unknown_size")
        assert width == "2px"

    def test_get_z_index(self):
        """Test get_z_index utility function."""
        z_index = get_z_index("modal")
        assert z_index == 100

    def test_get_z_index_fallback(self):
        """Test get_z_index falls back to 'base' for unknown layers."""
        z_index = get_z_index("unknown_layer")
        assert z_index == 1


class TestPlatformConsistency:
    """Test consistency across platform configurations."""

    def test_vertical_platforms_have_larger_bottom_margins(self):
        """Test that vertical platforms have larger bottom margins."""
        vertical_platforms = ["youtube_shorts", "tiktok", "instagram_reel", "instagram_story"]

        for platform in vertical_platforms:
            safe_area = SPACING_TOKENS.safe_area[platform]
            assert safe_area.bottom > safe_area.left, (
                f"Vertical platform '{platform}' should have larger bottom margin"
            )

    def test_platforms_with_ui_overlays_have_overlay_list(self):
        """Test that platforms with UI overlays document them."""
        platforms_with_overlays = ["youtube_shorts", "tiktok", "instagram_reel"]

        for platform in platforms_with_overlays:
            safe_area = SPACING_TOKENS.safe_area[platform]
            assert safe_area.ui_overlays is not None, (
                f"Platform '{platform}' should document UI overlays"
            )
            assert len(safe_area.ui_overlays) > 0

    def test_layout_modes_target_valid_platforms(self):
        """Test that layout modes target valid platform names."""
        valid_platforms = set(SPACING_TOKENS.safe_area.keys())

        for mode_name, mode in SPACING_TOKENS.layout_mode.items():
            for platform in mode.target_platforms:
                assert platform in valid_platforms, (
                    f"Mode '{mode_name}' targets invalid platform '{platform}'"
                )
