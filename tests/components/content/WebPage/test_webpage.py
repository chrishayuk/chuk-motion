"""Tests for WebPage component."""

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


class TestWebPageBasic:
    """Basic WebPage generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic WebPage generation."""
        tsx = component_builder.build_component("WebPage", {"html": "<h1>Test</h1>"}, theme_name)
        assert tsx is not None
        assert "WebPage" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "WebPage")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestWebPageBuilderMethod:
    """Tests for WebPage builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.content.WebPage.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, html="<h1>Hello World</h1>", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "WebPage"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.content.WebPage.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            html="<div><h1>Title</h1><p>Content</p></div>",
            start_time=1.0,
            css="h1 { color: red; }",
            base_styles=False,
            scale=1.5,
            scroll_y=100,
            animate_scroll=True,
            scroll_duration=90,
            theme="dark",
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["html"] == "<div><h1>Title</h1><p>Content</p></div>"
        assert props["css"] == "h1 { color: red; }"
        assert props["baseStyles"] is False
        assert props["scale"] == 1.5
        assert props["scrollY"] == 100
        assert props["animateScroll"] is True
        assert props["scrollDuration"] == 90
        assert props["theme"] == "dark"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.content.WebPage.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, html="<h1>Test</h1>", start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150

    def test_add_to_composition_default_values(self):
        """Test default values are applied correctly."""
        from chuk_motion.components.content.WebPage.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(builder, html="<h1>Test</h1>", start_time=0.0)

        props = builder.components[0].props
        assert props["css"] == ""
        assert props["baseStyles"] is True
        assert props["scale"] == 1.0
        assert props["scrollY"] == 0
        assert props["animateScroll"] is False
        assert props["scrollDuration"] == 60
        assert props["theme"] == "light"


class TestWebPageToolRegistration:
    """Tests for WebPage MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.content.WebPage.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution_basic(self):
        """Test basic tool execution."""
        from chuk_motion.components.content.WebPage.tool import register_tool

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

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "WebPage"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.content.WebPage.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        component_mock = Mock()
        component_mock.start_frame = 60
        timeline_mock.add_component = Mock(return_value=component_mock)
        timeline_mock.frames_to_seconds = Mock(return_value=2.0)
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        html = "<header><h1>My Page</h1></header>"
        css = "h1 { color: blue; }"

        result = asyncio.run(
            tool_func(
                html=html,
                css=css,
                base_styles=False,
                scale=1.2,
                scroll_y=200,
                animate_scroll=True,
                scroll_duration=120,
                theme="dark",
                duration=5.0,
                track="overlay",
                gap_before=1.0,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "WebPage"
        assert result_data["start_time"] == 2.0

        # Verify component was added with correct params
        call_args = timeline_mock.add_component.call_args
        assert call_args[1]["duration"] == 5.0
        assert call_args[1]["track"] == "overlay"
        assert call_args[1]["gap_before"] == 1.0

        # Verify component props
        component_instance = call_args[0][0]
        assert component_instance.props["html"] == html
        assert component_instance.props["css"] == css
        assert component_instance.props["baseStyles"] is False
        assert component_instance.props["scale"] == 1.2
        assert component_instance.props["scrollY"] == 200
        assert component_instance.props["animateScroll"] is True
        assert component_instance.props["scrollDuration"] == 120
        assert component_instance.props["theme"] == "dark"

    def test_tool_execution_default_values(self):
        """Test tool execution with default values."""
        from chuk_motion.components.content.WebPage.tool import register_tool

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

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "WebPage"

        # Verify default values
        call_args = timeline_mock.add_component.call_args
        component_instance = call_args[0][0]
        assert component_instance.props["css"] == ""
        assert component_instance.props["baseStyles"] is True
        assert component_instance.props["scale"] == 1.0
        assert component_instance.props["scrollY"] == 0
        assert component_instance.props["animateScroll"] is False
        assert component_instance.props["scrollDuration"] == 60
        assert component_instance.props["theme"] == "light"

    @pytest.mark.parametrize("theme", ["light", "dark"])
    def test_tool_execution_themes(self, theme):
        """Test tool execution with different themes."""
        from chuk_motion.components.content.WebPage.tool import register_tool

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

        result = asyncio.run(tool_func(theme=theme))

        result_data = json.loads(result)
        assert result_data["component"] == "WebPage"

    def test_tool_execution_scroll_animation(self):
        """Test tool execution with scroll animation."""
        from chuk_motion.components.content.WebPage.tool import register_tool

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

        result = asyncio.run(tool_func(scroll_y=500, animate_scroll=True, scroll_duration=180))

        result_data = json.loads(result)
        assert result_data["component"] == "WebPage"

        # Verify scroll props
        call_args = timeline_mock.add_component.call_args
        component_instance = call_args[0][0]
        assert component_instance.props["scrollY"] == 500
        assert component_instance.props["animateScroll"] is True
        assert component_instance.props["scrollDuration"] == 180

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        from chuk_motion.components.content.WebPage.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        from chuk_motion.components.content.WebPage.tool import register_tool

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
        assert "Test error" in result_data["error"]
