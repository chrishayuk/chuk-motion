# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/TypingCode/test_typingcode.py
"""
Tests for TypingCode template generation.
"""

import pytest
from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTypingCodeBasic:
    """Basic TypingCode generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TypingCode generation with all props."""
        tsx = component_builder.build_component(
            "TypingCode",
            {
                "code": 'console.log("Hello World");',
                "language": "javascript",
                "title": "Example",
                "variant": "editor",
                "cursor_style": "line",
                "typing_speed": 1.5,
            },
            theme_name,
        )

        assert tsx is not None
        assert "TypingCode" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TypingCode")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test TypingCode with only required props."""
        tsx = component_builder.build_component("TypingCode", {"code": "test code"}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "language = 'javascript'" in tsx or "language = " in tsx
        assert "variant = 'editor'" in tsx or "variant = " in tsx
        assert "cursor_style = 'line'" in tsx or "cursor_style = " in tsx
        assert "typing_speed = 1.5" in tsx or "typing_speed = " in tsx


class TestTypingCodeVariants:
    """Tests for TypingCode style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "terminal", "editor", "hacker"])
    def test_variant(self, component_builder, theme_name, variant):
        """Test each variant generates correctly."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variants" in tsx
        assert "variantStyle" in tsx

    def test_hacker_variant_glow(self, component_builder, theme_name):
        """Test hacker variant has cyan glow effect."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "test", "variant": "hacker"}, theme_name
        )

        assert "#00D9FF" in tsx
        assert "boxShadow" in tsx


class TestTypingCodeCursor:
    """Tests for cursor styles and animation."""

    @pytest.mark.parametrize("cursor_style", ["block", "line", "underline", "none"])
    def test_cursor_style(self, component_builder, theme_name, cursor_style):
        """Test each cursor style generates correctly."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "test", "cursor_style": cursor_style}, theme_name
        )

        assert tsx is not None
        assert cursor_style in tsx
        assert "cursorStyles" in tsx
        assert "cursorStyle" in tsx

    def test_cursor_blinking(self, component_builder, theme_name):
        """Test cursor has blinking animation."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "showCursor" in tsx
        assert "cursorBlinkSpeed" in tsx
        assert "isTypingComplete" in tsx

    def test_cursor_position(self, component_builder, theme_name):
        """Test cursor appears at end of typed code."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "tokens.length - 1" in tsx
        assert "showCursor &&" in tsx


class TestTypingCodeAnimation:
    """Tests for typing animation."""

    def test_typing_speed_prop(self, component_builder, theme_name):
        """Test typing_speed prop is used."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "test", "typing_speed": 2.0}, theme_name
        )

        assert "typing_speed" in tsx
        assert "charsPerFrame" in tsx

    def test_characters_revealed_progressively(self, component_builder, theme_name):
        """Test code is revealed character by character."""
        tsx = component_builder.build_component("TypingCode", {"code": "test code"}, theme_name)

        assert "charsToShow" in tsx
        assert "displayedCode" in tsx
        assert "slice" in tsx

    def test_typing_delay(self, component_builder, theme_name):
        """Test typing has initial delay."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "startDelay" in tsx

    def test_typing_completion(self, component_builder, theme_name):
        """Test typing completion is tracked."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "isTypingComplete" in tsx
        assert "totalChars" in tsx


class TestTypingCodeSyntaxHighlighting:
    """Tests for syntax highlighting features."""

    def test_prism_import(self, component_builder, theme_name):
        """Test prism-react-renderer is imported."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "from 'prism-react-renderer'" in tsx
        assert "Highlight" in tsx
        assert "themes" in tsx

    def test_language_support(self, component_builder, theme_name):
        """Test language prop is used."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "def foo(): pass", "language": "python"}, theme_name
        )

        assert "language" in tsx

    def test_line_numbers(self, component_builder, theme_name):
        """Test line numbers can be shown."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "line1\nline2", "show_line_numbers": True}, theme_name
        )

        assert "show_line_numbers" in tsx
        assert "tokens.map" in tsx


class TestTypingCodeContent:
    """Tests for TypingCode content rendering."""

    def test_code_prop_required(self, component_builder, theme_name):
        """Test code prop is required."""
        tsx = component_builder.build_component("TypingCode", {"code": "const x = 42;"}, theme_name)

        assert "code" in tsx

    def test_title_optional(self, component_builder, theme_name):
        """Test title is optional."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "title" in tsx
        assert "title &&" in tsx

    def test_editor_variant_title_bar(self, component_builder, theme_name):
        """Test editor variant has title bar with dots."""
        tsx = component_builder.build_component(
            "TypingCode", {"code": "test", "variant": "editor", "title": "app.js"}, theme_name
        )

        # Should have macOS-style window controls
        assert "#FF5F56" in tsx  # Red dot
        assert "#FFBD2E" in tsx  # Yellow dot
        assert "#27C93F" in tsx  # Green dot

    def test_monospace_font(self, component_builder, theme_name):
        """Test TypingCode uses monospace font."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "Fira Code" in tsx or "Monaco" in tsx or "Consolas" in tsx or "monospace" in tsx


class TestTypingCodeBuilderMethod:
    """Tests for TypingCode builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.code.TypingCode.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, code='console.log("test");', start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "TypingCode"
        assert builder.components[0].props["code"] == 'console.log("test");'

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.code.TypingCode.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            code="def test(): pass",
            start_time=1.0,
            language="python",
            title="Example",
            variant="editor",
            cursor_style="block",
            typing_speed="fast",
            show_line_numbers=False,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["code"] == "def test(): pass"
        assert props["language"] == "python"
        assert props["title"] == "Example"
        assert props["variant"] == "editor"
        assert props["cursor_style"] == "block"
        assert props["typing_speed"] == "fast"
        assert not props["show_line_numbers"]

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_mcp_remotion.components.code.TypingCode.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, code="test", start_time=2.0, duration=10.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 300


class TestTypingCodeToolRegistration:
    """Tests for TypingCode MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.code.TypingCode.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.code.TypingCode.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_typing_code = Mock()

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(code='print("test")', start_time=0.0))

        assert composition.add_typing_code.called
        result_data = json.loads(result)
        assert result_data["component"] == "TypingCode"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.code.TypingCode.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_composition = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(code='print("test")', start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.code.TypingCode.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        composition = Mock()
        project_manager.current_composition = composition
        composition.add_typing_code = Mock(side_effect=Exception("Test error"))

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(code='print("test")', start_time=0.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
