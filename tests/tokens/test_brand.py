# tests/tokens/test_brand.py
"""
Comprehensive tests for brand pack system.
"""

import pytest
from pydantic import ValidationError

from chuk_mcp_remotion.tokens.brand import (
    BRAND_PACKS,
    AssetsConfig,
    BrandPack,
    ColorsConfig,
    CTAStyleConfig,
    FontConfig,
    LogoConfig,
    MotionConfig,
    PlatformPreferencesConfig,
    TypographyConfig,
    get_brand_pack,
    list_brand_packs,
    merge_brand_pack,
)


class TestPydanticModels:
    """Test all Pydantic models are properly defined."""

    def test_logo_config_model(self):
        """Test LogoConfig model validation."""
        logo = LogoConfig(
            url="https://example.com/logo.png",
            width=200,
            height=60,
            position="top-left",
            scale=1.0,
        )
        assert logo.width == 200
        assert logo.position == "top-left"

    def test_logo_config_optional_url(self):
        """Test LogoConfig with optional URL."""
        logo = LogoConfig(url=None, width=200, height=60, position="top-left", scale=1.0)
        assert logo.url is None

    def test_colors_config_model(self):
        """Test ColorsConfig model validation."""
        colors = ColorsConfig(
            primary=["#007bff", "#0056b3"],
            secondary=["#6c757d", "#5a6268"],
            accent=["#ff4081", "#e91e63"],
            text="#ffffff",
            background="#000000",
            success="#28a745",
            warning="#ffc107",
            error="#dc3545",
        )
        assert len(colors.primary) == 2
        assert colors.text == "#ffffff"

    def test_font_config_model(self):
        """Test FontConfig model validation."""
        font = FontConfig(fonts=["Inter", "system-ui", "sans-serif"], fallback="sans-serif")
        assert len(font.fonts) == 3
        assert font.fallback == "sans-serif"

    def test_typography_config_model(self):
        """Test TypographyConfig model validation."""
        typography = TypographyConfig(
            heading_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
            body_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
            code_font=FontConfig(fonts=["Monaco"], fallback="monospace"),
        )
        assert typography.heading_font.fallback == "sans-serif"
        assert typography.code_font.fallback == "monospace"

    def test_typography_config_default_weights(self):
        """Test TypographyConfig has default font weights."""
        typography = TypographyConfig(
            heading_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
            body_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
            code_font=FontConfig(fonts=["Monaco"], fallback="monospace"),
        )
        assert "regular" in typography.font_weights
        assert "bold" in typography.font_weights
        assert typography.font_weights["regular"] == 400

    def test_motion_config_model(self):
        """Test MotionConfig model validation."""
        motion = MotionConfig(
            default_spring="smooth", default_easing="ease_out", default_tempo="medium"
        )
        assert motion.default_spring == "smooth"

    def test_assets_config_model(self):
        """Test AssetsConfig model with optional fields."""
        assets = AssetsConfig(
            intro_bumper="intro.mp4",
            outro_bumper=None,
            watermark="logo.png",
            background_music=None,
        )
        assert assets.intro_bumper == "intro.mp4"
        assert assets.outro_bumper is None

    def test_cta_style_config_model(self):
        """Test CTAStyleConfig model validation."""
        cta = CTAStyleConfig(variant="gradient", position="bottom-center", animation="scale_in")
        assert cta.variant == "gradient"

    def test_platform_preferences_config_model(self):
        """Test PlatformPreferencesConfig model validation."""
        prefs = PlatformPreferencesConfig(
            default_platform="youtube_long_form",
            safe_area_mode="standard",
            layout_mode="presentation",
        )
        assert prefs.default_platform == "youtube_long_form"

    def test_brand_pack_model(self):
        """Test complete BrandPack model validation."""
        brand = BrandPack(
            name="test",
            display_name="Test Brand",
            description="Test description",
            logo=LogoConfig(url=None, width=200, height=60, position="top-left", scale=1.0),
            colors=ColorsConfig(
                primary=["#007bff"],
                secondary=["#6c757d"],
                accent=["#ff4081"],
                text="#ffffff",
                background="#000000",
                success="#28a745",
                warning="#ffc107",
                error="#dc3545",
            ),
            typography=TypographyConfig(
                heading_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
                body_font=FontConfig(fonts=["Inter"], fallback="sans-serif"),
                code_font=FontConfig(fonts=["Monaco"], fallback="monospace"),
            ),
            motion=MotionConfig(
                default_spring="smooth", default_easing="ease_out", default_tempo="medium"
            ),
            assets=AssetsConfig(),
            cta_style=CTAStyleConfig(
                variant="gradient", position="bottom-center", animation="scale_in"
            ),
            platform_preferences=PlatformPreferencesConfig(
                default_platform="youtube_long_form",
                safe_area_mode="standard",
                layout_mode="presentation",
            ),
        )
        assert brand.name == "test"
        assert brand.display_name == "Test Brand"


