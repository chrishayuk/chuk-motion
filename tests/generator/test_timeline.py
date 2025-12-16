"""Tests for Timeline and Track system."""

import pytest

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.generator.timeline import Timeline, Track


class TestTrackDataclass:
    """Test Track dataclass."""

    def test_track_creation(self):
        """Test creating a Track."""
        track = Track(name="main", layer=0, default_gap=0.5)

        assert track.name == "main"
        assert track.layer == 0
        assert track.default_gap == 0.5
        assert track.cursor == 0
        assert track.components == []

    def test_track_with_components(self):
        """Test Track with components."""
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello"},
        )
        track = Track(
            name="main",
            layer=0,
            default_gap=0.5,
            cursor=90,
            components=[comp],
        )

        assert len(track.components) == 1
        assert track.cursor == 90


class TestTimelineInitialization:
    """Test Timeline initialization."""

    def test_default_initialization(self):
        """Test Timeline with default values."""
        timeline = Timeline()

        assert timeline.fps == 30
        assert timeline.width == 1920
        assert timeline.height == 1080
        assert timeline.theme == "tech"
        assert "main" in timeline.tracks
        assert "overlay" in timeline.tracks
        assert "background" in timeline.tracks
        assert timeline.active_track == "main"

    def test_custom_initialization(self):
        """Test Timeline with custom values."""
        timeline = Timeline(fps=60, width=1280, height=720, theme="finance")

        assert timeline.fps == 60
        assert timeline.width == 1280
        assert timeline.height == 720
        assert timeline.theme == "finance"

    def test_custom_tracks(self):
        """Test Timeline with custom track configuration."""
        custom_tracks = {
            "video": {"layer": 0, "default_gap": 0},
            "audio": {"layer": -1, "default_gap": 0},
        }
        timeline = Timeline(tracks=custom_tracks)

        assert "video" in timeline.tracks
        assert "audio" in timeline.tracks
        assert "main" not in timeline.tracks


class TestTimelineTrackManagement:
    """Test Timeline track management."""

    def test_add_track(self):
        """Test adding a new track."""
        timeline = Timeline()
        timeline.add_track("effects", layer=5, default_gap=0.2, description="Effects")

        assert "effects" in timeline.tracks
        assert timeline.tracks["effects"].layer == 5
        assert timeline.tracks["effects"].default_gap == 0.2

    def test_add_duplicate_track_raises_error(self):
        """Test that adding duplicate track raises ValueError."""
        timeline = Timeline()

        with pytest.raises(ValueError, match="already exists"):
            timeline.add_track("main", layer=0)

    def test_remove_track(self):
        """Test removing a track."""
        timeline = Timeline()
        timeline.remove_track("overlay")

        assert "overlay" not in timeline.tracks

    def test_remove_nonexistent_track_raises_error(self):
        """Test that removing nonexistent track raises ValueError."""
        timeline = Timeline()

        with pytest.raises(ValueError, match="not found"):
            timeline.remove_track("nonexistent")

    def test_get_track(self):
        """Test getting a track by name."""
        timeline = Timeline()
        track = timeline.get_track("main")

        assert track.name == "main"
        assert track.layer == 0

    def test_get_nonexistent_track_raises_error(self):
        """Test that getting nonexistent track raises ValueError."""
        timeline = Timeline()

        with pytest.raises(ValueError, match="not found"):
            timeline.get_track("nonexistent")

    def test_list_tracks(self):
        """Test listing all tracks."""
        timeline = Timeline()
        tracks = timeline.list_tracks()

        assert len(tracks) == 3
        # Should be sorted by layer (highest first)
        assert tracks[0]["name"] == "overlay"
        assert tracks[1]["name"] == "main"
        assert tracks[2]["name"] == "background"

    def test_set_active_track(self):
        """Test setting the active track."""
        timeline = Timeline()
        timeline.set_active_track("overlay")

        assert timeline.active_track == "overlay"

    def test_set_nonexistent_active_track_raises_error(self):
        """Test that setting nonexistent active track raises ValueError."""
        timeline = Timeline()

        with pytest.raises(ValueError, match="not found"):
            timeline.set_active_track("nonexistent")


class TestTimelineCursor:
    """Test Timeline cursor operations."""

    def test_get_track_cursor(self):
        """Test getting track cursor."""
        timeline = Timeline()
        cursor = timeline.get_track_cursor("main")

        assert cursor == 0

    def test_set_track_cursor(self):
        """Test setting track cursor."""
        timeline = Timeline()
        timeline.set_track_cursor("main", 150)

        assert timeline.get_track_cursor("main") == 150


