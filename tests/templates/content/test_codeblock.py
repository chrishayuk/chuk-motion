"""
Tests for CodeBlock template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestCodeBlockBasic:
    """Basic CodeBlock generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic CodeBlock generation with all props."""
        tsx = component_builder.build_component(
            "CodeBlock",
            {
                "code": 'console.log("Hello World");',
                "language": "javascript",
                "title": "Example Code",
                "variant": "editor",
                "animation": "fade_in",
            },
            theme_name,
        )

        assert tsx is not None
        assert "CodeBlock" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "CodeBlock")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test CodeBlock with only required props."""
        tsx = component_builder.build_component("CodeBlock", {"code": 'print("test")'}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "language = 'javascript'" in tsx or "language = " in tsx
        assert "variant = 'editor'" in tsx or "variant = " in tsx
        assert "animation = 'fade_in'" in tsx or "animation = " in tsx


class TestCodeBlockVariants:
    """Tests for CodeBlock style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "terminal", "editor", "glass"])
    def test_variant(self, component_builder, theme_name, variant):
        """Test each variant generates correctly."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variants" in tsx
        assert "variantStyle" in tsx

    def test_glass_variant_backdrop(self, component_builder, theme_name):
        """Test glass variant has backdrop filter."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "variant": "glass"}, theme_name
        )

        assert "backdropFilter" in tsx or "blur" in tsx

    def test_editor_variant_title_bar(self, component_builder, theme_name):
        """Test editor variant has title bar with dots."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "variant": "editor", "title": "app.js"}, theme_name
        )

        # Should have macOS-style window controls
        assert "#FF5F56" in tsx  # Red dot
        assert "#FFBD2E" in tsx  # Yellow dot
        assert "#27C93F" in tsx  # Green dot


class TestCodeBlockAnimations:
    """Tests for CodeBlock animations."""

    @pytest.mark.parametrize("animation", ["fade_in", "slide_up", "scale_in", "blur_in"])
    def test_animation(self, component_builder, theme_name, animation):
        """Test each animation variant generates correctly."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "animation": animation}, theme_name
        )

        assert tsx is not None
        assert animation in tsx or "animation" in tsx
        assert "spring" in tsx or "interpolate" in tsx

    def test_fade_in_animation(self, component_builder, theme_name):
        """Test fade_in animation specifics."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "animation": "fade_in"}, theme_name
        )

        assert "opacity" in tsx
        assert "spring" in tsx

    def test_slide_up_animation(self, component_builder, theme_name):
        """Test slide_up animation specifics."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "test", "animation": "slide_up"}, theme_name
        )

        assert "translateY" in tsx
        assert "interpolate" in tsx

    def test_exit_animation(self, component_builder, theme_name):
        """Test CodeBlock has exit fade out."""
        tsx = component_builder.build_component("CodeBlock", {"code": "test"}, theme_name)

        assert "exitProgress" in tsx
        assert "finalOpacity" in tsx


class TestCodeBlockSyntaxHighlighting:
    """Tests for syntax highlighting features."""

    def test_prism_import(self, component_builder, theme_name):
        """Test prism-react-renderer is imported."""
        tsx = component_builder.build_component("CodeBlock", {"code": "test"}, theme_name)

        assert "from 'prism-react-renderer'" in tsx
        assert "Highlight" in tsx
        assert "themes" in tsx

    def test_language_support(self, component_builder, theme_name):
        """Test language prop is used."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "def foo():\n    pass", "language": "python"}, theme_name
        )

        assert "language" in tsx

    def test_line_numbers(self, component_builder, theme_name):
        """Test line numbers are rendered."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "line1\nline2\nline3", "show_line_numbers": True}, theme_name
        )

        assert "show_line_numbers" in tsx
        assert "tokens.map" in tsx

    def test_highlight_lines(self, component_builder, theme_name):
        """Test specific lines can be highlighted."""
        tsx = component_builder.build_component(
            "CodeBlock", {"code": "line1\nline2\nline3", "highlight_lines": [2]}, theme_name
        )

        assert "highlight_lines" in tsx
        assert "isHighlighted" in tsx
        assert "backgroundColor" in tsx


class TestCodeBlockContent:
    """Tests for CodeBlock content rendering."""

    def test_code_prop_required(self, component_builder, theme_name):
        """Test code prop is required."""
        tsx = component_builder.build_component("CodeBlock", {"code": "const x = 42;"}, theme_name)

        assert "code" in tsx

    def test_title_optional(self, component_builder, theme_name):
        """Test title is optional."""
        tsx = component_builder.build_component("CodeBlock", {"code": "test"}, theme_name)

        assert "title" in tsx
        assert "title &&" in tsx  # Conditional rendering

    def test_monospace_font(self, component_builder, theme_name):
        """Test CodeBlock uses monospace font."""
        tsx = component_builder.build_component("CodeBlock", {"code": "test"}, theme_name)

        assert "Fira Code" in tsx or "Monaco" in tsx or "Consolas" in tsx or "monospace" in tsx
