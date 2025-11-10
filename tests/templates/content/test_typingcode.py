"""
Tests for TypingCode template generation.
"""

import pytest

from ..conftest import (
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
        assert "charCount" in tsx
        assert "visibleText" in tsx
        assert "visibility" in tsx  # Characters use visibility to hide/show

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
        assert "#FF3D00" in tsx  # Red dot
        assert "#FFB300" in tsx  # Yellow dot
        assert "#00C853" in tsx  # Green dot

    def test_monospace_font(self, component_builder, theme_name):
        """Test TypingCode uses monospace font."""
        tsx = component_builder.build_component("TypingCode", {"code": "test"}, theme_name)

        assert "Fira Code" in tsx or "Monaco" in tsx or "Consolas" in tsx or "monospace" in tsx
