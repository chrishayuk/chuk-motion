# chuk-motion/src/chuk_motion/components/text-animations/TypewriterText/tool.py
"""TypewriterText MCP tool."""

import asyncio

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the TypewriterText tool with the MCP server."""

    @mcp.tool
    async def remotion_add_typewriter_text(
        text: str,
        font_size: str = "4xl",
        font_weight: str = "medium",
        text_color: str | None = None,
        cursor_color: str | None = None,
        show_cursor: bool = True,
        type_speed: float = 2.0,
        position: str = "center",
        align: str = "left",
        duration: float | str = 3.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add TypewriterText classic typing animation with cursor.

        Creates a typewriter effect where characters appear one-by-one as if being
        typed, with an optional blinking cursor.

        Perfect for: Code demos, dialogue, captions, storytelling

        Args:
            text: Text to type out (supports multiline)
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 4xl
            font_weight: Font weight (normal, medium, semibold, bold) - default: medium
            text_color: Text color (uses on_dark color if not specified)
            cursor_color: Cursor color (uses text color if not specified)
            show_cursor: Whether to show blinking cursor - default: true
            type_speed: Characters per second (default: 2.0)
            position: Screen position (center, top, bottom, left) - default: center
            align: Text alignment (left, center, right) - default: left
            duration: Total duration in seconds or time string (e.g., "3s", "300ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Basic typewriter
            remotion_add_typewriter_text(
                text="Hello, World!",
                type_speed=3.0
            )

            # Code typing effect
            remotion_add_typewriter_text(
                text="const greeting = 'Hello';\\nconsole.log(greeting);",
                font_size="2xl",
                type_speed=4.0,
                position="left",
                align="left"
            )

            # Dialogue effect
            remotion_add_typewriter_text(
                text="Once upon a time...",
                font_weight="normal",
                type_speed=2.5,
                show_cursor=False
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse duration if it's a string
                actual_duration = duration
                if isinstance(duration, str):
                    # Simple parsing for "Xs" format
                    if duration.endswith('s'):
                        actual_duration = float(duration[:-1])
                    else:
                        actual_duration = float(duration)

                # Calculate if we need to speed up typing to fit in the given duration
                text_length = len(text)
                # Reserve 1.0 second for cursor to blink at the end
                time_available_for_typing = max(actual_duration - 1.0, 0.5)

                # Calculate minimum speed needed to finish in time
                min_speed_needed = text_length / time_available_for_typing

                # Use the faster of: requested speed or minimum needed speed
                final_type_speed = max(type_speed, min_speed_needed)

                # Use the requested duration (don't extend it)
                final_duration = actual_duration

                # Build props - use calculated type_speed to ensure completion
                props = {
                    "text": text,
                    "fontSize": font_size,
                    "fontWeight": font_weight,
                    "showCursor": show_cursor,
                    "typeSpeed": final_type_speed,
                    "position": position,
                    "align": align,
                }

                if text_color:
                    props["textColor"] = text_color
                if cursor_color:
                    props["cursorColor"] = cursor_color

                component = ComponentInstance(
                    component_type="TypewriterText",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=final_duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="TypewriterText",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=final_duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