class TestTimelineComponentAddition:
    """Test adding components to Timeline."""

    def test_add_component_basic(self):
        """Test adding a basic component."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=0,
            props={"text": "Hello"},
        )

        result = timeline.add_component(comp, duration=3.0)

        assert result.start_frame == 15  # 0 + 0.5s gap = 15 frames
        assert result.duration_frames == 90  # 3.0s * 30fps
        assert result.layer == 0  # main track layer
        assert len(timeline.tracks["main"].components) == 1

    def test_add_component_with_explicit_track(self):
        """Test adding component to specific track."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(
            component_type="TextOverlay",
            start_frame=0,
            duration_frames=0,
            props={"text": "Overlay"},
        )

        result = timeline.add_component(comp, duration=2.0, track="overlay")

        assert result.layer == 10  # overlay track layer
        assert len(timeline.tracks["overlay"].components) == 1
        assert len(timeline.tracks["main"].components) == 0

    def test_add_component_with_explicit_start_frame(self):
        """Test adding component with explicit start frame."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=0,
        )

        result = timeline.add_component(comp, duration=3.0, start_frame=100)

        assert result.start_frame == 100

    def test_add_component_with_gap_before(self):
        """Test adding component with custom gap."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=0,
        )

        result = timeline.add_component(comp, duration=3.0, gap_before=1.0)

        assert result.start_frame == 30  # 1.0s gap = 30 frames

    def test_add_component_with_align_to(self):
        """Test adding component aligned to another track."""
        timeline = Timeline(fps=30)

        # Add component to main track first
        main_comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        timeline.add_component(main_comp, duration=3.0)  # cursor now at 105

        # Add overlay aligned to main track
        overlay_comp = ComponentInstance(
            component_type="TextOverlay", start_frame=0, duration_frames=0
        )
        result = timeline.add_component(
            overlay_comp, duration=2.0, track="overlay", align_to="main", offset=0.5
        )

        # Should align to main cursor (105) + 0.5s offset (15)
        assert result.start_frame == 105 + 15

    def test_add_component_auto_stacking(self):
        """Test that components auto-stack on the same track."""
        timeline = Timeline(fps=30)

        # Add first component
        comp1 = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        result1 = timeline.add_component(comp1, duration=2.0)

        # Add second component
        comp2 = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        result2 = timeline.add_component(comp2, duration=2.0)

        # First: 0 + 15 (gap) = 15, duration 60
        # Second: 15 + 60 + 15 (gap) = 90, duration 60
        assert result1.start_frame == 15
        assert result2.start_frame == 90


class TestTimelineTimeConversion:
    """Test time conversion methods."""

    def test_seconds_to_frames_float(self):
        """Test converting seconds to frames with float."""
        timeline = Timeline(fps=30)

        assert timeline.seconds_to_frames(1.0) == 30
        assert timeline.seconds_to_frames(2.5) == 75
        assert timeline.seconds_to_frames(0.0) == 0

    def test_seconds_to_frames_string_seconds(self):
        """Test converting seconds string to frames."""
        timeline = Timeline(fps=30)

        assert timeline.seconds_to_frames("1s") == 30
        assert timeline.seconds_to_frames("2.5s") == 75

    def test_seconds_to_frames_string_milliseconds(self):
        """Test converting milliseconds string to frames."""
        timeline = Timeline(fps=30)

        assert timeline.seconds_to_frames("500ms") == 15
        assert timeline.seconds_to_frames("1000ms") == 30

    def test_seconds_to_frames_string_minutes(self):
        """Test converting minutes string to frames."""
        timeline = Timeline(fps=30)

        assert timeline.seconds_to_frames("1m") == 1800  # 60s * 30fps
        assert timeline.seconds_to_frames("0.5m") == 900  # 30s * 30fps

    def test_seconds_to_frames_string_no_unit(self):
        """Test converting string without unit (assumes seconds)."""
        timeline = Timeline(fps=30)

        assert timeline.seconds_to_frames("2") == 60
        assert timeline.seconds_to_frames("1.5") == 45

    def test_frames_to_seconds(self):
        """Test converting frames to seconds."""
        timeline = Timeline(fps=30)

        assert timeline.frames_to_seconds(30) == 1.0
        assert timeline.frames_to_seconds(75) == 2.5
        assert timeline.frames_to_seconds(0) == 0.0


