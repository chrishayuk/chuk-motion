"""Tests for CodeDiff template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestCodeDiffBasic:
    """Basic CodeDiff generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic CodeDiff generation."""
        tsx = component_builder.build_component("CodeDiff", {}, theme_name)
        assert tsx is not None
        assert "CodeDiff" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "CodeDiff")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestCodeDiffBuilderMethod:
    """Tests for CodeDiff builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.code.CodeDiff.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, duration=5.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "CodeDiff"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.code.CodeDiff.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            duration=10.0,
            lines='[{"type": "add", "content": "new line"}]',
            mode="split",
            language="python",
            show_line_numbers=False,
            show_heatmap=True,
            title="My Code Diff",
            left_label="Old",
            right_label="New",
            theme="light",
            width=1600,
            height=900,
            position="top-left",
            animate_lines=False,
        )

        props = builder.components[0].props
        assert props["lines"] == '[{"type": "add", "content": "new line"}]'
        assert props["mode"] == "split"
        assert props["language"] == "python"
        assert props["showLineNumbers"] is False
        assert props["showHeatmap"] is True
        assert props["title"] == "My Code Diff"
        assert props["leftLabel"] == "Old"
        assert props["rightLabel"] == "New"
        assert props["theme"] == "light"
        assert props["width"] == 1600
        assert props["height"] == 900
        assert props["position"] == "top-left"
        assert props["animateLines"] is False

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.code.CodeDiff.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestCodeDiffToolRegistration:
    """Tests for CodeDiff MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Execute with all parameters
        lines = json.dumps([{"type": "added", "content": "new line"}])
        result = asyncio.run(
            tool_func(
                duration=5.0,
                lines=lines,
                mode="unified",
                language="typescript",
                show_line_numbers=True,
                show_heatmap=False,
                title="Code Comparison",
                left_label="Before",
                right_label="After",
                theme="dark",
                width=1400,
                height=800,
                position="center",
                animate_lines=True,
            )
        )

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "CodeDiff"

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Test with invalid JSON - should handle gracefully
        result = asyncio.run(
            tool_func(
                duration=5.0,
                lines="invalid json",  # Invalid JSON
                mode="unified",
                language="typescript",
                show_line_numbers=True,
                show_heatmap=False,
                title="Code Comparison",
                left_label="Before",
                right_label="After",
                theme="dark",
                width=1400,
                height=800,
                position="center",
                animate_lines=True,
            )
        )

        # Should not crash, should handle gracefully and return success (invalid JSON becomes empty array)
        assert result is not None
        response = json.loads(result)
        assert response["component"] == "CodeDiff"

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Should return an error response when no project is set
        result = asyncio.run(tool_func(duration=5.0, lines="[]"))

        response = json.loads(result)
        assert "error" in response
        assert "No active project" in response["error"]

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.code.CodeDiff.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_code_diff to raise exception
        with patch.object(timeline, "add_code_diff", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(duration=5.0, lines="[]"))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
