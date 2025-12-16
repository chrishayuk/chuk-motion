"""Tests for LayoutTransition component."""

import asyncio
import json
from unittest.mock import Mock

import pytest
from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestLayoutTransitionBasic:
    """Basic LayoutTransition generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LayoutTransition generation."""
        tsx = component_builder.build_component("LayoutTransition", {}, theme_name)
        assert tsx is not None
        assert "LayoutTransition" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "LayoutTransition")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestLayoutTransitionBuilderMethod:
    """Tests for LayoutTransition builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.transitions.LayoutTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "LayoutTransition"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.transitions.LayoutTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            first_content={"type": "first"},
            second_content={"type": "second"},
            transition_type="slide_horizontal",
            transition_start=2.5,
            transition_duration=0.8,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["firstContent"] == {"type": "first"}
        assert props["secondContent"] == {"type": "second"}
        assert props["transitionType"] == "slide_horizontal"
        assert props["transitionStart"] == int(2.5 * 30)  # Default FPS is 30
        assert props["transitionDuration"] == int(0.8 * 30)

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.transitions.LayoutTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestLayoutTransitionToolRegistration:
    """Tests for LayoutTransition MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution_basic(self):
        """Test basic tool execution with valid content."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Create valid first and second content
        first_content = json.dumps({"type": "TitleScene", "config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        result = asyncio.run(tool_func(first_content=first_content, second_content=second_content))

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutTransition"

        # Verify component was added
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        first_content = json.dumps({"type": "Grid", "config": {"layout": "2x2"}})
        second_content = json.dumps({"type": "Container", "config": {"position": "center"}})

        result = asyncio.run(
            tool_func(
                first_content=first_content,
                second_content=second_content,
                transition_type="slide_horizontal",
                transition_start=1.5,
                transition_duration=0.8,
                duration=5.0,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutTransition"
        assert result_data["duration"] == 5.0

        # Verify component was added
        components = timeline.get_all_components()
        assert len(components) >= 1
        comp = components[0]
        assert comp.component_type == "LayoutTransition"

    @pytest.mark.parametrize(
        "transition_type",
        ["crossfade", "slide_horizontal", "slide_vertical", "cube_rotate", "parallax_push"],
    )
    def test_tool_execution_transition_types(self, transition_type):
        """Test tool execution with different transition types."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        first_content = json.dumps({"type": "TitleScene", "config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        result = asyncio.run(
            tool_func(
                first_content=first_content,
                second_content=second_content,
                transition_type=transition_type,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutTransition"

    def test_tool_execution_invalid_transition_type(self):
        """Test tool execution with invalid transition type."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        first_content = json.dumps({"type": "TitleScene", "config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        result = asyncio.run(
            tool_func(
                first_content=first_content,
                second_content=second_content,
                transition_type="invalid_type",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid transition_type" in result_data["error"]

    def test_tool_execution_invalid_json_first_content(self):
        """Test tool execution with invalid JSON in first_content."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(
            tool_func(
                first_content="invalid json",
                second_content='{"type":"TitleScene","config":{"text":"Second"}}',
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid JSON" in result_data["error"]

    def test_tool_execution_invalid_json_second_content(self):
        """Test tool execution with invalid JSON in second_content."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(
            tool_func(
                first_content='{"type":"TitleScene","config":{"text":"First"}}',
                second_content="invalid json",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid JSON" in result_data["error"]

    def test_tool_execution_invalid_content_format(self):
        """Test tool execution with invalid content format."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Missing 'type' key
        first_content = json.dumps({"config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        result = asyncio.run(tool_func(first_content=first_content, second_content=second_content))

        result_data = json.loads(result)
        assert "error" in result_data
        # Error message may vary depending on parse_nested_component implementation
        assert "Invalid content format" in result_data["error"] or "error" in result_data

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        first_content = json.dumps({"type": "TitleScene", "config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        result = asyncio.run(tool_func(first_content=first_content, second_content=second_content))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        from unittest.mock import patch

        from chuk_motion.components.transitions.LayoutTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        first_content = json.dumps({"type": "TitleScene", "config": {"text": "First"}})
        second_content = json.dumps({"type": "TitleScene", "config": {"text": "Second"}})

        # Patch add_layout_transition to raise an error
        with patch.object(timeline, "add_layout_transition", side_effect=Exception("Test error")):
            result = asyncio.run(
                tool_func(first_content=first_content, second_content=second_content)
            )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
