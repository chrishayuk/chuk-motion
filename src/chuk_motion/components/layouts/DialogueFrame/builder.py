# chuk-motion/src/chuk_motion/components/layouts/DialogueFrame/builder.py
"""DialogueFrame composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    left_speaker: Any | None = None,
    right_speaker: Any | None = None,
    center_content: Any | None = None,
    speaker_size: float = 40,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add DialogueFrame to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="DialogueFrame",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "left_speaker": left_speaker,
            "right_speaker": right_speaker,
            "center_content": center_content,
            "speaker_size": speaker_size,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
