# chuk-motion/tests/components/transitions/PixelTransition/test_pixeltransition.py
"""Tests for PixelTransition component."""

import asyncio
import json
from unittest.mock import Mock, patch


class TestPixelTransitionBuilderMethod:
    """Tests for PixelTransition builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.transitions.PixelTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import (
            ComponentInstance,
            CompositionBuilder,
        )

        builder = CompositionBuilder()

        # Create mock content components
        first_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "Before"},
            layer=0,
        )
        second_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "After"},
            layer=0,
        )

        result = add_to_composition(
            builder,
            start_time=0.0,
            first_content=first_content,
            second_content=second_content,
        )

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "PixelTransition"
        assert builder.components[0].props["firstContent"] == first_content
        assert builder.components[0].props["secondContent"] == second_content

    def test_add_to_composition_all_props(self):
        """Test add_to_composition with all properties."""
        from chuk_motion.components.transitions.PixelTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import (
            ComponentInstance,
            CompositionBuilder,
        )

        builder = CompositionBuilder()

        first_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "Before"},
            layer=0,
        )
        second_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "After"},
            layer=0,
        )

        result = add_to_composition(
            builder,
            start_time=0.0,
            first_content=first_content,
            second_content=second_content,
            grid_size=15,
            pixel_color="#FF0000",
            transition_start=2.5,
            transition_duration=1.5,
            duration=6.0,
        )

        assert result is builder
        comp = builder.components[0]
        assert comp.props["gridSize"] == 15
        assert comp.props["pixelColor"] == "#FF0000"
        assert comp.props["transitionStart"] == int(2.5 * 30)  # 75 frames
        assert comp.props["transitionDuration"] == int(1.5 * 30)  # 45 frames

    def test_add_to_composition_without_pixel_color(self):
        """Test add_to_composition without optional pixel_color parameter."""
        from chuk_motion.components.transitions.PixelTransition.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import (
            ComponentInstance,
            CompositionBuilder,
        )

        builder = CompositionBuilder()

        first_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "Before"},
            layer=0,
        )
        second_content = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=150,
            props={"text": "After"},
            layer=0,
        )

        result = add_to_composition(
            builder,
            start_time=0.0,
            first_content=first_content,
            second_content=second_content,
        )

        assert result is builder
        assert "pixelColor" not in builder.components[0].props


class TestPixelTransitionToolRegistration:
    """Tests for PixelTransition MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Create JSON for first and second content
        first_content_json = json.dumps({
            "component_type": "TitleScene",
            "props": {"text": "Before", "variant": "bold"}
        })
        second_content_json = json.dumps({
            "component_type": "TitleScene",
            "props": {"text": "After", "variant": "glass"}
        })

        result = asyncio.run(
            tool_func(
                first_content=first_content_json,
                second_content=second_content_json,
                duration=5.0,
            )
        )

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "PixelTransition"

    def test_tool_execution_with_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        first_content_json = json.dumps({
            "component_type": "TitleScene",
            "props": {"text": "Before"}
        })
        second_content_json = json.dumps({
            "component_type": "TitleScene",
            "props": {"text": "After"}
        })

        asyncio.run(
            tool_func(
                first_content=first_content_json,
                second_content=second_content_json,
                grid_size=12,
                pixel_color="#00FF00",
                transition_start=2.5,
                transition_duration=1.2,
                duration=6.0,
            )
        )

        components = timeline.get_all_components()
        assert len(components) >= 1
        comp = components[0]
        assert comp.props.get("gridSize") == 12
        assert comp.props.get("pixelColor") == "#00FF00"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        first_content_json = json.dumps({"component_type": "TitleScene", "props": {}})
        second_content_json = json.dumps({"component_type": "TitleScene", "props": {}})

        result = asyncio.run(
            tool_func(
                first_content=first_content_json,
                second_content=second_content_json,
                duration=5.0,
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        first_content_json = json.dumps({"component_type": "TitleScene", "props": {}})
        second_content_json = json.dumps({"component_type": "TitleScene", "props": {}})

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(
                tool_func(
                    first_content=first_content_json,
                    second_content=second_content_json,
                    duration=5.0,
                )
            )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]

    def test_tool_execution_invalid_json(self):
        """Test tool execution with invalid JSON content."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Invalid JSON
        result = asyncio.run(
            tool_func(
                first_content="not valid json",
                second_content="also not valid",
                duration=5.0,
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_invalid_content_format(self):
        """Test tool execution with None content (JSON null)."""
        from chuk_motion.components.transitions.PixelTransition.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # JSON null will parse to Python None, triggering the error
        null_content = "null"

        result = asyncio.run(
            tool_func(
                first_content=null_content,
                second_content=null_content,
                duration=5.0,
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid content format" in result_data["error"]
