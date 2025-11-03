"""
Tests for ThreeByThreeGrid layout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestThreeByThreeGridBasic:
    """Basic ThreeByThreeGrid generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic ThreeByThreeGrid generation."""
        tsx = component_builder.build_component(
            "ThreeByThreeGrid", {"padding": 40, "gap": 20, "border_width": 2}, theme_name
        )

        assert tsx is not None
        assert "ThreeByThreeGrid" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "ThreeByThreeGrid")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test ThreeByThreeGrid with minimal props."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "padding = 40" in tsx or "padding = " in tsx
        assert "gap = 20" in tsx or "gap = " in tsx


class TestThreeByThreeGridLayout:
    """Tests for grid layout structure."""

    def test_grid_display(self, component_builder, theme_name):
        """Test uses CSS Grid display."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert "display: 'grid'" in tsx or "display: grid" in tsx
        assert "gridTemplateColumns" in tsx
        assert "gridTemplateRows" in tsx

    def test_three_by_three_layout(self, component_builder, theme_name):
        """Test creates 3x3 grid."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert "1fr 1fr 1fr" in tsx  # 3 equal columns
        # Should appear twice (once for columns, once for rows)

    def test_children_array_handling(self, component_builder, theme_name):
        """Test handles children array."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert "children" in tsx
        assert "Array.isArray" in tsx
        assert "slice(0, 9)" in tsx  # Max 9 children


class TestThreeByThreeGridProps:
    """Tests for grid props."""

    def test_padding_prop(self, component_builder, theme_name):
        """Test padding prop is used."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {"padding": 60}, theme_name)

        assert "padding" in tsx

    def test_gap_prop(self, component_builder, theme_name):
        """Test gap prop is used."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {"gap": 30}, theme_name)

        assert "gap" in tsx

    def test_border_props(self, component_builder, theme_name):
        """Test border props are used."""
        tsx = component_builder.build_component(
            "ThreeByThreeGrid", {"border_width": 3, "border_color": "#FF0000"}, theme_name
        )

        assert "border_width" in tsx
        assert "border_color" in tsx
        assert "border_radius" in tsx

    def test_background_props(self, component_builder, theme_name):
        """Test background props are used."""
        tsx = component_builder.build_component(
            "ThreeByThreeGrid",
            {"background": "rgba(0,0,0,0.5)", "cell_background": "rgba(255,255,255,0.1)"},
            theme_name,
        )

        assert "background" in tsx
        assert "cell_background" in tsx


class TestThreeByThreeGridCells:
    """Tests for grid cell rendering."""

    def test_cell_wrapper(self, component_builder, theme_name):
        """Test each cell has wrapper div."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert "gridChildren.map" in tsx
        assert "width: " in tsx
        assert "height: " in tsx
        assert "overflow: " in tsx

    def test_cell_centering(self, component_builder, theme_name):
        """Test cells use flexbox centering."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)

        assert "display: " in tsx
        assert "alignItems: " in tsx
        assert "justifyContent: " in tsx
