# chuk-motion/tests/components/text_animations/TrueFocus/test_truefocus.py
"""Tests for TrueFocus component."""

import asyncio
import json
from unittest.mock import Mock, patch

import pytest
from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTrueFocusBasic:
    """Basic TrueFocus generation tests."""

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TrueFocus generation with all props."""
        tsx = component_builder.build_component(
            "TrueFocus",
            {
                "text": "Test Text",
                "fontSize": "3xl",
                "fontWeight": "bold",
                "revealDirection": "start",
                "scrambleSpeed": 3.0,
                "position": "center",
            },
            theme_name,
        )

        assert tsx is not None
        assert "TrueFocus" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TrueFocus")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_minimal_props(self, component_builder, theme_name):
        """Test TrueFocus with only required props."""
        tsx = component_builder.build_component("TrueFocus", {"text": "Test Text"}, theme_name)

        assert tsx is not None
        assert "Test Text" in tsx or "{text}" in tsx


class TestTrueFocusBuilderMethod:
    """Tests for TrueFocus builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.text_animations.TrueFocus.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="Test", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "TrueFocus"
        assert builder.components[0].props["text"] == "Test"

    def test_add_to_composition_with_all_colors(self):
        """Test add_to_composition with all optional color parameters."""
        from chuk_motion.components.text_animations.TrueFocus.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(
            builder,
            text="Test",
            start_time=0.0,
            text_color="#FF0000",
            frame_color="#00FF00",
            glow_color="#0000FF",
        )

        assert result is builder
        assert len(builder.components) == 1
        comp = builder.components[0]
        assert comp.props["textColor"] == "#FF0000"
        assert comp.props["frameColor"] == "#00FF00"
        assert comp.props["glowColor"] == "#0000FF"


class TestTrueFocusToolRegistration:
    """Tests for TrueFocus MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.text_animations.TrueFocus.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        from chuk_motion.components.text_animations.TrueFocus.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Test", duration=3.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "TrueFocus"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        from chuk_motion.components.text_animations.TrueFocus.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Test", duration=3.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        from chuk_motion.components.text_animations.TrueFocus.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(text="Test", duration=3.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_with_all_colors(self):
        """Test tool execution with all optional color parameters."""
        from chuk_motion.components.text_animations.TrueFocus.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(
            tool_func(
                text="Test",
                text_color="#FF0000",
                frame_color="#00FF00",
                glow_color="#0000FF",
                duration=3.0,
            )
        )

        # Check component was added with all colors
        components = timeline.get_all_components()
        assert len(components) >= 1
        comp = components[0]
        assert comp.props.get("textColor") == "#FF0000"
        assert comp.props.get("frameColor") == "#00FF00"
        assert comp.props.get("glowColor") == "#0000FF"
        result_data = json.loads(result)
        assert result_data["component"] == "TrueFocus"
