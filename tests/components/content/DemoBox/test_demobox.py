"""Tests for DemoBox template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestDemoBoxBasic:
    """Basic DemoBox generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic DemoBox generation."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)
        assert tsx is not None
        assert "DemoBox" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "DemoBox")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestDemoBoxBuilderMethod:
    """Tests for DemoBox builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.content.DemoBox.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, label="Test", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "DemoBox"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.content.DemoBox.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            label="My Label",
            start_time=1.0,
            color="secondary",
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["label"] == "My Label"
        assert props["color"] == "secondary"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.content.DemoBox.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, label="Test", start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestDemoBoxToolRegistration:
    """Tests for DemoBox MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.content.DemoBox.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.content.DemoBox.tool import register_tool

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
        result = asyncio.run(tool_func(
            label="Test Label",
            color="primary",
            duration=5.0,
            track="main",
            gap_before=None
        ))

        # Parse JSON response
        result_data = json.loads(result)
        assert result_data["component"] == "DemoBox"
        assert result_data["duration"] == 5.0

        # Verify component was added
        timeline_mock.add_component.assert_called_once()

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.content.DemoBox.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func(label="Test"))
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.content.DemoBox.tool import register_tool

        # Mock ProjectManager with timeline that raises an error
        pm_mock = Mock()
        timeline_mock = Mock()
        timeline_mock.add_component = Mock(side_effect=Exception("Test error"))
        pm_mock.current_timeline = timeline_mock

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func(label="Test"))
        result_data = json.loads(result)
        assert "error" in result_data
