"""Tests for Terminal template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTerminalBasic:
    """Basic Terminal generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Terminal generation."""
        tsx = component_builder.build_component("Terminal", {}, theme_name)
        assert tsx is not None
        assert "Terminal" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Terminal")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestTerminalBuilderMethod:
    """Tests for Terminal builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.frames.Terminal.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, duration=5.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "Terminal"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.frames.Terminal.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            duration=10.0,
            commands='[{"command": "ls", "output": "file.txt"}]',
            prompt="zsh",
            custom_prompt=">",
            title="My Terminal",
            theme="light",
            width=1000,
            height=700,
            position="top-left",
            show_cursor=False,
            type_speed=0.1,
        )

        props = builder.components[0].props
        assert props["commands"] == '[{"command": "ls", "output": "file.txt"}]'
        assert props["prompt"] == "zsh"
        assert props["customPrompt"] == ">"
        assert props["title"] == "My Terminal"
        assert props["theme"] == "light"
        assert props["width"] == 1000
        assert props["height"] == 700
        assert props["position"] == "top-left"
        assert props["showCursor"] is False
        assert props["typeSpeed"] == 0.1

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.frames.Terminal.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestTerminalToolRegistration:
    """Tests for Terminal MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.frames.Terminal.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.frames.Terminal.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        commands = json.dumps([{"command": "ls", "output": "file.txt"}])
        result = asyncio.run(
            tool_func(
                startFrame=0,
                durationInFrames=150,
                commands=commands,
                prompt="bash",
                customPrompt="$",
                title="Terminal",
                theme="dark",
                width=900,
                height=600,
                position="center",
                showCursor=True,
                typeSpeed=0.05,
            )
        )

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

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.frames.Terminal.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON - should handle gracefully
        result = asyncio.run(
            tool_func(
                startFrame=0,
                durationInFrames=150,
                commands="invalid json",  # Invalid JSON
                prompt="bash",
                customPrompt="$",
                title="Terminal",
                theme="dark",
                width=900,
                height=600,
                position="center",
                showCursor=True,
                typeSpeed=0.05,
            )
        )

        # Should not crash, should handle gracefully with empty list
        assert result is not None
        # Parse JSON response
        import json

        response = json.loads(result)
        assert "component" in response

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import tempfile
        from unittest.mock import Mock

        from chuk_motion.components.frames.Terminal.tool import register_tool
        from chuk_motion.utils.async_project_manager import AsyncProjectManager as ProjectManager

        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager(tmpdir)
            # Don't create or set active project

            mcp_mock = Mock()
            register_tool(mcp_mock, pm)

            tool_func = mcp_mock.tool.call_args[0][0]

            # Should return an error response when no project is set
            result = asyncio.run(tool_func(startFrame=0, durationInFrames=150))

            import json

            response = json.loads(result)
            assert "error" in response

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.frames.Terminal.tool import register_tool

        # Mock ProjectManager with valid project but mock add_component_to_track to raise error
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track.side_effect = Exception("Component creation failed")
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Call tool which should catch the exception
        result = asyncio.run(tool_func(startFrame=0, durationInFrames=150))

        # Should return error response
        response = json.loads(result)
        assert "error" in response
        assert "Component creation failed" in response["error"]
