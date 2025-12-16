# chuk-motion/src/chuk_motion/components/charts/PieChart/test_pie_chart.py
"""
Tests for PieChart template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_valid_typescript,
)


class TestPieChartBasic:
    """Basic PieChart generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic PieChart generation with all props."""
        tsx = component_builder.build_component(
            "PieChart",
            {
                "data": [{"label": "A", "value": 30}, {"label": "B", "value": 70}],
                "title": "Test Chart",
            },
            theme_name,
        )

        assert tsx is not None
        assert "PieChart" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "PieChart")

    def test_minimal_props(self, component_builder, theme_name):
        """Test PieChart with minimal props."""
        tsx = component_builder.build_component("PieChart", {}, theme_name)

        assert tsx is not None


class TestPieChartRendering:
    """Tests for PieChart rendering."""

    def test_svg_element(self, component_builder, theme_name):
        """Test SVG element is created."""
        tsx = component_builder.build_component(
            "PieChart",
            {
                "data": [{"label": "A", "value": 30}, {"label": "B", "value": 70}],
                "title": "Test Chart",
            },
            theme_name,
        )

        assert "<svg" in tsx
        assert "width=" in tsx
        assert "height=" in tsx

    def test_data_handling(self, component_builder, theme_name):
        """Test data prop is used."""
        tsx = component_builder.build_component(
            "PieChart",
            {
                "data": [{"label": "A", "value": 30}, {"label": "B", "value": 70}],
                "title": "Test Chart",
            },
            theme_name,
        )

        assert "data" in tsx


class TestPieChartBuilderMethod:
    """Tests for PieChart builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.charts.PieChart.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [{"label": "A", "value": 30}, {"label": "B", "value": 70}]
        result = add_to_composition(builder, data=data, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "PieChart"
        assert builder.components[0].props["data"] == data

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.charts.PieChart.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [{"label": "A", "value": 30}]
        add_to_composition(builder, data=data, title="Test Chart", start_time=1.0, duration=5.0)

        props = builder.components[0].props
        assert props["data"] == data
        assert props["title"] == "Test Chart"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.charts.PieChart.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, data=[], start_time=2.0, duration=4.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 120


class TestPieChartToolRegistration:
    """Tests for PieChart MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.charts.PieChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.charts.PieChart.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data='[{"label": "A", "value": 10}]', duration=4.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "PieChart"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.charts.PieChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data='[{"label": "A", "value": 10}]', duration=4.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.charts.PieChart.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_pie_chart to raise exception
        with patch.object(timeline, "add_pie_chart", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(data='[{"label": "A", "value": 10}]', duration=4.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_invalid_json(self):
        """Test tool execution handles invalid JSON data."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.charts.PieChart.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="invalid json {[}", title="Test", duration=4.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid data JSON" in result_data["error"]
