"""
Timeline and Track system for managing video composition with multi-track support.

This module implements a track-based timeline system similar to professional video
editors, where components can be placed on different tracks that stack sequentially
or layer on top of each other.
"""

from dataclasses import dataclass, field
from typing import Any, cast

from .composition_builder import ComponentInstance


@dataclass
class Track:
    """Represents a track in the timeline."""

    name: str
    layer: int
    default_gap: float  # seconds
    cursor: int = 0  # current position in frames
    components: list[ComponentInstance] = field(default_factory=list)


class Timeline:
    """
    Timeline with multi-track support for video composition.

    Tracks allow organizing components in independent timelines that can:
    - Auto-stack sequentially (main track)
    - Layer on top (overlay tracks)
    - Run in parallel (background tracks)

    Each track has:
    - layer: Z-index for rendering order (higher = on top)
    - cursor: Current frame position (for auto-stacking)
    - default_gap: Gap in seconds between auto-stacked components
    """

    # Default track configuration
    DEFAULT_TRACKS = {
        "main": {"layer": 0, "default_gap": 0.5, "description": "Primary content, auto-stacking"},
        "overlay": {
            "layer": 10,
            "default_gap": 0,
            "description": "Text overlays, UI elements",
        },
        "background": {
            "layer": -10,
            "default_gap": 0,
            "description": "Background media",
        },
    }

    def __init__(
        self,
        fps: int = 30,
        width: int = 1920,
        height: int = 1080,
        theme: str = "tech",
        tracks: dict[str, dict[str, Any]] | None = None,
    ):
        """
        Initialize timeline with tracks.

        Args:
            fps: Frames per second
            width: Video width
            height: Video height
            theme: Theme name
            tracks: Track configuration dict, or None to use defaults
        """
        self.fps = fps
        self.width = width
        self.height = height
        self.theme = theme

        # Initialize tracks
        track_config = tracks if tracks is not None else self.DEFAULT_TRACKS
        self.tracks: dict[str, Track] = {}

        for name, config in track_config.items():
            self.tracks[name] = Track(
                name=name,
                layer=cast(int, config["layer"]),
                default_gap=cast(float, config.get("default_gap", 0)),
                cursor=0,
                components=[],
            )

        # Default active track for component additions
        self.active_track = "main"

    @property
    def components(self) -> list[ComponentInstance]:
        """
        Get the main track's components list for CompositionBuilder compatibility.

        This allows builder methods (add_line_chart, etc.) to work with Timeline
        by appending to the main track's components.
        """
        return self.tracks["main"].components

    def add_track(
        self, name: str, layer: int, default_gap: float = 0, description: str = ""
    ) -> None:
        """
        Add a new track to the timeline.

        Args:
            name: Track name (unique identifier)
            layer: Z-index for rendering (higher = on top)
            default_gap: Default gap between components in seconds
            description: Human-readable description
        """
        if name in self.tracks:
            raise ValueError(f"Track '{name}' already exists")

        self.tracks[name] = Track(
            name=name, layer=layer, default_gap=default_gap, cursor=0, components=[]
        )

    def remove_track(self, name: str) -> None:
        """Remove a track from the timeline."""
        if name not in self.tracks:
            raise ValueError(f"Track '{name}' not found")
        del self.tracks[name]

    def get_track(self, name: str) -> Track:
        """Get a track by name."""
        if name not in self.tracks:
            raise ValueError(f"Track '{name}' not found")
        return self.tracks[name]

    def list_tracks(self) -> list[dict[str, Any]]:
        """List all tracks with their properties."""
        return [
            {
                "name": track.name,
                "layer": track.layer,
                "default_gap": track.default_gap,
                "cursor": track.cursor,
                "cursor_seconds": self.frames_to_seconds(track.cursor),
                "component_count": len(track.components),
            }
            for track in sorted(self.tracks.values(), key=lambda t: t.layer, reverse=True)
        ]

    def set_active_track(self, name: str) -> None:
        """Set the default track for component additions."""
        if name not in self.tracks:
            raise ValueError(f"Track '{name}' not found")
        self.active_track = name

    def get_track_cursor(self, track_name: str) -> int:
        """Get the current cursor position for a track (in frames)."""
        track = self.get_track(track_name)
        return track.cursor

    def set_track_cursor(self, track_name: str, frame: int) -> None:
        """Set the cursor position for a track (in frames)."""
        track = self.get_track(track_name)
        track.cursor = frame

    def add_component(
        self,
        component: ComponentInstance,
        duration: float | str,
        track: str | None = None,
        gap_before: float | str | None = None,
        align_to: str | None = None,
        offset: float | str = 0,
        start_frame: int | None = None,
    ) -> ComponentInstance:
        """
        Add a component to a track.

        Args:
            component: Component to add
            duration: Duration in seconds (float) or time string (e.g., "2s", "500ms")
            track: Track name (defaults to active_track)
            gap_before: Gap before component in seconds or time string (overrides track default)
            align_to: Align to another track's cursor instead of this track's
            offset: Offset in seconds or time string from alignment point
            start_frame: Explicit start frame (overrides auto-stacking)

        Returns:
            ComponentInstance with calculated timing
        """
        track_name = track if track is not None else self.active_track
        track_obj = self.get_track(track_name)

        # Calculate gap (handle both string and float inputs)
        gap = gap_before if gap_before is not None else track_obj.default_gap
        gap_frames = self.seconds_to_frames(gap)

        # Calculate start frame
        if start_frame is not None:
            # Explicit positioning
            calculated_start = start_frame
        elif align_to:
            # Align to another track's cursor
            ref_track = self.get_track(align_to)
            calculated_start = ref_track.cursor + self.seconds_to_frames(offset)
        else:
            # Use this track's cursor
            calculated_start = track_obj.cursor + gap_frames

        # Calculate duration (handle both string and float inputs)
        duration_frames = self.seconds_to_frames(duration)

        # Update component with calculated values
        component.start_frame = calculated_start
        component.duration_frames = duration_frames
        component.layer = track_obj.layer

        # Add to track
        track_obj.components.append(component)

        # Advance cursor only if not aligned to another track
        if not align_to:
            track_obj.cursor = calculated_start + duration_frames

        return component

    def get_all_components(self) -> list[ComponentInstance]:
        """
        Get all components from all tracks, sorted by layer.

        Returns:
            List of all components, sorted by layer (lowest first)
        """
        all_components = []
        for track in self.tracks.values():
            all_components.extend(track.components)

        # Sort by layer (lower layers render first)
        return sorted(all_components, key=lambda c: c.layer)

    def get_total_duration_frames(self) -> int:
        """Get total duration of the timeline in frames."""
        all_components = self.get_all_components()
        if not all_components:
            return 0
        return max(c.start_frame + c.duration_frames for c in all_components)

    def get_total_duration_seconds(self) -> float:
        """Get total duration of the timeline in seconds."""
        return self.frames_to_seconds(self.get_total_duration_frames())

    def seconds_to_frames(self, seconds: float | str) -> int:
        """
        Convert seconds to frames.

        Args:
            seconds: Time in seconds (as float) or time string with units (e.g., "1s", "500ms")

        Returns:
            Frame count
        """
        # Handle string inputs with units
        if isinstance(seconds, str):
            seconds_str = seconds.strip().lower()

            # Parse time string with units
            if seconds_str.endswith("ms"):
                # Milliseconds
                value = float(seconds_str[:-2])
                seconds_float = value / 1000.0
            elif seconds_str.endswith("s"):
                # Seconds
                seconds_float = float(seconds_str[:-1])
            elif seconds_str.endswith("m"):
                # Minutes
                value = float(seconds_str[:-1])
                seconds_float = value * 60.0
            else:
                # No unit, assume seconds
                seconds_float = float(seconds_str)
        else:
            seconds_float = float(seconds)

        return int(seconds_float * self.fps)

    def frames_to_seconds(self, frames: int) -> float:
        """Convert frames to seconds."""
        return frames / self.fps

    def _serialize_value(self, value: Any) -> Any:
        """Recursively serialize values to JSON-compatible types."""
        from dataclasses import asdict, is_dataclass

        from pydantic import BaseModel

        if isinstance(value, BaseModel):
            # Recursively serialize Pydantic models using model_dump
            try:
                dumped = value.model_dump(mode="python")
                # Recursively process the dumped dict in case it contains more BaseModels
                return self._serialize_value(dumped)
            except Exception:
                # Fallback: try to convert to dict manually
                return str(value)
        elif is_dataclass(value) and not isinstance(value, type):
            # Handle dataclasses (like ComponentInstance)
            dumped = asdict(value)
            # Recursively process the dumped dict
            return self._serialize_value(dumped)
        elif isinstance(value, dict):
            # Recursively serialize dict values
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # Recursively serialize list items
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, tuple):
            # Convert tuples to lists
            return [self._serialize_value(item) for item in value]
        else:
            # Return primitive types as-is
            return value

    def to_dict(self) -> dict[str, Any]:
        """
        Export timeline as dictionary.

        Returns:
            Dictionary representation of the timeline
        """
        return {
            "fps": self.fps,
            "width": self.width,
            "height": self.height,
            "theme": self.theme,
            "duration_frames": self.get_total_duration_frames(),
            "duration_seconds": self.get_total_duration_seconds(),
            "tracks": [
                {
                    "name": track.name,
                    "layer": track.layer,
                    "default_gap": track.default_gap,
                    "cursor": track.cursor,
                    "component_count": len(track.components),
                }
                for track in sorted(self.tracks.values(), key=lambda t: t.layer, reverse=True)
            ],
            "components": [
                {
                    "type": c.component_type,
                    "start_frame": c.start_frame,
                    "duration_frames": c.duration_frames,
                    "start_time": self.frames_to_seconds(c.start_frame),
                    "duration": self.frames_to_seconds(c.duration_frames),
                    "layer": c.layer,
                    "props": self._serialize_value(c.props),
                }
                for c in self.get_all_components()
            ],
        }

    def generate_composition_tsx(self) -> str:
        """
        Generate the VideoComposition.tsx file from the timeline.

        This delegates to CompositionBuilder's generation logic.
        """
        from .composition_builder import CompositionBuilder

        # Create a temporary CompositionBuilder with our components
        builder = CompositionBuilder(fps=self.fps, width=self.width, height=self.height)
        builder.theme = self.theme
        builder.components = self.get_all_components()

        return builder.generate_composition_tsx()
