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

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        lines = json.dumps([{"type": "added", "content": "new line"}])
        result = asyncio.run(
            tool_func(
                startFrame=0,
                durationInFrames=150,
                lines=lines,
                mode="unified",
                language="typescript",
                showLineNumbers=True,
                showHeatmap=False,
                title="Code Comparison",
                leftLabel="Before",
                rightLabel="After",
                theme="dark",
                width=1400,
                height=800,
                position="center",
                animateLines=True,
            )
        )

        # Parse JSON response
        import json

        response = json.loads(result)

        # Check Pydantic response structure
        assert response["component"] == "CodeDiff"
        assert "start_time" in response
        assert "duration" in response
        assert isinstance(response["start_time"], (int, float))
        assert isinstance(response["duration"], (int, float))

        # Verify component was added
        project_mock.add_component_to_track.assert_called_once()

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool

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
                lines="invalid json",  # Invalid JSON
                mode="unified",
                language="typescript",
                showLineNumbers=True,
                showHeatmap=False,
                title="Code Comparison",
                leftLabel="Before",
                rightLabel="After",
                theme="dark",
                width=1400,
                height=800,
                position="center",
                animateLines=True,
            )
        )

        # Should not crash, should handle gracefully and return success (invalid JSON becomes empty array)
        import json

        assert result is not None
        response = json.loads(result)
        assert response["component"] == "CodeDiff"

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import tempfile
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool
        from chuk_motion.utils.async_project_manager import AsyncProjectManager as ProjectManager

        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager(tmpdir)
            # Don't create or set active project

            mcp_mock = Mock()
            register_tool(mcp_mock, pm)

            tool_func = mcp_mock.tool.call_args[0][0]

            # Should return an error response when no project is set
            result = asyncio.run(tool_func(startFrame=0, durationInFrames=150, lines="[]"))

            import json

            response = json.loads(result)
            assert "error" in response

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeDiff.tool import register_tool

        # Mock ProjectManager with valid project but mock add_component_to_track to raise error
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track.side_effect = Exception("Component creation failed")
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Call tool which should catch the exception
        result = asyncio.run(tool_func(startFrame=0, durationInFrames=150, lines="[]"))

        # Should return error response
        response = json.loads(result)
        assert "error" in response
        assert "Component creation failed" in response["error"]
