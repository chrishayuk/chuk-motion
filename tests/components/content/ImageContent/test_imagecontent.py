"""Tests for ImageContent template generation."""

import pytest
from pydantic import ValidationError
from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestImageContentBasic:
    """Basic ImageContent generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic ImageContent generation."""
        tsx = component_builder.build_component("ImageContent", {"src": "image.png"}, theme_name)
        assert tsx is not None
        assert "ImageContent" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "ImageContent")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test ImageContent with minimal props."""
        tsx = component_builder.build_component("ImageContent", {"src": "test.png"}, theme_name)
        assert "test.png" in tsx or "src" in tsx


class TestImageContentRendering:
    """Tests for ImageContent rendering features."""

    def test_img_tag(self, component_builder, theme_name):
        """Test ImageContent generates img element."""
        tsx = component_builder.build_component("ImageContent", {"src": "image.png"}, theme_name)
        assert "Img" in tsx or "img" in tsx

    def test_fit_modes(self, component_builder, theme_name):
        """Test different fit modes are supported."""
        for fit_mode in ["contain", "cover", "fill"]:
            tsx = component_builder.build_component(
                "ImageContent", {"src": "image.png", "fit": fit_mode}, theme_name
            )
            assert tsx is not None
            assert_valid_typescript(tsx)

    def test_opacity_prop(self, component_builder, theme_name):
        """Test opacity property."""
        tsx = component_builder.build_component(
            "ImageContent", {"src": "image.png", "opacity": 0.5}, theme_name
        )
        assert tsx is not None
        assert_valid_typescript(tsx)

    def test_border_radius_prop(self, component_builder, theme_name):
        """Test border radius property."""
        tsx = component_builder.build_component(
            "ImageContent", {"src": "image.png", "borderRadius": 10}, theme_name
        )
        assert tsx is not None
        assert_valid_typescript(tsx)


class TestImageContentBuilderMethod:
    """Tests for ImageContent builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.content.ImageContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, src="image.png")

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "ImageContent"
        assert builder.components[0].props["src"] == "image.png"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.content.ImageContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            src="test.png",
            fit="contain",
            opacity=0.8,
            border_radius=15,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["src"] == "test.png"
        assert props["fit"] == "contain"
        assert props["opacity"] == 0.8
        assert props["borderRadius"] == 15

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.content.ImageContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, src="image.png", duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150

    def test_add_to_composition_default_values(self):
        """Test default values are applied correctly."""
        from chuk_motion.components.content.ImageContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(builder, start_time=0.0, src="image.png")

        props = builder.components[0].props
        assert props["fit"] == "cover"
        assert props["opacity"] == 1.0
        assert props["borderRadius"] == 0


class TestImageContentConfig:
    """Tests for ImageContentConfig Pydantic model."""

    def test_config_basic(self):
        """Test basic ImageContentConfig instantiation."""
        from chuk_motion.components.content.ImageContent.tool import ImageContentConfig

        config = ImageContentConfig(src="image.png")

        assert config.src == "image.png"
        assert config.fit == "cover"
        assert config.opacity == 1.0
        assert config.border_radius == 0

    def test_config_all_fields(self):
        """Test ImageContentConfig with all fields."""
        from chuk_motion.components.content.ImageContent.tool import ImageContentConfig

        config = ImageContentConfig(
            src="test.png",
            fit="contain",
            opacity=0.7,
            border_radius=20,
        )

        assert config.src == "test.png"
        assert config.fit == "contain"
        assert config.opacity == 0.7
        assert config.border_radius == 20

    def test_config_opacity_validation(self):
        """Test opacity validation (0.0 to 1.0)."""
        from chuk_motion.components.content.ImageContent.tool import ImageContentConfig

        # Valid opacities
        ImageContentConfig(src="image.png", opacity=0.0)
        ImageContentConfig(src="image.png", opacity=0.5)
        ImageContentConfig(src="image.png", opacity=1.0)

        # Invalid opacity - too high
        with pytest.raises(ValidationError):
            ImageContentConfig(src="image.png", opacity=1.5)

        # Invalid opacity - negative
        with pytest.raises(ValidationError):
            ImageContentConfig(src="image.png", opacity=-0.1)

    def test_config_border_radius_validation(self):
        """Test border_radius validation (must be >= 0)."""
        from chuk_motion.components.content.ImageContent.tool import ImageContentConfig

        # Valid border radii
        ImageContentConfig(src="image.png", border_radius=0)
        ImageContentConfig(src="image.png", border_radius=10)
        ImageContentConfig(src="image.png", border_radius=50)

        # Invalid border radius - negative
        with pytest.raises(ValidationError):
            ImageContentConfig(src="image.png", border_radius=-5)


class TestImageContentToolDefinition:
    """Tests for ImageContent TOOL_DEFINITION."""

    def test_tool_definition_exists(self):
        """Test TOOL_DEFINITION is accessible."""
        from chuk_motion.components.content.ImageContent.tool import TOOL_DEFINITION

        assert TOOL_DEFINITION is not None
        assert isinstance(TOOL_DEFINITION, dict)

    def test_tool_definition_structure(self):
        """Test TOOL_DEFINITION has correct structure."""
        from chuk_motion.components.content.ImageContent.tool import TOOL_DEFINITION

        assert "name" in TOOL_DEFINITION
        assert TOOL_DEFINITION["name"] == "create_image_content"

        assert "description" in TOOL_DEFINITION
        assert "inputSchema" in TOOL_DEFINITION

    def test_tool_definition_input_schema(self):
        """Test TOOL_DEFINITION inputSchema structure."""
        from chuk_motion.components.content.ImageContent.tool import TOOL_DEFINITION

        schema = TOOL_DEFINITION["inputSchema"]
        assert "type" in schema
        assert schema["type"] == "object"

        assert "properties" in schema
        props = schema["properties"]

        assert "component_type" in props
        assert "props" in props
        assert "start_frame" in props
        assert "duration_frames" in props
        assert "layer" in props

    def test_tool_definition_props_schema(self):
        """Test TOOL_DEFINITION props schema."""
        from chuk_motion.components.content.ImageContent.tool import TOOL_DEFINITION

        props_schema = TOOL_DEFINITION["inputSchema"]["properties"]["props"]
        assert "properties" in props_schema

        props = props_schema["properties"]
        assert "src" in props
        assert "fit" in props
        assert "opacity" in props
        assert "border_radius" in props

        # Check required fields
        assert "required" in props_schema
        assert "src" in props_schema["required"]
