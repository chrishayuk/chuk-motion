# chuk-motion/src/chuk_motion/components/text_animations/DecryptedText/tool.py
"""DecryptedText MCP tool."""

import asyncio

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
        duration: float = 3.0,
    ) -> str:
        """
        Add DecryptedText animated text reveal with character scrambling effect.

        Creates an animation where characters progressively decrypt from random
        characters to the final text, with configurable reveal direction.

        Args:
            text: Text to animate (characters will scramble then reveal)
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 3xl
            font_weight: Font weight (normal, medium, semibold, bold) - default: bold
            text_color: Text color (uses theme color if not specified)
            reveal_direction: Direction of reveal (start, end, center) - default: start
            scramble_speed: Speed of character scrambling (higher = faster) - default: 3.0
            position: Vertical position (center, top, bottom) - default: center
            duration: Total duration in seconds - default: 3.0

        Returns:
            JSON with component info

        Example:
            remotion_add_decrypted_text(
                text="Access Granted",
                font_size="4xl",
                reveal_direction="start"
            )
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_decrypted_text(
                    start_time=start_time,
                    text=text,
                    font_size=font_size,
                    font_weight=font_weight,
                    text_color=text_color,
                    reveal_direction=reveal_direction,
                    scramble_speed=scramble_speed,
                    position=position,
                    duration=duration,
                )

                return ComponentResponse(
                    component="DecryptedText",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
