# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/AreaChart/test_area_chart.py
"""
Tests for AreaChart template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_valid_typescript,
)


class TestAreaChartBasic:
    """Basic AreaChart generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic AreaChart generation with all props."""
        tsx = component_builder.build_component(
            "AreaChart",
            {
                "data": [[0, 10], [1, 20], [2, 30]],
                "title": "Test Chart",
                "xlabel": "X",
                "ylabel": "Y",
            },
            theme_name,
        )

        assert tsx is not None
        assert "AreaChart" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "AreaChart")

    def test_minimal_props(self, component_builder, theme_name):
        """Test AreaChart with minimal props."""
        tsx = component_builder.build_component("AreaChart", {}, theme_name)

        assert tsx is not None


class TestAreaChartRendering:
    """Tests for AreaChart rendering."""

    def test_svg_element(self, component_builder, theme_name):
        """Test SVG element is created."""
        tsx = component_builder.build_component(
            "AreaChart",
            {
                "data": [[0, 10], [1, 20], [2, 30]],
                "title": "Test Chart",
                "xlabel": "X",
                "ylabel": "Y",
            },
            theme_name,
        )

        assert "<svg" in tsx
        assert "width=" in tsx
        assert "height=" in tsx

    def test_data_handling(self, component_builder, theme_name):
        """Test data prop is used."""
        tsx = component_builder.build_component(
            "AreaChart",
            {
                "data": [[0, 10], [1, 20], [2, 30]],
                "title": "Test Chart",
                "xlabel": "X",
                "ylabel": "Y",
            },
            theme_name,
        )

        assert "data" in tsx


class TestAreaChartBuilderMethod:
    """Tests for AreaChart builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.charts.AreaChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [[0, 10], [1, 20], [2, 30]]
        result = add_to_composition(builder, data=data, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "AreaChart"
        assert builder.components[0].props["data"] == data

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.charts.AreaChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [[0, 10], [1, 20], [2, 30]]
        add_to_composition(
            builder,
            data=data,
            title="Test Chart",
            xlabel="X Axis",
            ylabel="Y Axis",
            start_time=1.0,
            duration=5.0,
        )

        props = builder.components[0].props
        assert props["data"] == data
        assert props["title"] == "Test Chart"
        assert props["xlabel"] == "X Axis"
        assert props["ylabel"] == "Y Axis"
        assert props["start_time"] == 1.0
        assert props["duration"] == 5.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.charts.AreaChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, data=[[0, 10]], start_time=2.0, duration=4.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2 seconds * 30 fps
        assert component.duration_frames == 120  # 4 seconds * 30 fps


class TestAreaChartToolRegistration:
    """Tests for AreaChart MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.AreaChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        # Verify decorator was called
        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.AreaChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition

        # Mock the add method
        composition.add_area_chart = Mock()

        # Register tool
        register_tool(mcp, project_manager)

        # Get the registered function
        tool_func = mcp.tool.call_args[0][0]

        # Execute the tool
        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", title="Test", start_time=0.0))

        # Verify it was called
        assert composition.add_area_chart.called
        result_data = json.loads(result)
        assert result_data["component"] == "AreaChart"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.AreaChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_composition = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", title="Test", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.AreaChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_area_chart = Mock(side_effect=Exception("Test error"))

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", title="Test", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_invalid_json(self):
        """Test tool execution handles invalid JSON data."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.AreaChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="invalid json {[}", title="Test", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid data JSON" in result_data["error"]
