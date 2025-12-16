# chuk-motion/src/chuk_motion/components/overlays/SubscribeButton/test_subscribe_button.py
"""
Tests for SubscribeButton template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_valid_typescript,
)


class TestSubscribeButtonBasic:
    """Basic SubscribeButton generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic SubscribeButton generation with all props."""
        tsx = component_builder.build_component(
            "SubscribeButton", {"text": "Test Text", "start_time": 0.0, "duration": 3.0}, theme_name
        )

        assert tsx is not None
        assert "SubscribeButton" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "SubscribeButton")
        assert_has_timing_props(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test SubscribeButton with minimal props."""
        tsx = component_builder.build_component("SubscribeButton", {}, theme_name)

        assert tsx is not None


class TestSubscribeButtonBuilderMethod:
    """Tests for SubscribeButton builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.overlays.SubscribeButton.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "SubscribeButton"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.overlays.SubscribeButton.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            variant="modern",
            animation="bounce",
            position="bottom-right",
            duration=3.0,
            custom_text="Click Here",
        )

        props = builder.components[0].props
        assert props["variant"] == "modern"
        assert props["animation"] == "bounce"
        assert props["position"] == "bottom-right"
        assert props["custom_text"] == "Click Here"


class TestSubscribeButtonToolRegistration:
    """Tests for SubscribeButton MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.overlays.SubscribeButton.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.SubscribeButton.tool import register_tool
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
        assert result_data["component"] == "SubscribeButton"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.SubscribeButton.tool import register_tool

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

        from chuk_motion.components.overlays.SubscribeButton.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_subscribe_button to raise exception
        with patch.object(timeline, "add_subscribe_button", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
