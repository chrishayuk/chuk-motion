"""Tests for LayoutEntrance component."""

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


class TestLayoutEntranceBasic:
    """Basic LayoutEntrance generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LayoutEntrance generation."""
        tsx = component_builder.build_component("LayoutEntrance", {}, theme_name)
        assert tsx is not None
        assert "LayoutEntrance" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "LayoutEntrance")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestLayoutEntranceBuilderMethod:
    """Tests for LayoutEntrance builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.animations.LayoutEntrance.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "LayoutEntrance"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.animations.LayoutEntrance.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            content={"type": "Grid"},
            entrance_type="fade_slide_up",
            entrance_delay=0.5,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["content"] == {"type": "Grid"}
        assert props["entrance_type"] == "fade_slide_up"
        assert props["entrance_delay"] == 0.5

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.animations.LayoutEntrance.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestLayoutEntranceToolRegistration:
    """Tests for LayoutEntrance MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution_basic(self):
        """Test basic tool execution with valid content."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

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

        # Create valid content
        content = json.dumps({"type": "Grid", "config": {"layout": "3x3"}})

        result = asyncio.run(tool_func(content=content))

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutEntrance"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

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

        content = json.dumps({"type": "Container", "config": {"position": "center"}})

        result = asyncio.run(
            tool_func(
                content=content,
                entrance_type="scale_in_pop",
                entrance_delay=0.5,
                duration=5.0,
                track="overlay",
                gap_before=1.0,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutEntrance"
        assert result_data["start_time"] == 2.0

        # Verify component was added with correct params
        call_args = timeline_mock.add_component.call_args
        assert call_args[1]["duration"] == 5.0
        assert call_args[1]["track"] == "overlay"
        assert call_args[1]["gap_before"] == 1.0

    @pytest.mark.parametrize(
        "entrance_type",
        [
            "none",
            "fade_in",
            "fade_slide_up",
            "scale_in_soft",
            "scale_in_pop",
            "slide_in_left",
            "slide_in_right",
            "blur_in",
            "zoom_in",
        ],
    )
    def test_tool_execution_entrance_types(self, entrance_type):
        """Test tool execution with different entrance types."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

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

        content = json.dumps({"type": "TitleScene", "config": {"text": "Hello"}})

        result = asyncio.run(
            tool_func(
                content=content,
                entrance_type=entrance_type,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "LayoutEntrance"

    def test_tool_execution_invalid_entrance_type(self):
        """Test tool execution with invalid entrance type."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        content = json.dumps({"type": "TitleScene", "config": {"text": "Hello"}})

        result = asyncio.run(
            tool_func(
                content=content,
                entrance_type="invalid_type",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid entrance_type" in result_data["error"]

    def test_tool_execution_invalid_json_content(self):
        """Test tool execution with invalid JSON in content."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(
            tool_func(
                content="invalid json",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid JSON" in result_data["error"]

    def test_tool_execution_invalid_content_format(self):
        """Test tool execution with invalid content format."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

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

        # Missing 'type' key
        content = json.dumps({"config": {"text": "Missing type"}})

        result = asyncio.run(tool_func(content=content))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid content format" in result_data["error"]

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        content = json.dumps({"type": "TitleScene", "config": {"text": "Hello"}})

        result = asyncio.run(tool_func(content=content))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        from chuk_motion.components.animations.LayoutEntrance.tool import register_tool

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline_mock = Mock()
        timeline_mock.add_component = Mock(side_effect=Exception("Test error"))
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        content = json.dumps({"type": "TitleScene", "config": {"text": "Hello"}})

        result = asyncio.run(tool_func(content=content))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]


class TestLayoutEntranceRenderer:
    """Tests for LayoutEntrance custom JSX renderer."""

    def test_render_jsx_with_content(self):
        """Test render_jsx with valid content ComponentInstance."""
        from chuk_motion.components.animations.LayoutEntrance.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create nested content
        content = ComponentInstance(
            component_type="Grid",
            start_frame=0,
            duration_frames=150,
            props={"layout": "3x3"},
            layer=0,
        )

        # Create LayoutEntrance component with content
        comp = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=150,
            props={"content": content, "entranceType": "fade_in"},
            layer=0,
        )

        # Mock functions
        def mock_render_child(child, indent):
            return f"{' ' * indent}<Grid />"

        def mock_snake_to_camel(s):
            parts = s.split("_")
            return parts[0] + "".join(p.capitalize() for p in parts[1:])

        def mock_format_prop_value(v):
            if isinstance(v, str):
                return f'"{v}"'
            return f"{{{v}}}"

        result = render_jsx(
            comp,
            mock_render_child,
            0,
            mock_snake_to_camel,
            mock_format_prop_value,
        )

        assert result is not None
        assert "LayoutEntrance" in result
        assert "entranceType" in result
        assert "<Grid />" in result

    def test_render_jsx_no_content(self):
        """Test render_jsx returns None when no content."""
        from chuk_motion.components.animations.LayoutEntrance.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create LayoutEntrance without content
        comp = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=150,
            props={"entranceType": "fade_in"},
            layer=0,
        )

        result = render_jsx(comp, None, 0, None, None)
        assert result is None

    def test_render_jsx_content_not_component_instance(self):
        """Test render_jsx returns None when content is not ComponentInstance."""
        from chuk_motion.components.animations.LayoutEntrance.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create LayoutEntrance with invalid content (not ComponentInstance)
        comp = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=150,
            props={"content": {"type": "Grid"}, "entranceType": "fade_in"},
            layer=0,
        )

        result = render_jsx(comp, None, 0, None, None)
        assert result is None

    def test_render_jsx_with_props(self):
        """Test render_jsx with multiple props."""
        from chuk_motion.components.animations.LayoutEntrance.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create nested content
        content = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=150,
            props={},
            layer=0,
        )

        # Create LayoutEntrance with multiple props
        comp = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=150,
            props={
                "content": content,
                "entranceType": "scale_in_pop",
                "entranceDelay": 0.5,
            },
            layer=0,
        )

        def mock_render_child(child, indent):
            return f"{' ' * indent}<Container />"

        def mock_snake_to_camel(s):
            parts = s.split("_")
            return parts[0] + "".join(p.capitalize() for p in parts[1:])

        def mock_format_prop_value(v):
            if isinstance(v, str):
                return f'"{v}"'
            return f"{{{v}}}"

        result = render_jsx(
            comp,
            mock_render_child,
            0,
            mock_snake_to_camel,
            mock_format_prop_value,
        )

        assert result is not None
        assert "entranceType" in result
        assert "entranceDelay" in result
        assert "<Container />" in result

    def test_render_jsx_without_props(self):
        """Test render_jsx with no props besides content."""
        from chuk_motion.components.animations.LayoutEntrance.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create nested content
        content = ComponentInstance(
            component_type="Grid",
            start_frame=0,
            duration_frames=150,
            props={},
            layer=0,
        )

        # Create LayoutEntrance with only content
        comp = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=150,
            props={"content": content},
            layer=0,
        )

        def mock_render_child(child, indent):
            return f"{' ' * indent}<Grid />"

        def mock_snake_to_camel(s):
            return s

        def mock_format_prop_value(v):
            return f"{{{v}}}"

        result = render_jsx(
            comp,
            mock_render_child,
            0,
            mock_snake_to_camel,
            mock_format_prop_value,
        )

        assert result is not None
        assert "LayoutEntrance" in result
        assert "startFrame" in result
        assert "durationInFrames" in result
        assert "<Grid />" in result
