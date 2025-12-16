"""Tests for Mosaic template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestMosaicBasic:
    """Basic Mosaic generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Mosaic generation."""
        tsx = component_builder.build_component("Mosaic", {}, theme_name)
        assert tsx is not None
        assert "Mosaic" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Mosaic")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestMosaicBuilderMethod:
    """Tests for Mosaic builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.Mosaic.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Mosaic"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.Mosaic.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        test_clips = [{"id": "clip1"}, {"id": "clip2"}]
        add_to_composition(
            builder,
            start_time=1.0,
            clips=test_clips,
            style="grid",
            gap=15.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["clips"] == test_clips
        assert props["style"] == "grid"
        assert props["gap"] == 15.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.Mosaic.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestMosaicToolRegistration:
    """Tests for Mosaic MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "Mosaic"

        # Verify component was added
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.Mosaic.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        with patch.object(timeline, "add_mosaic", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func())
            result_data = json.loads(result)
            assert "error" in result_data

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(clips="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid" in result_data["error"]

    def test_tool_execution_clips_not_list(self):
        """Test tool execution when clips is not a list."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with clips as a dict, not a list
        clips_json = json.dumps({"not": "a list"})

        result = asyncio.run(tool_func(clips=clips_json))

        result_data = json.loads(result)
        assert result_data["component"] == "Mosaic"
        assert len(timeline.get_all_components()) >= 1

    def test_tool_execution_clips_with_none_items(self):
        """Test tool execution when some clip items parse to None."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.Mosaic.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline = Timeline(fps=30)
        pm_mock.current_timeline = timeline

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with clips that include items without 'type' (will parse to non-ComponentInstance)
        clips_json = json.dumps(
            [
                {"type": "CodeBlock", "config": {"code": "Valid"}},
                {"config": {"code": "Invalid - no type"}},  # This won't become a ComponentInstance
                None,  # This will also not become a ComponentInstance
            ]
        )

        result = asyncio.run(tool_func(clips=clips_json))

        result_data = json.loads(result)
        assert result_data["component"] == "Mosaic"
        assert len(timeline.get_all_components()) >= 1
