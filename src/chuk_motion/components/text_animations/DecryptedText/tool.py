# chuk-motion/src/chuk_motion/components/overlays/DecryptedText/tool.py
"""DecryptedText MCP tool."""

import asyncio

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the DecryptedText tool with the MCP server."""

    @mcp.tool
    async def remotion_add_decrypted_text(
        text: str,
        font_size: str = "3xl",
        font_weight: str = "bold",
        text_color: str | None = None,
        reveal_direction: str = "start",
        scramble_speed: float = 3.0,
        position: str = "center",
        duration: float | str = 3.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add DecryptedText animated text reveal with character scrambling effect.

        Creates an animation where characters progressively decrypt from random
        characters to the final text, with configurable reveal direction.

        Perfect for: Dramatic text reveals, code/hacker aesthetics, mystery unveilings

        Args:
            text: Text to animate (characters will scramble then reveal)
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 3xl
            font_weight: Font weight (normal, medium, semibold, bold, extrabold, black) - default: bold
            text_color: Text color (uses on_dark color if not specified)
            reveal_direction: Direction of reveal (start, end, center) - default: start
            scramble_speed: Speed of character scrambling (higher = faster) - default: 3.0
            position: Vertical position (center, top, bottom) - default: center
            duration: Total duration in seconds or time string (e.g., "3s", "300ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Basic decrypted text reveal
            remotion_add_decrypted_text(
                text="Access Granted",
                font_size="4xl",
                reveal_direction="start"
            )

            # Center-out reveal with custom styling
            remotion_add_decrypted_text(
                text="System Initialized",
                reveal_direction="center",
                font_weight="extrabold",
                scramble_speed=5.0,
                duration=4.0
            )

            # End-to-start reveal
            remotion_add_decrypted_text(
                text="Decoding Complete",
                reveal_direction="end",
                position="top",
                text_color="#00FF00"
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse duration if it's a string
                actual_duration = duration
                if isinstance(duration, str):
                    if duration.endswith('s'):
                        actual_duration = float(duration[:-1])
                    else:
                        actual_duration = float(duration)

                # Calculate if we need to speed up decryption to fit in the given duration
                text_length = len(text)
                # Reserve 0.5 second for final display
                fps = 30
                frames_available = max(int(actual_duration * fps) - int(0.5 * fps), fps)

                # Calculate frames needed per character at current speed
                frames_per_char = scramble_speed
                total_frames_needed = text_length * frames_per_char

                # If we need more frames than available, speed up
                if total_frames_needed > frames_available:
                    final_scramble_speed = max(1, frames_available / text_length)
                else:
                    final_scramble_speed = scramble_speed

                # Build props with adjusted scramble_speed
                props = {
                    "text": text,
                    "fontSize": font_size,
                    "fontWeight": font_weight,
                    "revealDirection": reveal_direction,
                    "scrambleSpeed": final_scramble_speed,
                    "position": position,
                }

                if text_color:
                    props["textColor"] = text_color

                component = ComponentInstance(
                    component_type="DecryptedText",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=actual_duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="DecryptedText",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=actual_duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
