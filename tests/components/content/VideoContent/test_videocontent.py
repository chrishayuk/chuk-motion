"""Tests for VideoContent template generation."""

import pytest
from pydantic import ValidationError
from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestVideoContentBasic:
    """Basic VideoContent generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic VideoContent generation."""
        tsx = component_builder.build_component("VideoContent", {"src": "video.mp4"}, theme_name)
        assert tsx is not None
        assert "VideoContent" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "VideoContent")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test VideoContent with minimal props."""
        tsx = component_builder.build_component("VideoContent", {"src": "test.mp4"}, theme_name)
        assert "test.mp4" in tsx or "src" in tsx


class TestVideoContentRendering:
    """Tests for VideoContent rendering features."""

    def test_video_tag(self, component_builder, theme_name):
        """Test VideoContent generates video element."""
        tsx = component_builder.build_component("VideoContent", {"src": "video.mp4"}, theme_name)
        assert "Video" in tsx or "video" in tsx or "OffthreadVideo" in tsx

    def test_fit_modes(self, component_builder, theme_name):
        """Test different fit modes are supported."""
        for fit_mode in ["contain", "cover", "fill"]:
            tsx = component_builder.build_component(
                "VideoContent", {"src": "video.mp4", "fit": fit_mode}, theme_name
            )
            assert tsx is not None
            assert_valid_typescript(tsx)

    def test_muted_prop(self, component_builder, theme_name):
        """Test muted property."""
        tsx = component_builder.build_component(
            "VideoContent", {"src": "video.mp4", "muted": True}, theme_name
        )
        assert tsx is not None
        assert_valid_typescript(tsx)

    def test_loop_prop(self, component_builder, theme_name):
        """Test loop property."""
        tsx = component_builder.build_component(
            "VideoContent", {"src": "video.mp4", "loop": True}, theme_name
        )
        assert tsx is not None
        assert_valid_typescript(tsx)


class TestVideoContentBuilderMethod:
    """Tests for VideoContent builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.content.VideoContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(builder, start_time=0.0, src="video.mp4")

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "VideoContent"
        assert builder.components[0].props["src"] == "video.mp4"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.content.VideoContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            src="test.mp4",
            volume=0.8,
            playback_rate=1.5,
            fit="contain",
            muted=True,
            start_from=30,
            loop=True,
            duration=10.0,
        )

        props = builder.components[0].props
        assert props["src"] == "test.mp4"
        assert props["volume"] == 0.8
        assert props["playbackRate"] == 1.5
        assert props["fit"] == "contain"
        assert props["muted"] is True
        assert props["startFrom"] == 30
        assert props["loop"] is True

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.content.VideoContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(builder, start_time=2.0, src="video.mp4", duration=5.0)

        component = builder.components[0]
        assert component.start_frame == 60
        assert component.duration_frames == 150

    def test_add_to_composition_default_values(self):
        """Test default values are applied correctly."""
        from chuk_motion.components.content.VideoContent.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(builder, start_time=0.0, src="video.mp4")

        props = builder.components[0].props
        assert props["volume"] == 1.0
        assert props["playbackRate"] == 1.0
        assert props["fit"] == "cover"
        assert props["muted"] is False
        assert props["startFrom"] == 0
        assert props["loop"] is False


class TestVideoContentConfig:
    """Tests for VideoContentConfig Pydantic model."""

    def test_config_basic(self):
        """Test basic VideoContentConfig instantiation."""
        from chuk_motion.components.content.VideoContent.tool import VideoContentConfig

        config = VideoContentConfig(src="video.mp4")

        assert config.src == "video.mp4"
        assert config.volume == 1.0
        assert config.playback_rate == 1.0
        assert config.fit == "cover"
        assert config.muted is False
        assert config.start_from == 0
        assert config.loop is False

    def test_config_all_fields(self):
        """Test VideoContentConfig with all fields."""
        from chuk_motion.components.content.VideoContent.tool import VideoContentConfig

        config = VideoContentConfig(
            src="test.mp4",
            volume=0.8,
            playback_rate=1.5,
            fit="contain",
            muted=True,
            start_from=30,
            loop=True,
        )

        assert config.src == "test.mp4"
        assert config.volume == 0.8
        assert config.playback_rate == 1.5
        assert config.fit == "contain"
        assert config.muted is True
        assert config.start_from == 30
        assert config.loop is True

    def test_config_volume_validation(self):
        """Test volume validation (0.0 to 1.0)."""
        from chuk_motion.components.content.VideoContent.tool import VideoContentConfig

        # Valid volumes
        VideoContentConfig(src="video.mp4", volume=0.0)
        VideoContentConfig(src="video.mp4", volume=0.5)
        VideoContentConfig(src="video.mp4", volume=1.0)

        # Invalid volume - too high
        with pytest.raises(ValidationError):
            VideoContentConfig(src="video.mp4", volume=1.5)

        # Invalid volume - negative
        with pytest.raises(ValidationError):
            VideoContentConfig(src="video.mp4", volume=-0.1)

    def test_config_playback_rate_validation(self):
        """Test playback_rate validation (must be > 0)."""
        from chuk_motion.components.content.VideoContent.tool import VideoContentConfig

        # Valid playback rates
        VideoContentConfig(src="video.mp4", playback_rate=0.5)
        VideoContentConfig(src="video.mp4", playback_rate=1.0)
        VideoContentConfig(src="video.mp4", playback_rate=2.0)

        # Invalid playback rate - zero
        with pytest.raises(ValidationError):
            VideoContentConfig(src="video.mp4", playback_rate=0.0)

        # Invalid playback rate - negative
        with pytest.raises(ValidationError):
            VideoContentConfig(src="video.mp4", playback_rate=-1.0)


class TestVideoContentToolDefinition:
    """Tests for VideoContent TOOL_DEFINITION."""

    def test_tool_definition_exists(self):
        """Test TOOL_DEFINITION is accessible."""
        from chuk_motion.components.content.VideoContent.tool import TOOL_DEFINITION

        assert TOOL_DEFINITION is not None
        assert isinstance(TOOL_DEFINITION, dict)

    def test_tool_definition_structure(self):
        """Test TOOL_DEFINITION has correct structure."""
        from chuk_motion.components.content.VideoContent.tool import TOOL_DEFINITION

        assert "name" in TOOL_DEFINITION
        assert TOOL_DEFINITION["name"] == "create_video_content"

        assert "description" in TOOL_DEFINITION
        assert "inputSchema" in TOOL_DEFINITION

    def test_tool_definition_input_schema(self):
        """Test TOOL_DEFINITION inputSchema structure."""
        from chuk_motion.components.content.VideoContent.tool import TOOL_DEFINITION

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
        from chuk_motion.components.content.VideoContent.tool import TOOL_DEFINITION

        props_schema = TOOL_DEFINITION["inputSchema"]["properties"]["props"]
        assert "properties" in props_schema

        props = props_schema["properties"]
        assert "src" in props
        assert "volume" in props
        assert "playback_rate" in props
        assert "fit" in props
        assert "muted" in props
        assert "start_from" in props
        assert "loop" in props

        # Check required fields
        assert "required" in props_schema
        assert "src" in props_schema["required"]
