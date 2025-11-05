"""
Tests for LowerThird template generation.
"""

import pytest

from ..conftest import (
    assert_design_tokens_injected,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestLowerThirdBasic:
    """Basic LowerThird generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LowerThird generation with all props."""
        tsx = component_builder.build_component(
            "LowerThird",
            {
                "name": "Speaker Name",
                "title": "Job Title",
                "variant": "glass",
                "position": "bottom_left",
            },
            theme_name,
        )

        assert tsx is not None
        assert "LowerThird" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "LowerThird")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test LowerThird with only required props."""
        tsx = component_builder.build_component("LowerThird", {"name": "Speaker"}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "variant = 'glass'" in tsx or "variant = " in tsx
        assert "position = 'bottom_left'" in tsx or "position = " in tsx


class TestLowerThirdPositions:
    """Tests for LowerThird position variants."""

    @pytest.mark.parametrize(
        "position",
        ["bottom_left", "bottom_center", "bottom_right", "top_left", "top_center", "top_right"],
    )
    def test_position_variant(self, component_builder, theme_name, position):
        """Test each position variant generates correctly."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "position": position}, theme_name
        )

        assert tsx is not None
        assert position in tsx
        assert "positionStyle" in tsx

    def test_position_mapping(self, component_builder, theme_name):
        """Test that positions map to correct CSS properties."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "position": "bottom_left"}, theme_name
        )

        # Should have interpolate for slide animation
        assert "interpolate" in tsx
        assert "bottom" in tsx
        assert "left" in tsx


class TestLowerThirdVariants:
    """Tests for LowerThird style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "standard", "glass", "bold", "animated"])
    def test_style_variant(self, component_builder, theme_name, variant):
        """Test each style variant generates correctly."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variantStyle" in tsx

    def test_glass_variant_backdrop(self, component_builder, theme_name):
        """Test glass variant has backdrop filter."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "variant": "glass"}, theme_name
        )

        assert "backdropFilter" in tsx or "blur" in tsx


class TestLowerThirdAnimation:
    """Tests for LowerThird slide animation."""

    def test_has_slide_animation(self, component_builder, theme_name):
        """Test LowerThird has slide-in animation."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "slideIn" in tsx
        assert "spring" in tsx
        assert "interpolate" in tsx

    def test_uses_motion_tokens(self, component_builder, theme_name):
        """Test animation uses motion tokens from theme."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        # Should use motion config
        assert "damping" in tsx
        assert "stiffness" in tsx
        assert "50.0" in tsx or "120.0" in tsx  # Actual spring config values

    def test_has_fade_in_out(self, component_builder, theme_name):
        """Test LowerThird has fade in and fade out."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "opacity" in tsx
        assert "fadeOut" in tsx
        assert "finalOpacity" in tsx


class TestLowerThirdContent:
    """Tests for LowerThird content rendering."""

    def test_name_only(self, component_builder, theme_name):
        """Test LowerThird with name only (no title)."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test Name"}, theme_name)

        assert "{name}" in tsx
        assert "title &&" in tsx  # Conditional rendering

    def test_name_and_title(self, component_builder, theme_name):
        """Test LowerThird with both name and title."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test Name", "title": "Test Title"}, theme_name
        )

        assert "{name}" in tsx
        assert "{title}" in tsx


class TestLowerThirdDesignTokens:
    """Tests for design token integration."""

    def test_design_tokens_injected(self, component_builder, theme_name):
        """Test that design tokens are properly injected."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert_design_tokens_injected(tsx)

    def test_font_family_from_theme(self, component_builder, theme_name):
        """Test font family comes from theme."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "fontFamily" in tsx
        assert "Inter" in tsx or "SF Pro" in tsx
