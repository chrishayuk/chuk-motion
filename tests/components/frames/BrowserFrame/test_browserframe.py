"""Tests for BrowserFrame template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestBrowserFrameBasic:
    """Basic BrowserFrame generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic BrowserFrame generation."""
        tsx = component_builder.build_component("BrowserFrame", {}, theme_name)
        assert tsx is not None
        assert "BrowserFrame" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "BrowserFrame")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestBrowserFrameBuilderMethod:
    """Tests for BrowserFrame builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.frames.BrowserFrame.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, duration=5.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "BrowserFrame"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.frames.BrowserFrame.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            duration=10.0,
            url="https://example.org",
            theme="firefox",
            tabs='[{"title": "Tab 1", "url": "https://example.org"}]',
            show_status=True,
            status_text="Loading...",
            content="Page content",
            width=1400,
            height=900,
            position="bottom-right",
            shadow=False,
        )

        props = builder.components[0].props
        assert props["url"] == "https://example.org"
        assert props["theme"] == "firefox"
        assert props["tabs"] == '[{"title": "Tab 1", "url": "https://example.org"}]'
        assert props["showStatus"] is True
        assert props["statusText"] == "Loading..."
        assert props["content"] == "Page content"
        assert props["width"] == 1400
        assert props["height"] == 900
        assert props["position"] == "bottom-right"
        assert props["shadow"] is False

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.frames.BrowserFrame.builder import (
            add_to_composition,
        )
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestBrowserFrameToolRegistration:
    """Tests for BrowserFrame MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.frames.BrowserFrame.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.frames.BrowserFrame.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        tabs = json.dumps([{"title": "Tab 1", "url": "https://example.com"}])
        result = asyncio.run(tool_func(
            startFrame=0,
            durationInFrames=150,
            url="https://example.com",
            theme="chrome",
            tabs=tabs,
            showStatus=False,
            statusText="",
            content="",
            width=1200,
            height=800,
            position="center",
            shadow=True
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

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.frames.BrowserFrame.tool import register_tool

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
            startFrame=0,
            durationInFrames=150,
            url="https://example.com",
            theme="chrome",
            tabs="invalid json",  # Invalid JSON
            showStatus=False,
            statusText="",
            content="",
            width=1200,
            height=800,
            position="center",
            shadow=True
        ))

        # Should not crash, should handle gracefully
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

        from chuk_mcp_remotion.components.frames.BrowserFrame.tool import register_tool
        from chuk_mcp_remotion.utils.project_manager import ProjectManager

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

        from chuk_mcp_remotion.components.frames.BrowserFrame.tool import register_tool

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
                url="https://example.com"
            ))
            # If we get here, check for error in result
            if result:
                assert "error" in result.lower() or "Test error" in result
        except Exception as e:
            # Error propagated as expected
            assert "Test error" in str(e)
