# chuk-motion/src/chuk_motion/components/layouts/SplitScreen/test_splitscreen.py
"""
Tests for SplitScreen layout template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestSplitScreenBasic:
    """Basic SplitScreen generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic SplitScreen generation."""
        tsx = component_builder.build_component("SplitScreen", {}, theme_name)

        assert tsx is not None
        assert "SplitScreen" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "SplitScreen")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (left, right)."""
        tsx = component_builder.build_component("SplitScreen", {}, theme_name)

        assert "left" in tsx
        assert "right" in tsx


class TestSplitScreenBuilderMethod:
    """Tests for SplitScreen builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.SplitScreen.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "SplitScreen"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.SplitScreen.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            orientation="horizontal",
            layout="50-50",
            gap=30,
            left_content="left",
            right_content="right",
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["orientation"] == "horizontal"
        assert props["layout"] == "50-50"
        assert props["gap"] == 30
        assert props["left_content"] == "left"
        assert props["right_content"] == "right"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.SplitScreen.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestSplitScreenToolRegistration:
    """Tests for SplitScreen MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.SplitScreen.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.SplitScreen.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(duration=5.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "SplitScreen"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.SplitScreen.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.SplitScreen.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_split_screen to raise exception
        with patch.object(timeline, "add_split_screen", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_json_parsing_error(self):
        """Test tool handles invalid JSON in component parameters."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.SplitScreen.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Test with invalid JSON in left_content parameter
        result = asyncio.run(tool_func(left_content="invalid json", duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid component JSON" in result_data["error"]
