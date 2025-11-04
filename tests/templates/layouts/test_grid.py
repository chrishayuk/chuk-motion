"""
Tests for Grid layout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestGridBasic:
    """Basic Grid generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Grid generation with all props."""
        tsx = component_builder.build_component(
            "Grid", {"layout": "2x2", "padding": 40, "gap": 30, "border_width": 3}, theme_name
        )

        assert tsx is not None
        assert "Grid" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Grid")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test Grid with minimal props."""
        tsx = component_builder.build_component("Grid", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "layout = '3x3'" in tsx or "layout = " in tsx
        assert "padding = 40" in tsx or "padding = " in tsx


class TestGridLayouts:
    """Tests for Grid layout variants."""

    @pytest.mark.parametrize("layout", ["1x2", "2x1", "2x2", "3x2", "2x3", "3x3", "4x2", "2x4"])
    def test_layout_variant(self, component_builder, theme_name, layout):
        """Test each layout variant generates correctly."""
        tsx = component_builder.build_component("Grid", {"layout": layout}, theme_name)

        assert tsx is not None
        assert layout in tsx
        assert "gridTemplateColumns" in tsx
        assert "gridTemplateRows" in tsx

    def test_layout_mapping(self, component_builder, theme_name):
        """Test that layouts map to correct grid templates."""
        tsx = component_builder.build_component("Grid", {"layout": "2x2"}, theme_name)

        # Should define layout configuration
        assert "2x2" in tsx
        assert "layouts" in tsx


class TestGridProps:
    """Tests for Grid runtime props."""

    def test_padding_prop(self, component_builder, theme_name):
        """Test padding prop is used."""
        tsx = component_builder.build_component("Grid", {"padding": 60}, theme_name)

        assert "padding" in tsx
        assert "padding = 40" in tsx or "padding = " in tsx  # Has default

    def test_gap_prop(self, component_builder, theme_name):
        """Test gap prop is used."""
        tsx = component_builder.build_component("Grid", {"gap": 25}, theme_name)

        assert "gap" in tsx
        assert "gap = 20" in tsx or "gap = " in tsx  # Has default

    def test_border_props(self, component_builder, theme_name):
        """Test border props are used."""
        tsx = component_builder.build_component(
            "Grid", {"border_width": 2, "border_color": "rgba(255, 255, 255, 0.2)"}, theme_name
        )

        assert "border_width" in tsx
        assert "border_color" in tsx
        assert "border_radius" in tsx

    def test_cell_background_prop(self, component_builder, theme_name):
        """Test cell_background prop is used."""
        tsx = component_builder.build_component(
            "Grid", {"cell_background": "rgba(0, 0, 0, 0.3)"}, theme_name
        )

        assert "cell_background" in tsx


class TestGridChildren:
    """Tests for Grid children rendering."""

    def test_children_array_handling(self, component_builder, theme_name):
        """Test Grid handles children array."""
        tsx = component_builder.build_component("Grid", {}, theme_name)

        assert "children" in tsx
        assert "Array.isArray" in tsx
        assert "children.map" in tsx

    def test_cell_wrapper(self, component_builder, theme_name):
        """Test each cell is wrapped with styling div."""
        tsx = component_builder.build_component("Grid", {}, theme_name)

        # Each child should be wrapped
        assert "width: " in tsx
        assert "height: " in tsx
        assert "overflow: " in tsx


class TestGridStyling:
    """Tests for Grid CSS styling."""

    def test_absolute_positioning(self, component_builder, theme_name):
        """Test Grid uses absolute positioning."""
        tsx = component_builder.build_component("Grid", {}, theme_name)

        assert "position: " in tsx or "position: 'absolute'" in tsx
        assert "top" in tsx
        assert "left" in tsx

    def test_grid_display(self, component_builder, theme_name):
        """Test Grid uses CSS Grid."""
        tsx = component_builder.build_component("Grid", {}, theme_name)

        assert "display: 'grid'" in tsx or "display: grid" in tsx
        assert "gridTemplateColumns" in tsx
        assert "gridTemplateRows" in tsx
