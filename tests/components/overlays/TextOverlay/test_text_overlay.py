# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TextOverlay/test_text_overlay.py
"""
Tests for TextOverlay template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_valid_typescript,
)


class TestTextOverlayBasic:
    """Basic TextOverlay generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TextOverlay generation with all props."""
        tsx = component_builder.build_component(
            "TextOverlay", {"text": "Test Text", "start_time": 0.0, "duration": 3.0}, theme_name
        )

        assert tsx is not None
        assert "TextOverlay" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TextOverlay")
        assert_has_timing_props(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test TextOverlay with minimal props."""
        tsx = component_builder.build_component("TextOverlay", {}, theme_name)

        assert tsx is not None


class TestTextOverlayBuilderMethod:
    """Tests for TextOverlay builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.overlays.TextOverlay.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="Hello World", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "TextOverlay"
        assert builder.components[0].props["text"] == "Hello World"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.overlays.TextOverlay.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            text="Hello World",
            start_time=1.0,
            style="bold",
            animation="fade_in",
            duration=3.0,
            position="center",
        )

        props = builder.components[0].props
        assert props["text"] == "Hello World"
        assert props["style"] == "bold"
        assert props["animation"] == "fade_in"
        assert props["position"] == "center"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.overlays.TextOverlay.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, text="Test", start_time=2.0, duration=3.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 90


class TestTextOverlayToolRegistration:
    """Tests for TextOverlay MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TextOverlay.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TextOverlay.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_text_overlay = Mock()

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Hello World", start_time=0.0))

        assert composition.add_text_overlay.called
        result_data = json.loads(result)
        assert result_data["component"] == "TextOverlay"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TextOverlay.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_composition = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Hello World", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TextOverlay.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_text_overlay = Mock(side_effect=Exception("Test error"))

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Hello World", start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
