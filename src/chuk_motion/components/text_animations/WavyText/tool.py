# chuk-motion/src/chuk_motion/components/text-animations/WavyText/tool.py
"""WavyText MCP tool."""

import asyncio

from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the WavyText tool with the MCP server."""

    @mcp.tool
    async def remotion_add_wavy_text(
        text: str,
        font_size: str = "4xl",
        font_weight: str = "bold",
        text_color: str | None = None,
        wave_amplitude: float = 20.0,
        wave_speed: float = 1.0,
        wave_frequency: float = 0.3,
        position: str = "center",
        align: str = "center",
        duration: float = 3.0,
    ) -> str:
        """
        Add WavyText continuous wave motion animation.

        Creates a fun wave effect where each character oscillates vertically with
        a phase offset, creating a continuous wave motion.

        Perfect for: Fun titles, music videos, creative content, playful effects

        Args:
            text: Text to animate with wave
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 4xl
            font_weight: Font weight (normal, medium, semibold, bold, extrabold, black) - default: bold
            text_color: Text color (uses on_dark color if not specified)
            wave_amplitude: Height of wave oscillation in pixels (default: 20.0)
            wave_speed: Speed of wave motion (default: 1.0)
            wave_frequency: Frequency of wave (spacing between peaks) (default: 0.3)
            position: Vertical position (center, top, bottom) - default: center
            align: Text alignment (left, center, right) - default: center
            duration: Total duration in seconds (default: 3.0)

        Returns:
            JSON with component info

        Example:
            # Basic wave
            remotion_add_wavy_text(
                text="MUSIC",
                wave_amplitude=25.0,
                wave_speed=1.5
            )

            # Subtle wave
            remotion_add_wavy_text(
                text="Creative Content",
                wave_amplitude=10.0,
                wave_frequency=0.5,
                wave_speed=0.8
            )

            # Intense wave
            remotion_add_wavy_text(
                text="PARTY",
                font_size="4xl",
                wave_amplitude=40.0,
                wave_speed=2.0,
                wave_frequency=0.2
            )
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_wavy_text(
                    text=text,
                    font_size=font_size,
                    font_weight=font_weight,
                    text_color=text_color,
                    wave_amplitude=wave_amplitude,
                    wave_speed=wave_speed,
                    wave_frequency=wave_frequency,
                    position=position,
                    align=align,
                    start_time=start_time,
                    duration=duration,
                )

                return ComponentResponse(
                    component="WavyText",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
