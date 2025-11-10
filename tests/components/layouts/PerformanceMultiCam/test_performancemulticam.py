"""Tests for PerformanceMultiCam template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestPerformanceMultiCamBasic:
    """Basic PerformanceMultiCam generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic PerformanceMultiCam generation."""
        tsx = component_builder.build_component("PerformanceMultiCam", {}, theme_name)
        assert tsx is not None
        assert "PerformanceMultiCam" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "PerformanceMultiCam")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestPerformanceMultiCamBuilderMethod:
    """Tests for PerformanceMultiCam builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "PerformanceMultiCam"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        test_cams = [{"id": "cam1"}, {"id": "cam2"}]
        add_to_composition(
            builder,
            start_time=1.0,
            primary_cam={"type": "primary"},
            secondary_cams=test_cams,
            layout="grid",
            gap=25.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["primary_cam"] == {"type": "primary"}
        assert props["secondary_cams"] == test_cams
        assert props["layout"] == "grid"
        assert props["gap"] == 25.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestPerformanceMultiCamToolRegistration:
    """Tests for PerformanceMultiCam MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline_mock = Mock()
        component_mock = Mock()
        component_mock.start_frame = 0
        timeline_mock.add_component = Mock(return_value=component_mock)
        timeline_mock.frames_to_seconds = Mock(return_value=0.0)
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        primary_cam = json.dumps({"id": "primary", "angle": "front"})
        secondary_cams = json.dumps([{"id": "cam1"}, {"id": "cam2"}])

        result = asyncio.run(tool_func(
            primary_cam=primary_cam,
            secondary_cams=secondary_cams,
            layout="primary-main",
            gap=20,
            padding=40,
            duration=5.0,
            track="main",
            gap_before=None
        ))

        result_data = json.loads(result)
        assert result_data["component"] == "PerformanceMultiCam"
        assert result_data["layout"] == "primary-main"
        assert result_data["duration"] == 5.0

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON - should handle gracefully
        result = asyncio.run(tool_func(
            primary_cam="invalid json",
            secondary_cams="also invalid",
            layout="primary-main"
        ))

        # Should return error response
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

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
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline_mock = Mock()
        timeline_mock.add_component = Mock(side_effect=Exception("Test error"))
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_with_non_list_secondary_cams(self):
        """Test tool execution when secondary_cams is not a list."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.layouts.PerformanceMultiCam.tool import register_tool

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        timeline_mock = Mock()
        component_mock = Mock()
        component_mock.start_frame = 0
        timeline_mock.add_component = Mock(return_value=component_mock)
        timeline_mock.frames_to_seconds = Mock(return_value=0.0)
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Pass secondary_cams as a dict instead of a list to hit the else branch
        primary_cam = json.dumps({"id": "primary"})
        secondary_cams = json.dumps({"cam1": "data", "cam2": "data"})  # Dict, not list

        result = asyncio.run(tool_func(
            primary_cam=primary_cam,
            secondary_cams=secondary_cams,
            duration=5.0
        ))

        result_data = json.loads(result)
        assert result_data["component"] == "PerformanceMultiCam"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()
