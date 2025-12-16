"""Tests for Vertical template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestVerticalBasic:
    """Basic Vertical generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Vertical generation."""
        tsx = component_builder.build_component("Vertical", {}, theme_name)
        assert tsx is not None
        assert "Vertical" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Vertical")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestVerticalBuilderMethod:
    """Tests for Vertical builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.Vertical.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Vertical"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.Vertical.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            top={"type": "top"},
            bottom={"type": "bottom"},
            layout_style="split-vertical",
            top_ratio=60.0,
            gap=25.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["top"] == {"type": "top"}
        assert props["bottom"] == {"type": "bottom"}
        assert props["layout_style"] == "split-vertical"
        assert props["top_ratio"] == 60.0
        assert props["gap"] == 25.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.Vertical.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestVerticalToolRegistration:
    """Tests for Vertical MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Vertical.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Vertical.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Use real Timeline with builder methods registered (via conftest.py)
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "Vertical"

        # Verify component was added
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Vertical.tool import register_tool

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
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.Vertical.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Use real Timeline but patch add_vertical to raise error
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Patch the builder method to raise error
        with patch.object(timeline, "add_vertical", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Vertical.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Use real Timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(top="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid component JSON" in result_data["error"]