class TestTimelineDuration:
    """Test Timeline duration calculations."""

    def test_get_total_duration_empty(self):
        """Test duration of empty timeline."""
        timeline = Timeline()

        assert timeline.get_total_duration_frames() == 0
        assert timeline.get_total_duration_seconds() == 0.0

    def test_get_total_duration_single_component(self):
        """Test duration with single component."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        timeline.add_component(comp, duration=3.0)

        # Start at 15 (0.5s gap) + 90 frames (3s) = 105 frames
        assert timeline.get_total_duration_frames() == 105
        assert timeline.get_total_duration_seconds() == 3.5

    def test_get_total_duration_multiple_tracks(self):
        """Test duration with components on multiple tracks."""
        timeline = Timeline(fps=30)

        # Add to main track: ends at frame 105
        main_comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        timeline.add_component(main_comp, duration=3.0)

        # Add longer component to overlay track
        overlay_comp = ComponentInstance(
            component_type="TextOverlay", start_frame=0, duration_frames=0
        )
        timeline.add_component(overlay_comp, duration=5.0, track="overlay")

        # Overlay: 0 + 0 gap + 150 frames (5s) = 150 frames
        assert timeline.get_total_duration_frames() == 150


class TestTimelineGetAllComponents:
    """Test getting all components."""

    def test_get_all_components_empty(self):
        """Test getting components from empty timeline."""
        timeline = Timeline()

        assert timeline.get_all_components() == []

    def test_get_all_components_multiple_tracks(self):
        """Test getting all components from multiple tracks."""
        timeline = Timeline(fps=30)

        # Add to main track
        main_comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=0)
        timeline.add_component(main_comp, duration=2.0)

        # Add to overlay track
        overlay_comp = ComponentInstance(
            component_type="TextOverlay", start_frame=0, duration_frames=0
        )
        timeline.add_component(overlay_comp, duration=2.0, track="overlay")

        all_comps = timeline.get_all_components()

        assert len(all_comps) == 2
        # Should be sorted by layer (lowest first)
        assert all_comps[0].layer == 0  # main
        assert all_comps[1].layer == 10  # overlay


class TestTimelineComponentsProperty:
    """Test Timeline.components property for CompositionBuilder compatibility."""

    def test_components_property_returns_main_track(self):
        """Test that components property returns main track components."""
        timeline = Timeline(fps=30)

        comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        timeline.tracks["main"].components.append(comp)

        assert timeline.components == [comp]

    def test_components_property_allows_append(self):
        """Test that components property allows appending."""
        timeline = Timeline(fps=30)

        comp = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        timeline.components.append(comp)

        assert len(timeline.tracks["main"].components) == 1


class TestTimelineToDict:
    """Test Timeline serialization."""

    def test_to_dict_empty(self):
        """Test serializing empty timeline."""
        timeline = Timeline(fps=30, width=1920, height=1080, theme="tech")
        result = timeline.to_dict()

        assert result["fps"] == 30
        assert result["width"] == 1920
        assert result["height"] == 1080
        assert result["theme"] == "tech"
        assert result["duration_frames"] == 0
        assert result["duration_seconds"] == 0.0
        assert len(result["tracks"]) == 3
        assert result["components"] == []

    def test_to_dict_with_components(self):
        """Test serializing timeline with components."""
        timeline = Timeline(fps=30)
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=0,
            props={"text": "Hello"},
        )
        timeline.add_component(comp, duration=3.0)

        result = timeline.to_dict()

        assert len(result["components"]) == 1
        assert result["components"][0]["type"] == "TitleScene"
        assert result["components"][0]["props"]["text"] == "Hello"


class TestTimelineSerializeValue:
    """Test Timeline._serialize_value helper."""

    def test_serialize_primitive_types(self):
        """Test serializing primitive types."""
        timeline = Timeline()

        assert timeline._serialize_value(42) == 42
        assert timeline._serialize_value("hello") == "hello"
        assert timeline._serialize_value(True) is True
        assert timeline._serialize_value(3.14) == 3.14

    def test_serialize_dict(self):
        """Test serializing dict."""
        timeline = Timeline()

        result = timeline._serialize_value({"key": "value", "num": 42})
        assert result == {"key": "value", "num": 42}

    def test_serialize_list(self):
        """Test serializing list."""
        timeline = Timeline()

        result = timeline._serialize_value([1, 2, 3])
        assert result == [1, 2, 3]

    def test_serialize_tuple(self):
        """Test serializing tuple to list."""
        timeline = Timeline()

        result = timeline._serialize_value((1, 2, 3))
        assert result == [1, 2, 3]

    def test_serialize_nested_dict(self):
        """Test serializing nested dict."""
        timeline = Timeline()

        result = timeline._serialize_value({"outer": {"inner": "value"}})
        assert result == {"outer": {"inner": "value"}}


class TestTimelineGenerateCompositionTsx:
    """Test Timeline TSX generation."""

    def test_generate_composition_tsx_empty(self):
        """Test generating TSX for empty timeline."""
        timeline = Timeline(fps=30, theme="tech")
        tsx = timeline.generate_composition_tsx()

        assert "import React from 'react'" in tsx
        assert "VideoComposition" in tsx
        assert "AbsoluteFill" in tsx

    def test_generate_composition_tsx_with_components(self):
        """Test generating TSX with components."""
        timeline = Timeline(fps=30, theme="tech")
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello"},
        )
        timeline.tracks["main"].components.append(comp)

        tsx = timeline.generate_composition_tsx()

        assert "import { TitleScene }" in tsx
        assert "TitleScene" in tsx
