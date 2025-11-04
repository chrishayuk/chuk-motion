"""
Tests for ThreeColumnLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestThreeColumnLayoutBasic:
    """Basic ThreeColumnLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic ThreeColumnLayout generation."""
        tsx = component_builder.build_component(
            "ThreeColumnLayout",
            {"left_width": 25, "center_width": 50, "right_width": 25},
            theme_name,
        )

        assert tsx is not None
        assert "ThreeColumnLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "ThreeColumnLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test ThreeColumnLayout with minimal props."""
        tsx = component_builder.build_component("ThreeColumnLayout", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "left_width" in tsx or "leftWidth" in tsx
        assert "center_width" in tsx or "centerWidth" in tsx
        assert "right_width" in tsx or "rightWidth" in tsx


class TestThreeColumnLayoutStructure:
    """Tests for layout structure."""

    def test_flex_display(self, component_builder, theme_name):
        """Test uses Flexbox."""
        tsx = component_builder.build_component("ThreeColumnLayout", {}, theme_name)

        assert "display: 'flex'" in tsx or "display: flex" in tsx
        assert "flexDirection" in tsx

    def test_three_columns(self, component_builder, theme_name):
        """Test creates 3 columns."""
        tsx = component_builder.build_component("ThreeColumnLayout", {}, theme_name)

        # Should have column width configuration
        assert "left_width" in tsx or "leftWidth" in tsx
        assert "center_width" in tsx or "centerWidth" in tsx
        assert "right_width" in tsx or "rightWidth" in tsx

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (left, center, right)."""
        tsx = component_builder.build_component("ThreeColumnLayout", {}, theme_name)

        assert "{left}" in tsx
        assert "{center}" in tsx
        assert "{right}" in tsx


class TestThreeColumnLayoutProps:
    """Tests for column props."""

    def test_column_widths(self, component_builder, theme_name):
        """Test column width props."""
        tsx = component_builder.build_component(
            "ThreeColumnLayout",
            {"left_width": 30, "center_width": 40, "right_width": 30},
            theme_name,
        )

        assert "left_width" in tsx or "leftWidth" in tsx
        assert "center_width" in tsx or "centerWidth" in tsx
        assert "right_width" in tsx or "rightWidth" in tsx

    def test_padding_and_gap(self, component_builder, theme_name):
        """Test padding and gap props."""
        tsx = component_builder.build_component(
            "ThreeColumnLayout", {"padding": 40, "gap": 20}, theme_name
        )

        assert "padding" in tsx
        assert "gap" in tsx

    def test_border_props(self, component_builder, theme_name):
        """Test border props."""
        tsx = component_builder.build_component(
            "ThreeColumnLayout", {"border_width": 2}, theme_name
        )

        assert "border_width" in tsx
