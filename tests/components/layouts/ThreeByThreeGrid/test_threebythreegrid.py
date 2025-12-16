"""Tests for ThreeByThreeGrid template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestThreeByThreeGridBasic:
    """Basic ThreeByThreeGrid generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic ThreeByThreeGrid generation."""
        tsx = component_builder.build_component("ThreeByThreeGrid", {}, theme_name)
        assert tsx is not None
        assert "ThreeByThreeGrid" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "ThreeByThreeGrid")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestThreeByThreeGridBuilderMethod:
    """Tests for ThreeByThreeGrid builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.ThreeByThreeGrid.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, items=[], start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "ThreeByThreeGrid"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.ThreeByThreeGrid.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        test_items = [{"id": f"item{i}"} for i in range(9)]
        add_to_composition(
            builder,
            items=test_items,
            start_time=1.0,
            gap=25.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["items"] == test_items
        assert props["gap"] == 25.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.ThreeByThreeGrid.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, items=[], start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestThreeByThreeGridToolRegistration:
    """Tests for ThreeByThreeGrid MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func(items='[{"content": "test"}]'))

        result_data = json.loads(result)
        assert result_data["component"] == "ThreeByThreeGrid"

        # Verify component was added
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func(items="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        with patch.object(timeline, "add_three_by_three_grid", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(items='[{"content": "test"}]'))
            result_data = json.loads(result)
            assert "error" in result_data
            assert "Test error" in result_data["error"]

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(items="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid" in result_data["error"]

    def test_tool_execution_non_list_items(self):
        """Test tool execution when items is not a list."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with JSON string instead of list - should still work but skip the list processing
        # JSON string value will be parsed as a Python string, which is sliceable but not a list
        result = asyncio.run(tool_func(items='"test string"'))

        # Should succeed but with empty children
        result_data = json.loads(result)
        assert result_data["component"] == "ThreeByThreeGrid"

    def test_tool_execution_with_null_child(self):
        """Test tool execution when parse_nested_component returns None."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.ThreeByThreeGrid.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Mock parse_nested_component to return None
        with patch(
            "chuk_motion.components.layouts.ThreeByThreeGrid.tool.parse_nested_component",
            return_value=None,
        ):
            result = asyncio.run(tool_func(items='[{"title": "A"}]'))

        # Should still succeed, just with no children added
        result_data = json.loads(result)
        assert result_data["component"] == "ThreeByThreeGrid"
