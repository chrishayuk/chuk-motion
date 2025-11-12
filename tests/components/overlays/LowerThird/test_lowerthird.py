# chuk-motion/src/chuk_motion/components/overlays/LowerThird/test_lowerthird.py
"""
Tests for LowerThird template generation.
"""

import pytest
from tests.components.conftest import (
    assert_design_tokens_injected,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestLowerThirdBasic:
    """Basic LowerThird generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LowerThird generation with all props."""
        tsx = component_builder.build_component(
            "LowerThird",
            {
                "name": "Speaker Name",
                "title": "Job Title",
                "variant": "glass",
                "position": "bottom_left",
            },
            theme_name,
        )

        assert tsx is not None
        assert "LowerThird" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "LowerThird")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test LowerThird with only required props."""
        tsx = component_builder.build_component("LowerThird", {"name": "Speaker"}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert "variant = 'glass'" in tsx or "variant = " in tsx
        assert "position = 'bottom_left'" in tsx or "position = " in tsx


class TestLowerThirdPositions:
    """Tests for LowerThird position variants."""

    @pytest.mark.parametrize(
        "position",
        ["bottom_left", "bottom_center", "bottom_right", "top_left", "top_center", "top_right"],
    )
    def test_position_variant(self, component_builder, theme_name, position):
        """Test each position variant generates correctly."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "position": position}, theme_name
        )

        assert tsx is not None
        assert position in tsx
        assert "positionStyle" in tsx

    def test_position_mapping(self, component_builder, theme_name):
        """Test that positions map to correct CSS properties."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "position": "bottom_left"}, theme_name
        )

        # Should have interpolate for slide animation
        assert "interpolate" in tsx
        assert "bottom" in tsx
        assert "left" in tsx


class TestLowerThirdVariants:
    """Tests for LowerThird style variants."""

    @pytest.mark.parametrize("variant", ["minimal", "standard", "glass", "bold", "animated"])
    def test_style_variant(self, component_builder, theme_name, variant):
        """Test each style variant generates correctly."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "variant": variant}, theme_name
        )

        assert tsx is not None
        assert variant in tsx
        assert "variantStyle" in tsx

    def test_glass_variant_backdrop(self, component_builder, theme_name):
        """Test glass variant has backdrop filter."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test", "variant": "glass"}, theme_name
        )

        assert "backdropFilter" in tsx or "blur" in tsx


class TestLowerThirdAnimation:
    """Tests for LowerThird slide animation."""

    def test_has_slide_animation(self, component_builder, theme_name):
        """Test LowerThird has slide-in animation."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "slideIn" in tsx
        assert "spring" in tsx
        assert "interpolate" in tsx

    def test_uses_motion_tokens(self, component_builder, theme_name):
        """Test animation uses motion tokens from theme."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        # Should use motion config
        assert "damping" in tsx
        assert "stiffness" in tsx
        assert "50.0" in tsx or "120.0" in tsx  # Actual spring config values

    def test_has_fade_in_out(self, component_builder, theme_name):
        """Test LowerThird has fade in and fade out."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "opacity" in tsx
        assert "fadeOut" in tsx
        assert "finalOpacity" in tsx


class TestLowerThirdContent:
    """Tests for LowerThird content rendering."""

    def test_name_only(self, component_builder, theme_name):
        """Test LowerThird with name only (no title)."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test Name"}, theme_name)

        assert "{name}" in tsx
        assert "title &&" in tsx  # Conditional rendering

    def test_name_and_title(self, component_builder, theme_name):
        """Test LowerThird with both name and title."""
        tsx = component_builder.build_component(
            "LowerThird", {"name": "Test Name", "title": "Test Title"}, theme_name
        )

        assert "{name}" in tsx
        assert "{title}" in tsx


class TestLowerThirdDesignTokens:
    """Tests for design token integration."""

    def test_design_tokens_injected(self, component_builder, theme_name):
        """Test that design tokens are properly injected."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert_design_tokens_injected(tsx)

    def test_font_family_from_theme(self, component_builder, theme_name):
        """Test font family comes from theme."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        assert "fontFamily" in tsx
        assert "Inter" in tsx or "SF Pro" in tsx


class TestLowerThirdBuilderMethod:
    """Tests for LowerThird builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.overlays.LowerThird.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, name="John Doe", start_time=0.0)

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "LowerThird"
        assert builder.components[0].props["name"] == "John Doe"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.overlays.LowerThird.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            name="John Doe",
            start_time=1.0,
            title="CEO",
            variant="modern",
            position="bottom-left",
            duration=5.0,
        )

        props = builder.components[0].props
        assert props["name"] == "John Doe"
        assert props["title"] == "CEO"
        assert props["variant"] == "modern"
        assert props["position"] == "bottom-left"

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.overlays.LowerThird.builder import add_to_composition
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, name="Test", start_time=2.0, duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150


class TestLowerThirdToolRegistration:
    """Tests for LowerThird MCP tool."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.overlays.LowerThird.tool import register_tool

        mcp = Mock()
        project_manager = Mock()

        register_tool(mcp, project_manager)

        assert mcp.tool.called or hasattr(mcp, "tool")

    def test_tool_execution(self):
        """Test tool execution creates component."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.LowerThird.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(name="Test", duration=5.0))

        # Check component was added
        assert len(timeline.get_all_components()) >= 1
        result_data = json.loads(result)
        assert result_data["component"] == "LowerThird"

    def test_tool_execution_no_project(self):
        """Test tool execution when no project exists."""
        import asyncio
        import json
        from unittest.mock import Mock

        from chuk_motion.components.overlays.LowerThird.tool import register_tool

        mcp = Mock()
        project_manager = Mock()
        project_manager.current_timeline = None  # No project

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        result = asyncio.run(tool_func(name="Test", duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No active project" in result_data["error"]

    def test_tool_execution_error_handling(self):
        """Test tool execution handles exceptions."""
        import asyncio
        import json
        from unittest.mock import Mock, patch

        from chuk_motion.components.overlays.LowerThird.tool import register_tool
        from chuk_motion.generator.timeline import Timeline

        mcp = Mock()
        project_manager = Mock()
        timeline = Timeline(fps=30)
        project_manager.current_timeline = timeline

        register_tool(mcp, project_manager)
        tool_func = mcp.tool.call_args[0][0]

        # Mock add_component to raise exception
        with patch.object(timeline, "add_component", side_effect=Exception("Test error")):
            result = asyncio.run(tool_func(name="Test", duration=5.0))

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Test error" in result_data["error"]
