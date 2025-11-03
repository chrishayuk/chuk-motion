"""
Tests for ThreeRowLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestThreeRowLayoutBasic:
    """Basic ThreeRowLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic ThreeRowLayout generation."""
        tsx = component_builder.build_component(
            "ThreeRowLayout",
            {"top_height": 25, "middle_height": 50, "bottom_height": 25},
            theme_name,
        )

        assert tsx is not None
        assert "ThreeRowLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "ThreeRowLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test ThreeRowLayout with minimal props."""
        tsx = component_builder.build_component("ThreeRowLayout", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "top_height" in tsx or "topHeight" in tsx
        assert "middle_height" in tsx or "middleHeight" in tsx
        assert "bottom_height" in tsx or "bottomHeight" in tsx


class TestThreeRowLayoutStructure:
    """Tests for layout structure."""

    def test_flex_display(self, component_builder, theme_name):
        """Test uses Flexbox."""
        tsx = component_builder.build_component("ThreeRowLayout", {}, theme_name)

        assert "display: 'flex'" in tsx or "display: flex" in tsx
        assert "flexDirection" in tsx

    def test_three_rows(self, component_builder, theme_name):
        """Test creates 3 rows."""
        tsx = component_builder.build_component("ThreeRowLayout", {}, theme_name)

        assert "top_height" in tsx or "topHeight" in tsx
        assert "middle_height" in tsx or "middleHeight" in tsx
        assert "bottom_height" in tsx or "bottomHeight" in tsx

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (top, middle, bottom)."""
        tsx = component_builder.build_component("ThreeRowLayout", {}, theme_name)

        assert "{top}" in tsx
        assert "{middle}" in tsx
        assert "{bottom}" in tsx


class TestThreeRowLayoutProps:
    """Tests for row props."""

    def test_row_heights(self, component_builder, theme_name):
        """Test row height props."""
        tsx = component_builder.build_component(
            "ThreeRowLayout",
            {"top_height": 30, "middle_height": 40, "bottom_height": 30},
            theme_name,
        )

        assert "top_height" in tsx or "topHeight" in tsx
        assert "middle_height" in tsx or "middleHeight" in tsx
        assert "bottom_height" in tsx or "bottomHeight" in tsx

    def test_padding_and_gap(self, component_builder, theme_name):
        """Test padding and gap props."""
        tsx = component_builder.build_component(
            "ThreeRowLayout", {"padding": 40, "gap": 20}, theme_name
        )

        assert "padding" in tsx
        assert "gap" in tsx

    def test_border_props(self, component_builder, theme_name):
        """Test border props."""
        tsx = component_builder.build_component("ThreeRowLayout", {"border_width": 2}, theme_name)

        assert "border_width" in tsx
