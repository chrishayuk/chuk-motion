# chuk-motion/src/chuk_motion/components/animations/Counter/test_counter.py
"""
Tests for Counter template generation.
"""

from tests.components.conftest import (
    assert_has_interface,
    assert_valid_typescript,
)


class TestCounterBasic:
    """Basic Counter generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Counter generation with all props."""
        tsx = component_builder.build_component(
            "Counter", {"start": 0, "end": 100, "duration": 2.0}, theme_name
        )

        assert tsx is not None
        assert "Counter" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Counter")

    def test_animation(self, component_builder, theme_name):
        """Test animation is present."""
        tsx = component_builder.build_component(
            "Counter", {"start": 0, "end": 100, "duration": 2.0}, theme_name
        )

        assert "spring" in tsx or "interpolate" in tsx
        assert "useCurrentFrame" in tsx


class TestCounterBuilderMethod:
    """Tests for Counter builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.animations.Counter.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, end_value=100.0, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Counter"
        assert builder.components[0].props["end_value"] == 100.0

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.animations.Counter.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            end_value=500.0,
            start_time=1.0,
            start_value=10.0,
            prefix="$",
            suffix=" USD",
            decimals=2,
            animation="ease_in",
            duration=3.0,
        )

        props = builder.components[0].props
        assert props["end_value"] == 500.0
        assert props["start_value"] == 10.0
        assert props["prefix"] == "$"
        assert props["suffix"] == " USD"
        assert props["decimals"] == 2
        assert props["animation"] == "ease_in"
        assert props["start_time"] == 1.0
        assert props["duration"] == 3.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.animations.Counter.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, end_value=100.0, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2 seconds * 30 fps
        assert component.duration_frames == 150  # 5 seconds * 30 fps


class TestCounterToolRegistration:
    """Tests for Counter MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.animations.Counter.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        # Verify decorator was called
        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.animations.Counter.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(end_value=100, duration=2.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "Counter"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.animations.Counter.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(end_value=100, duration=2.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.animations.Counter.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(end_value=100, duration=2.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
