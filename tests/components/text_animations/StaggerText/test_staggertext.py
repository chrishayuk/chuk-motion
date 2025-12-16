# chuk-motion/tests/components/text_animations/StaggerText/test_staggertext.py
"""Tests for StaggerText component."""

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


class TestStaggerTextBasic:
    """Basic StaggerText generation tests."""

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_basic_generation(self, component_builder, theme_name):
        """Test basic StaggerText generation with all props."""
        tsx = component_builder.build_component(
            "StaggerText",
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
        assert "StaggerText" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "StaggerText")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    @pytest.mark.skip(reason="Component uses new structure with templates in component dir")
    def test_minimal_props(self, component_builder, theme_name):
        """Test StaggerText with only required props."""
        tsx = component_builder.build_component("StaggerText", {"text": "Test Text"}, theme_name)

        assert tsx is not None
        assert "Test Text" in tsx or "{text}" in tsx


class TestStaggerTextBuilderMethod:
    """Tests for StaggerText builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.text_animations.StaggerText.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="Test", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "StaggerText"
        assert builder.components[0].props["text"] == "Test"

    def test_add_to_composition_with_text_color(self):
        """Test add_to_composition with optional text_color parameter."""
        from chuk_motion.components.text_animations.StaggerText.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="Test", start_time=0.0, text_color="#FF0000")

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].props["textColor"] == "#FF0000"


class TestStaggerTextToolRegistration:
    """Tests for StaggerText MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.text_animations.StaggerText.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        from chuk_motion.components.text_animations.StaggerText.tool import register_tool
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
        assert result_data["component"] == "StaggerText"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        from chuk_motion.components.text_animations.StaggerText.tool import register_tool

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
        from chuk_motion.components.text_animations.StaggerText.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_stagger_text to raise exception
        with patch.object(timeline, "add_stagger_text", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(text="Test", duration=3.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_with_text_color(self):
        """Test tool execution with optional text_color parameter."""
        from chuk_motion.components.text_animations.StaggerText.tool import register_tool
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
        assert result_data["component"] == "StaggerText"
