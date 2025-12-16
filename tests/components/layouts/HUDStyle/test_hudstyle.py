"""Tests for HUDStyle template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestHUDStyleBasic:
    """Basic HUDStyle generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic HUDStyle generation."""
        tsx = component_builder.build_component("HUDStyle", {}, theme_name)
        assert tsx is not None
        assert "HUDStyle" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "HUDStyle")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestHUDStyleBuilderMethod:
    """Tests for HUDStyle builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.HUDStyle.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "HUDStyle"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.HUDStyle.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            main_content={"type": "main"},
            top_left={"type": "tl"},
            top_right={"type": "tr"},
            bottom_left={"type": "bl"},
            bottom_right={"type": "br"},
            center={"type": "center"},
            overlay_size=20.0,
            gap=25.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["main_content"] == {"type": "main"}
        assert props["top_left"] == {"type": "tl"}
        assert props["top_right"] == {"type": "tr"}
        assert props["bottom_left"] == {"type": "bl"}
        assert props["bottom_right"] == {"type": "br"}
        assert props["center"] == {"type": "center"}
        assert props["overlay_size"] == 20.0
        assert props["gap"] == 25.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.HUDStyle.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestHUDStyleToolRegistration:
    """Tests for HUDStyle MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.HUDStyle.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.HUDStyle.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "HUDStyle"

        # Verify component was added
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.HUDStyle.tool import register_tool

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

        from chuk_motion.components.layouts.HUDStyle.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        with patch.object(timeline, "add_hud_style", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func())
            result_data = json.loads(result)
            assert "error" in result_data

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.HUDStyle.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(main_content="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid" in result_data["error"]
