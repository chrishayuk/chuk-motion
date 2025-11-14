"""VideoContent composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    src: str,
    volume: float = 1.0,
    playback_rate: float = 1.0,
    fit: str = "cover",
    muted: bool = False,
    start_from: int = 0,
    loop: bool = False,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add VideoContent to the composition.

    Args:
        builder: CompositionBuilder instance
        start_time: When to show the video (seconds)
        src: Video source URL or path to static file (e.g. 'video.mp4')
        volume: Video volume (0.0 to 1.0)
        playback_rate: Video playback speed multiplier (0.5 = half speed, 2.0 = double speed)
        fit: How video fits in container ("contain", "cover", or "fill")
        muted: Whether video should be muted
        start_from: Frame offset to start video from
        loop: Whether to loop the video continuously
        duration: Total duration (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    props = {
        "src": src,
        "volume": volume,
        "playbackRate": playback_rate,
        "fit": fit,
        "muted": muted,
        "startFrom": start_from,
        "loop": loop,
        "start_time": start_time,
        "duration": duration,
    }

    component = ComponentInstance(
        component_type="VideoContent",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props=props,
        layer=0,
    )
    builder.components.append(component)
    return builder
