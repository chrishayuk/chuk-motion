"""Tests for DeviceFrame template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestDeviceFrameBasic:
    """Basic DeviceFrame generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic DeviceFrame generation."""
        tsx = component_builder.build_component("DeviceFrame", {}, theme_name)
        assert tsx is not None
        assert "DeviceFrame" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "DeviceFrame")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestDeviceFrameBuilderMethod:
    """Tests for DeviceFrame builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.frames.DeviceFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, duration=5.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "DeviceFrame"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.frames.DeviceFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            duration=10.0,
            device="tablet",
            content="Test content",
            orientation="landscape",
            scale=1.5,
            glare=False,
            shadow=False,
            position="top-right",
        )

        props = builder.components[0].props
        assert props["device"] == "tablet"
        assert props["content"] == "Test content"
        assert props["orientation"] == "landscape"
        assert props["scale"] == 1.5
        assert props["glare"] is False
        assert props["shadow"] is False
        assert props["position"] == "top-right"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.frames.DeviceFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestDeviceFrameToolRegistration:
    """Tests for DeviceFrame MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.frames.DeviceFrame.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.frames.DeviceFrame.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        result = asyncio.run(tool_func(
            startFrame=0,
            durationInFrames=150,
            device="phone",
            content="",
            orientation="portrait",
            scale=1.0,
            glare=True,
            shadow=True,
            position="center"
        ))

        # Parse JSON response
        import json
        response = json.loads(result)

        # Check FrameComponentResponse structure
        assert "component" in response
        assert "position" in response
        assert "start_time" in response
        assert "duration" in response

        # Verify component was added
        project_mock.add_component_to_track.assert_called_once()

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import tempfile
        from unittest.mock import Mock

        from chuk_motion.components.frames.DeviceFrame.tool import register_tool
        from chuk_motion.utils.project_manager import ProjectManager

        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager(tmpdir)
            # Don't create or set active project

            mcp_mock = Mock()
            register_tool(mcp_mock, pm)

            tool_func = mcp_mock.tool.call_args[0][0]

            # Should return an error response when no project is set
            result = asyncio.run(tool_func(
                startFrame=0,
                durationInFrames=150
            ))

            import json
            response = json.loads(result)
            assert "error" in response

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.frames.DeviceFrame.tool import register_tool

        # Mock ProjectManager that raises an error
        pm_mock = Mock()
        pm_mock.get_active_project = Mock(side_effect=Exception("Test error"))

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # The error should propagate
        try:
            result = asyncio.run(tool_func(
                startFrame=0,
                durationInFrames=150,
                device="phone"
            ))
            # If we get here, check for error in result
            if result:
                assert "error" in result.lower() or "Test error" in result
        except Exception as e:
            # Error propagated as expected
            assert "Test error" in str(e)
