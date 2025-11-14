# chuk-motion/src/chuk_motion/components/code/CodeBlock/test_codeblock.py
"""
Tests for CodeBlock template generation.
"""

import pytest
from tests.components.conftest import (
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
        assert "#FF3D00" in tsx  # Red dot
        assert "#FFB300" in tsx  # Yellow dot
        assert "#00C853" in tsx  # Green dot


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


class TestCodeBlockBuilderMethod:
    """Tests for CodeBlock builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.code.CodeBlock.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, code='console.log("test");', start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "CodeBlock"
        assert builder.components[0].props["code"] == 'console.log("test");'

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.code.CodeBlock.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            code="def test(): pass",
            start_time=1.0,
            language="python",
            title="Example",
            variant="editor",
            animation="slide_up",
            show_line_numbers=False,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["code"] == "def test(): pass"
        assert props["language"] == "python"
        assert props["title"] == "Example"
        assert props["variant"] == "editor"
        assert props["animation"] == "slide_up"
        assert not props["show_line_numbers"]

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.code.CodeBlock.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, code="test", start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestCodeBlockToolRegistration:
    """Tests for CodeBlock MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeBlock.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeBlock.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(code="test", duration=5.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "CodeBlock"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.code.CodeBlock.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(code="test", duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.code.CodeBlock.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(code="test", duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
