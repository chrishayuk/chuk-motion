"""Tests for Timeline template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTimelineBasic:
    """Basic Timeline generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Timeline generation."""
        tsx = component_builder.build_component("Timeline", {}, theme_name)
        assert tsx is not None
        assert "Timeline" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Timeline")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestTimelineBuilderMethod:
    """Tests for Timeline builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.layouts.Timeline.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Timeline"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.layouts.Timeline.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        test_milestones = [{"time": 1.0, "label": "Event 1"}]
        add_to_composition(
            builder,
            start_time=1.0,
            main_content={"type": "main"},
            milestones=test_milestones,
            current_time=5.0,
            total_duration=15.0,
            position="top",
            height=120.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["main_content"] == {"type": "main"}
        assert props["milestones"] == test_milestones
        assert props["current_time"] == 5.0
        assert props["total_duration"] == 15.0
        assert props["position"] == "top"
        assert props["height"] == 120.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.layouts.Timeline.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestTimelineToolRegistration:
    """Tests for Timeline MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Timeline.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Timeline.tool import register_tool

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline_mock = Mock()
        component_mock = Mock()
        component_mock.start_frame = 0
        timeline_mock.add_component = Mock(return_value=component_mock)
        timeline_mock.frames_to_seconds = Mock(return_value=0.0)
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "Timeline"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Timeline.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Timeline.tool import register_tool

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline_mock = Mock()
        timeline_mock.add_component = Mock(side_effect=Exception("Test error"))
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data
    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.Timeline.tool import register_tool

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(main_content="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid" in result_data["error"]


