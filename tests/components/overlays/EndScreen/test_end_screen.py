# chuk-motion/src/chuk_motion/components/overlays/EndScreen/test_end_screen.py
"""
Tests for EndScreen template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_valid_typescript,
)


class TestEndScreenBasic:
    """Basic EndScreen generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic EndScreen generation with all props."""
        tsx = component_builder.build_component(
            "EndScreen", {"text": "Test Text", "start_time": 0.0, "duration": 3.0}, theme_name
        )

        assert tsx is not None
        assert "EndScreen" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "EndScreen")
        assert_has_timing_props(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test EndScreen with minimal props."""
        tsx = component_builder.build_component("EndScreen", {}, theme_name)

        assert tsx is not None


class TestEndScreenBuilderMethod:
    """Tests for EndScreen builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.overlays.EndScreen.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, cta_text="Subscribe")

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "EndScreen"
        assert builder.components[0].props["cta_text"] == "Subscribe"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.overlays.EndScreen.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            cta_text="Subscribe",
            thumbnail_url="http://example.com/thumb.jpg",
            variant="modern",
            duration_seconds=10.0,
        )

        props = builder.components[0].props
        assert props["cta_text"] == "Subscribe"
        assert props["thumbnail_url"] == "http://example.com/thumb.jpg"
        assert props["variant"] == "modern"
        assert props["duration_seconds"] == 10.0


class TestEndScreenToolRegistration:
    """Tests for EndScreen MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.overlays.EndScreen.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.EndScreen.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(cta_text="Test", duration=8.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "EndScreen"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.EndScreen.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(cta_text="Test", duration=8.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.overlays.EndScreen.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(cta_text="Test", duration=8.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
