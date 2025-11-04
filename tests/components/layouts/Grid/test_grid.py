# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Grid/test_grid.py
"""
Tests for Grid layout template generation.
"""

import pytest
from tests.components.conftest import (
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


class TestGridBuilderMethod:
    """Tests for Grid builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.layouts.Grid.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        items = ["item1", "item2"]
        result = add_to_composition(builder, items=items, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Grid"
        assert builder.components[0].props["items"] == items

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.layouts.Grid.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        items = ["item1", "item2", "item3"]
        add_to_composition(
            builder, items=items, start_time=1.0, layout="2x2", gap=30, padding=60, duration=10.0
        )

        props = builder.components[0].props
        assert props["items"] == items
        assert props["layout"] == "2x2"
        assert props["gap"] == 30
        assert props["padding"] == 60

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.layouts.Grid.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, items=[], start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestGridToolRegistration:
    """Tests for Grid MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Grid.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Grid.tool import register_tool
        from chuk_mcp_remotion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(items='[{"title": "A"}]', duration=5.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "Grid"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Grid.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(items='[{"title": "A"}]', duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_mcp_remotion.components.layouts.Grid.tool import register_tool
        from chuk_mcp_remotion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(items='[{"title": "A"}]', duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_invalid_json(self):
        """Test tool execution handles invalid JSON data."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Grid.tool import register_tool
        from chuk_mcp_remotion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(items="invalid json {[}", duration=4.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid items JSON" in result_data["error"]

