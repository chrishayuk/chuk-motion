"""Tests for DialogueFrame template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestDialogueFrameBasic:
    """Basic DialogueFrame generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic DialogueFrame generation."""
        tsx = component_builder.build_component("DialogueFrame", {}, theme_name)
        assert tsx is not None
        assert "DialogueFrame" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "DialogueFrame")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestDialogueFrameBuilderMethod:
    """Tests for DialogueFrame builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.DialogueFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "DialogueFrame"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.DialogueFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            left_speaker={"type": "left"},
            right_speaker={"type": "right"},
            center_content={"type": "center"},
            speaker_size=45.0,
            gap=25.0,
            padding=50.0,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["left_speaker"] == {"type": "left"}
        assert props["right_speaker"] == {"type": "right"}
        assert props["center_content"] == {"type": "center"}
        assert props["speaker_size"] == 45.0
        assert props["gap"] == 25.0
        assert props["padding"] == 50.0

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.DialogueFrame.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestDialogueFrameToolRegistration:
    """Tests for DialogueFrame MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.DialogueFrame.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.DialogueFrame.tool import register_tool
        from chuk_motion.generator.composition_builder import CompositionBuilder

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        builder = CompositionBuilder(fps=30)
        pm_mock.current_timeline = builder

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())

        result_data = json.loads(result)
        assert result_data["component"] == "DialogueFrame"

        # Verify component was added
        assert len(builder.components) >= 1

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.DialogueFrame.tool import register_tool

        # Mock ProjectManager with no current_timeline
        pm_mock = Mock()
        pm_mock.current_timeline = None

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        result = asyncio.run(tool_func())
        result_data = json.loads(result)
        assert "error" in result_data

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.layouts.DialogueFrame.tool import register_tool
        from chuk_motion.generator.composition_builder import CompositionBuilder

        # Mock ProjectManager with builder that raises an error
        pm_mock = Mock()
        builder = CompositionBuilder(fps=30)
        pm_mock.current_timeline = builder

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        with patch.object(builder, "add_dialogue_frame", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func())
            result_data = json.loads(result)
            assert "error" in result_data

    def test_tool_json_parsing_error(self):
        """Test tool handles JSON parsing errors."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.layouts.DialogueFrame.tool import register_tool
        from chuk_motion.generator.composition_builder import CompositionBuilder

        # Mock ProjectManager with current_timeline
        pm_mock = Mock()
        builder = CompositionBuilder(fps=30)
        pm_mock.current_timeline = builder

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # Test with invalid JSON
        result = asyncio.run(tool_func(left_speaker="invalid json {"))
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid component JSON" in result_data["error"]
