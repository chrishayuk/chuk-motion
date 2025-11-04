"""
Tests for AsymmetricLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestAsymmetricLayoutBasic:
    """Basic AsymmetricLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic AsymmetricLayout generation."""
        tsx = component_builder.build_component(
            "AsymmetricLayout", {"layout": "main_left", "main_ratio": 70}, theme_name
        )

        assert tsx is not None
        assert "AsymmetricLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "AsymmetricLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test AsymmetricLayout with minimal props."""
        tsx = component_builder.build_component("AsymmetricLayout", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "layout" in tsx
        assert "main_ratio" in tsx or "mainRatio" in tsx


class TestAsymmetricLayoutVariants:
    """Tests for layout variants."""

    @pytest.mark.parametrize("layout", ["main-left", "main-right"])
    def test_layout_variant(self, component_builder, theme_name, layout):
        """Test each layout variant."""
        tsx = component_builder.build_component("AsymmetricLayout", {"layout": layout}, theme_name)

        assert tsx is not None
        assert layout in tsx

    def test_main_ratio_prop(self, component_builder, theme_name):
        """Test main_ratio prop controls split."""
        tsx = component_builder.build_component("AsymmetricLayout", {"main_ratio": 80}, theme_name)

        assert "main_ratio" in tsx or "mainRatio" in tsx


class TestAsymmetricLayoutStructure:
    """Tests for layout structure."""

    def test_flex_display(self, component_builder, theme_name):
        """Test uses Flexbox for layout."""
        tsx = component_builder.build_component("AsymmetricLayout", {}, theme_name)

        assert "display: 'flex'" in tsx or "display: flex" in tsx

    def test_named_props_handling(self, component_builder, theme_name):
        """Test uses named props not children array."""
        tsx = component_builder.build_component("AsymmetricLayout", {}, theme_name)

        assert "mainFeed" in tsx
        assert "demo1" in tsx
        assert "demo2" in tsx


class TestAsymmetricLayoutProps:
    """Tests for layout props."""

    def test_padding_and_gap(self, component_builder, theme_name):
        """Test padding and gap props."""
        tsx = component_builder.build_component(
            "AsymmetricLayout", {"padding": 40, "gap": 20}, theme_name
        )

        assert "padding" in tsx
        assert "gap" in tsx

    def test_border_props(self, component_builder, theme_name):
        """Test border props."""
        tsx = component_builder.build_component("AsymmetricLayout", {"border_width": 2}, theme_name)

        assert "border_width" in tsx
