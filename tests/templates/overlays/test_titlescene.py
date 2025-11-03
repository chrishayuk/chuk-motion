"""
Tests for TitleScene template generation.
"""

import pytest

from ..conftest import (
    assert_design_tokens_injected,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTitleSceneBasic:
    """Basic TitleScene generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TitleScene generation with all props."""
        tsx = component_builder.build_component(
            "TitleScene",
            {
                "title": "Test Title",
                "subtitle": "Test Subtitle",
                "variant": "bold",
                "animation": "fade_zoom",
            },
            theme_name,
        )

        assert tsx is not None
        assert "TitleScene" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TitleScene")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test TitleScene with only required props."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Minimal Title"}, theme_name
        )

        assert tsx is not None
        assert "TitleScene" in tsx
        # Should have default values
        assert "variant = 'bold'" in tsx or "variant = " in tsx
        assert "animation = " in tsx


class TestTitleSceneAnimations:
    """Tests for TitleScene animation variants."""

    @pytest.mark.parametrize(
        "animation", ["fade_zoom", "slide_up", "typewriter", "blur_in", "fade_slide", "zoom"]
    )
    def test_animation_variant(self, component_builder, theme_name, animation):
        """Test each animation variant generates correctly."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": animation}, theme_name
        )

        assert tsx is not None
        assert animation in tsx or "animation" in tsx
        assert "spring" in tsx or "interpolate" in tsx

    def test_fade_zoom_animation(self, component_builder, theme_name):
        """Test fade_zoom animation specifics."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": "fade_zoom"}, theme_name
        )

        assert "spring" in tsx
        assert "scale" in tsx
        assert "opacity" in tsx

    def test_typewriter_animation(self, component_builder, theme_name):
        """Test typewriter animation specifics."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test Title", "animation": "typewriter"}, theme_name
        )

        assert "charsToShow" in tsx
        assert "slice" in tsx


class TestTitleSceneVariants:
    """Tests for TitleScene style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "standard", "bold", "kinetic", "glass"])
    def test_style_variant(self, component_builder, theme_name, variant):
        """Test each style variant generates correctly."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variantStyle" in tsx

    def test_bold_variant_sizing(self, component_builder, theme_name):
        """Test bold variant has larger font size."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "variant": "bold"}, theme_name
        )

        assert "120" in tsx  # Bold uses 120px font size


class TestTitleSceneDesignTokens:
    """Tests for design token integration."""

    def test_color_tokens_injected(self, component_builder, theme_name):
        """Test that color tokens from theme are injected."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        assert_design_tokens_injected(tsx)
        # Should have actual color values, not template vars
        assert "#" in tsx

    def test_typography_tokens_injected(self, component_builder, theme_name):
        """Test that typography tokens are injected."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        # Should have font family from theme
        assert "Inter" in tsx or "SF Pro" in tsx
        assert "fontFamily" in tsx

    def test_motion_tokens_injected(self, component_builder, theme_name):
        """Test that motion tokens are injected."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": "fade_zoom"}, theme_name
        )

        # Should have motion config values
        assert "damping" in tsx
        assert "stiffness" in tsx
        assert "200" in tsx  # Default damping value


class TestTitleSceneFadeOut:
    """Tests for fade-out animation."""

    def test_has_fade_out(self, component_builder, theme_name):
        """Test that TitleScene has fade-out at end."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        assert "fadeOut" in tsx
        assert "durationInFrames - 20" in tsx
        assert "finalOpacity" in tsx


class TestTitleSceneThemes:
    """Tests for all theme compatibility."""

    def test_all_themes(self, component_builder, all_themes):
        """Test generation works with all available themes."""
        for theme_name in all_themes:
            tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

            assert tsx is not None
            assert_valid_typescript(tsx)
            assert "[[" not in tsx  # No unresolved vars
