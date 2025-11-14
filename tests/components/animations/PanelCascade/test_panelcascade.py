"""Tests for PanelCascade component."""

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


class TestPanelCascadeBasic:
    """Basic PanelCascade generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic PanelCascade generation."""
        tsx = component_builder.build_component("PanelCascade", {}, theme_name)
        assert tsx is not None
        assert "PanelCascade" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "PanelCascade")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestPanelCascadeBuilderMethod:
    """Tests for PanelCascade builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.animations.PanelCascade.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "PanelCascade"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.animations.PanelCascade.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        test_items = [{"type": "CodeBlock"}, {"type": "DemoBox"}]
        add_to_composition(
            builder,
            start_time=1.0,
            items=test_items,
            cascade_type="bounce_in",
            stagger_delay=0.12,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["items"] == test_items
        assert props["cascade_type"] == "bounce_in"
        assert props["stagger_delay"] == 0.12

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.animations.PanelCascade.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150

    def test_add_to_composition_default_items(self):
        """Test default empty items list."""
        from chuk_motion.components.animations.PanelCascade.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(builder, start_time=0.0)

        props = builder.components[0].props
        assert props["items"] == []


class TestPanelCascadeToolRegistration:
    """Tests for PanelCascade MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution_basic(self):
        """Test basic tool execution with valid items."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

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

        # Create valid items array
        items = json.dumps(
            [
                {"type": "CodeBlock", "config": {"code": "Panel 1"}},
                {"type": "CodeBlock", "config": {"code": "Panel 2"}},
            ]
        )

        result = asyncio.run(tool_func(items=items))

        result_data = json.loads(result)
        assert result_data["component"] == "PanelCascade"

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_all_params(self):
        """Test tool execution with all parameters."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

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

        items = json.dumps(
            [
                {"type": "DemoBox", "config": {}},
                {"type": "Counter", "config": {"start_value": 0, "end_value": 100}},
            ]
        )

        result = asyncio.run(
            tool_func(
                items=items,
                cascade_type="wave",
                stagger_delay=0.1,
                duration=5.0,
                track="overlay",
                gap_before=1.0,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "PanelCascade"
        assert result_data["start_time"] == 2.0

        # Verify component was added with correct params
        call_args = timeline_mock.add_component.call_args
        assert call_args[1]["duration"] == 5.0
        assert call_args[1]["track"] == "overlay"
        assert call_args[1]["gap_before"] == 1.0

    @pytest.mark.parametrize(
        "cascade_type",
        [
            "from_edges",
            "from_center",
            "bounce_in",
            "sequential_left",
            "sequential_right",
            "sequential_top",
            "wave",
        ],
    )
    def test_tool_execution_cascade_types(self, cascade_type):
        """Test tool execution with different cascade types."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

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

        items = json.dumps(
            [
                {"type": "CodeBlock", "config": {"code": "Panel"}},
            ]
        )

        result = asyncio.run(
            tool_func(
                items=items,
                cascade_type=cascade_type,
            )
        )

        result_data = json.loads(result)
        assert result_data["component"] == "PanelCascade"

    def test_tool_execution_invalid_cascade_type(self):
        """Test tool execution with invalid cascade type."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        items = json.dumps([{"type": "CodeBlock", "config": {}}])

        result = asyncio.run(
            tool_func(
                items=items,
                cascade_type="invalid_type",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid cascade_type" in result_data["error"]

    def test_tool_execution_invalid_json_items(self):
        """Test tool execution with invalid JSON in items."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(
            tool_func(
                items="invalid json",
            )
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid JSON" in result_data["error"]

    def test_tool_execution_items_not_array(self):
        """Test tool execution when items is not an array."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        pm_mock = Mock()
        timeline_mock = Mock()
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Items is a dict, not an array
        items = json.dumps({"not": "an array"})

        result = asyncio.run(tool_func(items=items))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "items must be a JSON array" in result_data["error"]

    def test_tool_execution_invalid_item_format(self):
        """Test tool execution with invalid item format."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

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

        # Missing 'type' key in one item
        items = json.dumps(
            [
                {"type": "CodeBlock", "config": {"code": "Valid"}},
                {"config": {"code": "Missing type"}},
            ]
        )

        result = asyncio.run(tool_func(items=items))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid item format" in result_data["error"]

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        items = json.dumps([{"type": "CodeBlock", "config": {}}])

        result = asyncio.run(tool_func(items=items))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        from chuk_motion.components.animations.PanelCascade.tool import register_tool

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline_mock = Mock()
        timeline_mock.add_component = Mock(side_effect=Exception("Test error"))
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        items = json.dumps([{"type": "CodeBlock", "config": {}}])

        result = asyncio.run(tool_func(items=items))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]


class TestPanelCascadeRenderer:
    """Tests for PanelCascade custom JSX renderer."""

    def test_render_jsx_with_items(self):
        """Test render_jsx with valid item ComponentInstances."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create panel items
        item1 = ComponentInstance(
            component_type="CodeBlock",
            start_frame=0,
            duration_frames=150,
            props={"code": "Panel 1"},
            layer=0,
        )
        item2 = ComponentInstance(
            component_type="CodeBlock",
            start_frame=0,
            duration_frames=150,
            props={"code": "Panel 2"},
            layer=0,
        )

        # Create PanelCascade component with items
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={"items": [item1, item2], "cascadeType": "from_edges"},
            layer=0,
        )

        # Mock functions
        def mock_render_child(child, indent):
            return f"{' ' * indent}<{child.component_type} />"

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
        assert "PanelCascade" in result
        assert "cascadeType" in result
        assert "<CodeBlock />" in result

    def test_render_jsx_no_items(self):
        """Test render_jsx returns None when no items."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create PanelCascade without items
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={"cascadeType": "from_edges"},
            layer=0,
        )

        result = render_jsx(comp, None, 0, None, None)
        assert result is None

    def test_render_jsx_items_not_list(self):
        """Test render_jsx returns None when items is not a list."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create PanelCascade with items as dict (not list)
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={"items": {"not": "a list"}, "cascadeType": "from_edges"},
            layer=0,
        )

        result = render_jsx(comp, None, 0, None, None)
        assert result is None

    def test_render_jsx_empty_items_list(self):
        """Test render_jsx returns None when items list is empty."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create PanelCascade with empty items list
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={"items": [], "cascadeType": "from_edges"},
            layer=0,
        )

        result = render_jsx(comp, None, 0, None, None)
        assert result is None

    def test_render_jsx_items_not_component_instances(self):
        """Test render_jsx returns None when items are not ComponentInstances."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create PanelCascade with items that aren't ComponentInstances
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={
                "items": [{"type": "CodeBlock"}, {"type": "DemoBox"}],
                "cascadeType": "from_edges",
            },
            layer=0,
        )

        def mock_render_child(child, indent):
            return f"<{child.component_type} />"

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
        assert result is None

    def test_render_jsx_with_props(self):
        """Test render_jsx with multiple props."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create panel items
        item1 = ComponentInstance(
            component_type="DemoBox",
            start_frame=0,
            duration_frames=150,
            props={},
            layer=0,
        )

        # Create PanelCascade with multiple props
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={
                "items": [item1],
                "cascadeType": "bounce_in",
                "staggerDelay": 0.12,
            },
            layer=0,
        )

        def mock_render_child(child, indent):
            return f"{' ' * indent}<{child.component_type} />"

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
        assert "cascadeType" in result
        assert "staggerDelay" in result
        assert "<DemoBox />" in result

    def test_render_jsx_without_props(self):
        """Test render_jsx with no props besides items."""
        from chuk_motion.components.animations.PanelCascade.renderer import render_jsx
        from chuk_motion.generator.composition_builder import ComponentInstance

        # Create panel items
        item1 = ComponentInstance(
            component_type="CodeBlock",
            start_frame=0,
            duration_frames=150,
            props={},
            layer=0,
        )

        # Create PanelCascade with only items
        comp = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=150,
            props={"items": [item1]},
            layer=0,
        )

        def mock_render_child(child, indent):
            return f"{' ' * indent}<{child.component_type} />"

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
        assert "PanelCascade" in result
        assert "startFrame" in result
        assert "durationInFrames" in result
        assert "<CodeBlock />" in result
