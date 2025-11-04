# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TitleScene/test_titlescene.py
"""
Tests for TitleScene template generation.
"""

import pytest
from tests.components.conftest import (
    assert_design_tokens_injected,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestTitleSceneBasic:
    """Basic TitleScene generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TitleScene generation with all props."""
        tsx = component_builder.build_component(
            "TitleScene",
            {
                "title": "Test Title",
                "subtitle": "Test Subtitle",
                "variant": "bold",
                "animation": "fade_zoom",
            },
            theme_name,
        )

        assert tsx is not None
        assert "TitleScene" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TitleScene")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test TitleScene with only required props."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Minimal Title"}, theme_name
        )

        assert tsx is not None
        assert "TitleScene" in tsx
        # Should have default values
        assert "variant = 'bold'" in tsx or "variant = " in tsx
        assert "animation = " in tsx


class TestTitleSceneAnimations:
    """Tests for TitleScene animation variants."""

    @pytest.mark.parametrize(
        "animation", ["fade_zoom", "slide_up", "typewriter", "blur_in", "fade_slide", "zoom"]
    )
    def test_animation_variant(self, component_builder, theme_name, animation):
        """Test each animation variant generates correctly."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": animation}, theme_name
        )

        assert tsx is not None
        assert animation in tsx or "animation" in tsx
        assert "spring" in tsx or "interpolate" in tsx

    def test_fade_zoom_animation(self, component_builder, theme_name):
        """Test fade_zoom animation specifics."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": "fade_zoom"}, theme_name
        )

        assert "spring" in tsx
        assert "scale" in tsx
        assert "opacity" in tsx

    def test_typewriter_animation(self, component_builder, theme_name):
        """Test typewriter animation specifics."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test Title", "animation": "typewriter"}, theme_name
        )

        assert "charsToShow" in tsx
        assert "slice" in tsx


class TestTitleSceneVariants:
    """Tests for TitleScene style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "standard", "bold", "kinetic", "glass"])
    def test_style_variant(self, component_builder, theme_name, variant):
        """Test each style variant generates correctly."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variantStyle" in tsx

    def test_bold_variant_sizing(self, component_builder, theme_name):
        """Test bold variant has larger font size."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "variant": "bold"}, theme_name
        )

        assert "120" in tsx  # Bold uses 120px font size


class TestTitleSceneDesignTokens:
    """Tests for design token integration."""

    def test_color_tokens_injected(self, component_builder, theme_name):
        """Test that color tokens from theme are injected."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        assert_design_tokens_injected(tsx)
        # Should have actual color values, not template vars
        assert "#" in tsx

    def test_typography_tokens_injected(self, component_builder, theme_name):
        """Test that typography tokens are injected."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        # Should have font family from theme
        assert "Inter" in tsx or "SF Pro" in tsx
        assert "fontFamily" in tsx

    def test_motion_tokens_injected(self, component_builder, theme_name):
        """Test that motion tokens are injected."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test", "animation": "fade_zoom"}, theme_name
        )

        # Should have motion config values
        assert "damping" in tsx
        assert "stiffness" in tsx
        assert "200" in tsx  # Default damping value


class TestTitleSceneFadeOut:
    """Tests for fade-out animation."""

    def test_has_fade_out(self, component_builder, theme_name):
        """Test that TitleScene has fade-out at end."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        assert "fadeOut" in tsx
        assert "durationInFrames - 20" in tsx
        assert "finalOpacity" in tsx


class TestTitleSceneThemes:
    """Tests for all theme compatibility."""

    def test_all_themes(self, component_builder, all_themes):
        """Test generation works with all available themes."""
        for theme_name in all_themes:
            tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

            assert tsx is not None
            assert_valid_typescript(tsx)
            assert "[[" not in tsx  # No unresolved vars


class TestTitleSceneBuilderMethod:
    """Tests for TitleScene builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_mcp_remotion.components.overlays.TitleScene.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, text="Title Text")

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "TitleScene"
        assert builder.components[0].props["text"] == "Title Text"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_mcp_remotion.components.overlays.TitleScene.builder import add_to_composition
        from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            text="Title Text",
            subtitle="Subtitle",
            variant="modern",
            animation="fade_zoom",
            duration_seconds=5.0,
        )

        props = builder.components[0].props
        assert props["text"] == "Title Text"
        assert props["subtitle"] == "Subtitle"
        assert props["variant"] == "modern"
        assert props["animation"] == "fade_zoom"
        assert props["duration_seconds"] == 5.0


class TestTitleSceneToolRegistration:
    """Tests for TitleScene MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TitleScene.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TitleScene.tool import register_tool
        from chuk_mcp_remotion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Title Text", duration_seconds=3.0))

        # Check component was added to timeline
        assert len(timeline.get_all_components()) == 1
        assert timeline.get_all_components()[0].component_type == "TitleScene"

        result_data = json.loads(result)
        assert result_data["component"] == "TitleScene"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_mcp_remotion.components.overlays.TitleScene.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(text="Title Text", duration_seconds=3.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_mcp_remotion.components.overlays.TitleScene.tool import register_tool
        from chuk_mcp_remotion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(text="Title Text", duration_seconds=3.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
