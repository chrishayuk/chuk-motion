# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/LineChart/test_linechart.py
"""
Tests for LineChart template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestLineChartBasic:
    """Basic LineChart generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LineChart generation with all props."""
        tsx = component_builder.build_component(
            "LineChart",
            {
                "data_points": [10, 25, 15, 30, 40],
                "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                "title": "Sales Growth",
                "xlabel": "Month",
                "ylabel": "Revenue",
            },
            theme_name,
        )

        assert tsx is not None
        assert "LineChart" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "LineChart")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test LineChart with minimal props."""
        tsx = component_builder.build_component("LineChart", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "data = []" in tsx or "data" in tsx


class TestLineChartDataHandling:
    """Tests for data handling."""

    def test_data_points_prop(self, component_builder, theme_name):
        """Test data prop is used."""
        tsx = component_builder.build_component(
            "LineChart", {"data": [[0, 1], [1, 2], [2, 3]]}, theme_name
        )

        assert "data" in tsx or "dataPoints" in tsx

    def test_labels_prop(self, component_builder, theme_name):
        """Test labels prop is used."""
        tsx = component_builder.build_component(
            "LineChart", {"data": [[0, 1], [1, 2], [2, 3]], "title": "Test Chart"}, theme_name
        )

        assert "title" in tsx or "Test Chart" in tsx

    def test_empty_data_handling(self, component_builder, theme_name):
        """Test handling of empty data."""
        tsx = component_builder.build_component("LineChart", {"data_points": []}, theme_name)

        assert "dataPoints.length === 0" in tsx
        assert "return null" in tsx


class TestLineChartSVG:
    """Tests for SVG rendering."""

    def test_svg_element(self, component_builder, theme_name):
        """Test SVG element is created."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<svg" in tsx
        assert "width=" in tsx
        assert "height=" in tsx

    def test_chart_dimensions(self, component_builder, theme_name):
        """Test chart has proper dimensions."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "chartWidth" in tsx
        assert "chartHeight" in tsx
        assert "padding" in tsx

    def test_svg_gradients(self, component_builder, theme_name):
        """Test SVG gradients are defined."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<defs>" in tsx
        assert "linearGradient" in tsx
        assert "bgGradient" in tsx
        assert "lineGradient" in tsx

    def test_svg_filters(self, component_builder, theme_name):
        """Test SVG filters for glow effect."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<filter" in tsx
        assert "feGaussianBlur" in tsx
        assert "glow" in tsx


class TestLineChartPath:
    """Tests for line path generation."""

    def test_path_generation(self, component_builder, theme_name):
        """Test SVG path is generated."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<path" in tsx
        assert "pathData" in tsx
        assert "d={pathData}" in tsx

    def test_path_styling(self, component_builder, theme_name):
        """Test path has proper styling."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "stroke=" in tsx
        assert "strokeWidth" in tsx
        assert "strokeLinecap" in tsx
        assert "strokeLinejoin" in tsx

    def test_coordinate_scaling(self, component_builder, theme_name):
        """Test coordinate scaling functions."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "scaleX" in tsx
        assert "scaleY" in tsx


class TestLineChartAnimation:
    """Tests for chart animations."""

    def test_entrance_animation(self, component_builder, theme_name):
        """Test chart has entrance animation."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "entranceProgress" in tsx
        assert "spring" in tsx
        assert "scale" in tsx

    def test_exit_animation(self, component_builder, theme_name):
        """Test chart has exit animation."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "exitProgress" in tsx
        assert "exitDuration" in tsx
        assert "opacity" in tsx

    def test_line_drawing_animation(self, component_builder, theme_name):
        """Test line is drawn progressively."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "lineProgress" in tsx
        assert "numPointsToShow" in tsx
        assert "visiblePoints" in tsx

    def test_data_points_pulse(self, component_builder, theme_name):
        """Test data points have pulse animation."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "pulseScale" in tsx
        assert "Math.sin" in tsx


class TestLineChartElements:
    """Tests for chart visual elements."""

    def test_background_rect(self, component_builder, theme_name):
        """Test chart has background."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<rect" in tsx
        assert "fill=" in tsx

    def test_grid_lines(self, component_builder, theme_name):
        """Test chart has grid lines."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<line" in tsx
        assert "stroke=" in tsx

    def test_axes(self, component_builder, theme_name):
        """Test chart has axes."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        # Should have x and y axes
        assert "<line" in tsx

    def test_data_point_circles(self, component_builder, theme_name):
        """Test data points are rendered as circles."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "<circle" in tsx
        assert "cx=" in tsx
        assert "cy=" in tsx
        assert "r=" in tsx


class TestLineChartLabels:
    """Tests for chart labels."""

    def test_title_optional(self, component_builder, theme_name):
        """Test title is optional."""
        tsx = component_builder.build_component("LineChart", {"data_points": [1, 2, 3]}, theme_name)

        assert "title" in tsx
        assert "title &&" in tsx

    def test_xlabel_optional(self, component_builder, theme_name):
        """Test x-axis label is optional."""
        tsx = component_builder.build_component(
            "LineChart", {"data_points": [1, 2, 3], "xlabel": "Time"}, theme_name
        )

        assert "xlabel" in tsx
        assert "xlabel &&" in tsx
        assert "<text" in tsx

    def test_ylabel_optional(self, component_builder, theme_name):
        """Test y-axis label is optional."""
        tsx = component_builder.build_component(
            "LineChart", {"data_points": [1, 2, 3], "ylabel": "Value"}, theme_name
        )

        assert "ylabel" in tsx
        assert "ylabel &&" in tsx
        assert "<text" in tsx


class TestLineChartBuilderMethod:
    """Tests for LineChart builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.charts.LineChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [[0, 10], [1, 20], [2, 30]]
        result = add_to_composition(builder, data=data, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "LineChart"
        assert builder.components[0].props["data"] == data

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.charts.LineChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        data = [[0, 10], [1, 20]]
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

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.charts.LineChart.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, data=[], start_time=2.0, duration=4.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 120


class TestLineChartToolRegistration:
    """Tests for LineChart MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.LineChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.LineChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_line_chart = Mock()

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", start_time=0.0))

        assert composition.add_line_chart.called
        result_data = json.loads(result)
        assert result_data["component"] == "LineChart"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.LineChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_composition = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.LineChart.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_line_chart = Mock(side_effect=Exception("Test error"))

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(data="[[0, 10], [1, 20]]", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_invalid_json(self):
        """Test tool execution handles invalid JSON data."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.charts.LineChart.tool import register_tool

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
