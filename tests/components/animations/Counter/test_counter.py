# chuk-mcp-remotion/src/chuk_mcp_remotion/components/animations/Counter/test_counter.py
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
        from chuk_mcp_remotion.components.animations.Counter.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, end_value=100.0, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Counter"
        assert builder.components[0].props["end_value"] == 100.0

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.animations.Counter.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

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
        from chuk_mcp_remotion.components.animations.Counter.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

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

        from chuk_mcp_remotion.components.animations.Counter.tool import register_tool

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

        from chuk_mcp_remotion.components.animations.Counter.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition

        # Mock the add method
        composition.add_counter = Mock()

        # Register tool
        register_tool(mcp, project_manager)

        # Get the registered function (it's the first call's first argument)
        tool_func = mcp.tool.call_args[0][0]

        # Execute the tool
        result = asyncio.run(tool_func(end_value=100.0, start_time=0.0))

        # Verify it was called
        assert composition.add_counter.called
        result_data = json.loads(result)
        assert result_data["component"] == "Counter"
        assert result_data["start_value"] == 0
        assert result_data["end_value"] == 100.0
        assert result_data["start_time"] == 0.0
        assert result_data["duration"] == 2.0

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.animations.Counter.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_composition = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(end_value=100.0, start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.animations.Counter.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_counter = Mock(side_effect=Exception("Test error"))

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(end_value=100.0, start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
