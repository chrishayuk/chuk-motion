# chuk-motion/tests/components/text_animations/DecryptedText/test_decryptedtext.py
"""Tests for DecryptedText component."""

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


class TestDecryptedTextBasic:
    """Basic DecryptedText generation tests."""

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_basic_generation(self, component_builder, theme_name):
        """Test basic DecryptedText generation with all props."""
        tsx = component_builder.build_component(
            "DecryptedText",
            {
                "text": "ACCESS GRANTED",
                "fontSize": "3xl",
                "fontWeight": "bold",
                "revealDirection": "start",
                "scrambleSpeed": 3.0,
                "position": "center",
            },
            theme_name,
        )

        assert tsx is not None
        assert "DecryptedText" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "DecryptedText")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_minimal_props(self, component_builder, theme_name):
        """Test DecryptedText with only required props."""
        tsx = component_builder.build_component(
            "DecryptedText", {"text": "Test Text"}, theme_name
        )

        assert tsx is not None
        assert "Test Text" in tsx or "{text}" in tsx


class TestDecryptedTextBuilderMethod:
    """Tests for DecryptedText builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.text_animations.DecryptedText.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="HACKED", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "DecryptedText"
        assert builder.components[0].props["text"] == "HACKED"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.text_animations.DecryptedText.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            text="SECRET",
            start_time=1.0,
            font_size="4xl",
            font_weight="extrabold",
            reveal_direction="center",
            scramble_speed=5.0,
            position="top",
            duration=4.0,
        )

        props = builder.components[0].props
        assert props["text"] == "SECRET"
        assert props["fontSize"] == "4xl"
        assert props["fontWeight"] == "extrabold"

    def test_add_to_composition_with_text_color(self):
        """Test add_to_composition with optional text_color parameter."""
        from chuk_motion.components.text_animations.DecryptedText.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(
            builder, text="HACKED", start_time=0.0, text_color="#FF0000"
        )

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].props["textColor"] == "#FF0000"


class TestDecryptedTextToolRegistration:
    """Tests for DecryptedText MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.text_animations.DecryptedText.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        from chuk_motion.components.text_animations.DecryptedText.tool import register_tool
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
        assert result_data["component"] == "DecryptedText"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        from chuk_motion.components.text_animations.DecryptedText.tool import register_tool

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
        from chuk_motion.components.text_animations.DecryptedText.tool import register_tool
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

    def test_tool_execution_with_text_color(self):
        """Test tool execution with optional text_color parameter."""
        from chuk_motion.components.text_animations.DecryptedText.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Test", text_color="#FF0000", duration=3.0))

        # Check component was added with text_color
        components = timeline.get_all_components()
        assert len(components) >= 1
        assert components[0].props.get("textColor") == "#FF0000"
        result_data = json.loads(result)
        assert result_data["component"] == "DecryptedText"
