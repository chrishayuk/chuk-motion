"""Tests for StylizedWebPage component."""

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


class TestStylizedWebPageBasic:
    """Basic StylizedWebPage generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic StylizedWebPage generation."""
        tsx = component_builder.build_component(
            "StylizedWebPage", {"title": "Test", "subtitle": "Test Subtitle"}, theme_name
        )
        assert tsx is not None
        assert "StylizedWebPage" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "StylizedWebPage")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestStylizedWebPageBuilderMethod:
    """Tests for StylizedWebPage builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.content.StylizedWebPage.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(
            builder, title="Test Title", subtitle="Test Subtitle", start_time=0.0
        )

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "StylizedWebPage"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.content.StylizedWebPage.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            title="My App",
            subtitle="Amazing Features",
            start_time=1.0,
            show_header=True,
            show_sidebar=True,
            show_footer=True,
            header_text="Home • About • Contact",
            sidebar_items=["Dashboard", "Settings"],
            content_lines=["Line 1", "Line 2"],
            footer_text="© 2024 Test",
            theme="dark",
            accent_color="accent",
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["title"] == "My App"
        assert props["subtitle"] == "Amazing Features"
        assert props["showHeader"] is True
        assert props["showSidebar"] is True
        assert props["showFooter"] is True
        assert props["headerText"] == "Home • About • Contact"
        assert props["sidebarItems"] == ["Dashboard", "Settings"]
        assert props["contentLines"] == ["Line 1", "Line 2"]
        assert props["footerText"] == "© 2024 Test"
        assert props["theme"] == "dark"
        assert props["accentColor"] == "accent"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.content.StylizedWebPage.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, title="Test", subtitle="Test", start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150

    def test_add_to_composition_default_lists(self):
        """Test default values for sidebar_items and content_lines."""
        from chuk_motion.components.content.StylizedWebPage.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(builder, title="Test", subtitle="Test", start_time=0.0)

        props = builder.components[0].props
        assert props["sidebarItems"] == ["Dashboard", "Analytics", "Settings"]
        assert props["contentLines"] == [
            "Welcome to our site",
            "Explore our features",
            "Get started today",
        ]

    def test_add_to_composition_custom_lists(self):
        """Test custom values for sidebar_items and content_lines."""
        from chuk_motion.components.content.StylizedWebPage.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        custom_sidebar = ["Item 1", "Item 2"]
        custom_content = ["Content 1", "Content 2"]

        add_to_composition(
            builder,
            title="Test",
            subtitle="Test",
            start_time=0.0,
            sidebar_items=custom_sidebar,
            content_lines=custom_content,
        )

        props = builder.components[0].props
        assert props["sidebarItems"] == custom_sidebar
        assert props["contentLines"] == custom_content


class TestStylizedWebPageToolRegistration:
    """Tests for StylizedWebPage MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution_basic(self):
        """Test basic tool execution."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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
        assert result_data["component"] == "StylizedWebPage"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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

        result = asyncio.run(
            tool_func(
                title="My Amazing App",
                subtitle="Build something incredible",
                show_header=True,
                show_sidebar=True,
                show_footer=True,
                header_text="Home • About • Contact",
                sidebar_items=["Dashboard", "Analytics", "Settings"],
                content_lines=["Welcome", "Explore", "Get started"],
                footer_text="© 2024 My Company",
                theme="dark",
                accent_color="secondary",
                duration=5.0,
                track="overlay",
                gap_before=1.0,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "StylizedWebPage"
        assert result_data["start_time"] == 2.0

        # Verify component was added with correct params
        call_args = timeline_mock.add_component.call_args
        assert call_args[1]["duration"] == 5.0
        assert call_args[1]["track"] == "overlay"
        assert call_args[1]["gap_before"] == 1.0

    def test_tool_execution_default_sidebar_items(self):
        """Test tool execution with default sidebar_items."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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

        result = asyncio.run(tool_func(sidebar_items=None))

        result_data = json.loads(result)
        assert result_data["component"] == "StylizedWebPage"

        # Verify the component props have default sidebar items
        call_args = timeline_mock.add_component.call_args
        component_instance = call_args[0][0]
        assert component_instance.props["sidebarItems"] == ["Dashboard", "Analytics", "Settings"]

    def test_tool_execution_default_content_lines(self):
        """Test tool execution with default content_lines."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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

        result = asyncio.run(tool_func(content_lines=None))

        result_data = json.loads(result)
        assert result_data["component"] == "StylizedWebPage"

        # Verify the component props have default content lines
        call_args = timeline_mock.add_component.call_args
        component_instance = call_args[0][0]
        assert component_instance.props["contentLines"] == [
            "Welcome to our site",
            "Explore our features",
            "Get started today",
        ]

    def test_tool_execution_custom_lists(self):
        """Test tool execution with custom lists."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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

        custom_sidebar = ["Custom 1", "Custom 2"]
        custom_content = ["Line A", "Line B"]

        result = asyncio.run(tool_func(sidebar_items=custom_sidebar, content_lines=custom_content))

        result_data = json.loads(result)
        assert result_data["component"] == "StylizedWebPage"

        # Verify the component props have custom values
        call_args = timeline_mock.add_component.call_args
        component_instance = call_args[0][0]
        assert component_instance.props["sidebarItems"] == custom_sidebar
        assert component_instance.props["contentLines"] == custom_content

    @pytest.mark.parametrize("theme", ["light", "dark"])
    def test_tool_execution_themes(self, theme):
        """Test tool execution with different themes."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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
        assert result_data["component"] == "StylizedWebPage"

    @pytest.mark.parametrize("accent_color", ["primary", "accent", "secondary"])
    def test_tool_execution_accent_colors(self, accent_color):
        """Test tool execution with different accent colors."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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

        result = asyncio.run(tool_func(accent_color=accent_color))

        result_data = json.loads(result)
        assert result_data["component"] == "StylizedWebPage"

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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
        from chuk_motion.components.content.StylizedWebPage.tool import register_tool

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