class TestBrandPacksStructure:
    """Test BRAND_PACKS structure and completeness."""

    def test_all_brand_packs_present(self):
        """Test all expected brand packs exist."""
        expected_packs = ["default", "tech_startup", "enterprise", "creator", "education"]
        for pack in expected_packs:
            assert pack in BRAND_PACKS, f"Brand pack '{pack}' not found"
            assert isinstance(BRAND_PACKS[pack], BrandPack)

    def test_brand_pack_names_match_keys(self):
        """Test that brand pack names match their dictionary keys."""
        for key, pack in BRAND_PACKS.items():
            assert (
                pack.name == key
            ), f"Brand pack key '{key}' doesn't match name '{pack.name}'"

    def test_all_packs_have_display_names(self):
        """Test all brand packs have display names."""
        for pack_name, pack in BRAND_PACKS.items():
            assert pack.display_name, f"Brand pack '{pack_name}' missing display name"
            assert len(pack.display_name) > 0

    def test_all_packs_have_descriptions(self):
        """Test all brand packs have descriptions."""
        for pack_name, pack in BRAND_PACKS.items():
            assert pack.description, f"Brand pack '{pack_name}' missing description"
            assert len(pack.description) > 0

    def test_all_packs_have_logo_config(self):
        """Test all brand packs have logo configuration."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.logo, LogoConfig
            ), f"Brand pack '{pack_name}' has invalid logo config"
            assert pack.logo.width > 0
            assert pack.logo.height > 0

    def test_all_packs_have_color_palettes(self):
        """Test all brand packs have complete color palettes."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.colors, ColorsConfig
            ), f"Brand pack '{pack_name}' has invalid colors"
            assert len(pack.colors.primary) > 0, f"Brand pack '{pack_name}' has empty primary colors"
            assert pack.colors.text, f"Brand pack '{pack_name}' missing text color"
            assert pack.colors.background, f"Brand pack '{pack_name}' missing background color"

    def test_all_packs_have_typography(self):
        """Test all brand packs have typography configuration."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.typography, TypographyConfig
            ), f"Brand pack '{pack_name}' has invalid typography"
            assert len(pack.typography.heading_font.fonts) > 0
            assert len(pack.typography.body_font.fonts) > 0
            assert len(pack.typography.code_font.fonts) > 0

    def test_all_packs_have_motion_config(self):
        """Test all brand packs have motion configuration."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.motion, MotionConfig
            ), f"Brand pack '{pack_name}' has invalid motion config"
            assert pack.motion.default_spring
            assert pack.motion.default_easing
            assert pack.motion.default_tempo

    def test_all_packs_have_cta_style(self):
        """Test all brand packs have CTA style configuration."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.cta_style, CTAStyleConfig
            ), f"Brand pack '{pack_name}' has invalid CTA style"
            assert pack.cta_style.variant
            assert pack.cta_style.position
            assert pack.cta_style.animation

    def test_all_packs_have_platform_preferences(self):
        """Test all brand packs have platform preferences."""
        for pack_name, pack in BRAND_PACKS.items():
            assert isinstance(
                pack.platform_preferences, PlatformPreferencesConfig
            ), f"Brand pack '{pack_name}' has invalid platform preferences"


class TestBrandPackDifferences:
    """Test that brand packs have meaningful differences."""

    def test_tech_startup_vs_enterprise_colors(self):
        """Test tech_startup and enterprise have different color schemes."""
        tech = BRAND_PACKS["tech_startup"]
        enterprise = BRAND_PACKS["enterprise"]

        # Primary colors should be different
        assert tech.colors.primary != enterprise.colors.primary
        # Text colors should be different (tech is brighter)
        assert tech.colors.text != enterprise.colors.text

    def test_creator_has_vibrant_colors(self):
        """Test creator brand has more vibrant colors."""
        creator = BRAND_PACKS["creator"]

        # Creator should have vibrant colors (orange, pink, purple range)
        assert any("#f" in color.lower() or "#e" in color.lower() for color in creator.colors.primary)

    def test_enterprise_has_conservative_motion(self):
        """Test enterprise brand has conservative motion settings."""
        enterprise = BRAND_PACKS["enterprise"]

        assert enterprise.motion.default_tempo == "slow"
        assert enterprise.motion.default_spring in ["smooth", "gentle"]

    def test_creator_has_energetic_motion(self):
        """Test creator brand has energetic motion settings."""
        creator = BRAND_PACKS["creator"]

        assert creator.motion.default_tempo == "fast"
        assert creator.motion.default_spring == "bouncy"

    def test_education_optimized_for_clarity(self):
        """Test education brand is optimized for clarity."""
        education = BRAND_PACKS["education"]

        assert education.platform_preferences.layout_mode == "technical_detail"


class TestUtilityFunctions:
    """Test all utility functions."""

    def test_get_brand_pack(self):
        """Test get_brand_pack utility function."""
        pack = get_brand_pack("tech_startup")
        assert isinstance(pack, BrandPack)
        assert pack.name == "tech_startup"

    def test_get_brand_pack_fallback(self):
        """Test get_brand_pack falls back to 'default' for unknown packs."""
        pack = get_brand_pack("unknown_pack")
        assert pack.name == "default"

    def test_list_brand_packs(self):
        """Test list_brand_packs returns all pack info."""
        packs = list_brand_packs()
        assert isinstance(packs, list)
        assert len(packs) == 5

        # Check structure
        for pack in packs:
            assert "name" in pack
            assert "display_name" in pack
            assert "description" in pack

    def test_merge_brand_pack_basic(self):
        """Test merge_brand_pack with basic override."""
        overrides = {"name": "custom", "display_name": "Custom Brand"}
        merged = merge_brand_pack("default", overrides)

        assert isinstance(merged, BrandPack)
        assert merged.name == "custom"
        assert merged.display_name == "Custom Brand"

    def test_merge_brand_pack_deep_merge(self):
        """Test merge_brand_pack performs deep merge."""
        overrides = {
            "colors": {
                "primary": ["#custom1", "#custom2"],
                "text": "#customtext",
            }
        }
        merged = merge_brand_pack("default", overrides)

        # Should have custom primary and text
        assert merged.colors.primary == ["#custom1", "#custom2"]
        assert merged.colors.text == "#customtext"

        # Should still have original secondary (not overridden)
        assert merged.colors.secondary == BRAND_PACKS["default"].colors.secondary

    def test_merge_brand_pack_nested_override(self):
        """Test merge_brand_pack with nested structure override."""
        overrides = {
            "motion": {
                "default_spring": "bouncy",
            }
        }
        merged = merge_brand_pack("enterprise", overrides)

        assert merged.motion.default_spring == "bouncy"
        # Should keep other motion settings from enterprise
        assert merged.motion.default_tempo == "slow"

    def test_merge_brand_pack_preserves_model(self):
        """Test merge_brand_pack returns valid Pydantic model."""
        overrides = {"description": "Custom description"}
        merged = merge_brand_pack("default", overrides)

        # Should be a valid BrandPack instance
        assert isinstance(merged, BrandPack)

        # Should be able to access nested Pydantic models
        assert isinstance(merged.logo, LogoConfig)
        assert isinstance(merged.colors, ColorsConfig)
        assert isinstance(merged.typography, TypographyConfig)


class TestBrandPackConsistency:
    """Test consistency across brand packs."""

    def test_all_logo_dimensions_reasonable(self):
        """Test all logo dimensions are reasonable."""
        for pack_name, pack in BRAND_PACKS.items():
            assert 50 <= pack.logo.width <= 300, (
                f"Brand pack '{pack_name}' logo width should be reasonable"
            )
            assert 20 <= pack.logo.height <= 200, (
                f"Brand pack '{pack_name}' logo height should be reasonable"
            )

    def test_all_color_gradients_have_steps(self):
        """Test all color gradients have multiple steps."""
        for pack_name, pack in BRAND_PACKS.items():
            assert len(pack.colors.primary) >= 1, (
                f"Brand pack '{pack_name}' primary should have at least 1 color"
            )
            assert len(pack.colors.secondary) >= 1, (
                f"Brand pack '{pack_name}' secondary should have at least 1 color"
            )

    def test_all_font_families_have_fallbacks(self):
        """Test all font families have system fallbacks."""
        for pack_name, pack in BRAND_PACKS.items():
            assert pack.typography.heading_font.fallback in ["sans-serif", "serif", "monospace"]
            assert pack.typography.body_font.fallback in ["sans-serif", "serif", "monospace"]
            assert pack.typography.code_font.fallback == "monospace"

    def test_all_platform_preferences_valid(self):
        """Test all platform preferences reference valid values."""
        valid_platforms = [
            "youtube_long_form",
            "youtube_shorts",
            "tiktok",
            "instagram_reel",
            "linkedin",
            "presentation",
        ]
        valid_safe_area_modes = ["conservative", "standard", "aggressive"]
        valid_layout_modes = ["presentation", "feed_grab", "mobile_readable", "technical_detail"]

        for pack_name, pack in BRAND_PACKS.items():
            assert pack.platform_preferences.default_platform in valid_platforms, (
                f"Brand pack '{pack_name}' has invalid default platform"
            )
            assert pack.platform_preferences.safe_area_mode in valid_safe_area_modes, (
                f"Brand pack '{pack_name}' has invalid safe area mode"
            )
            assert pack.platform_preferences.layout_mode in valid_layout_modes, (
                f"Brand pack '{pack_name}' has invalid layout mode"
            )
