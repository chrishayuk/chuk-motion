# chuk-motion/src/chuk_motion/components/text-animations/TypewriterText/tool.py
"""TypewriterText MCP tool."""

import asyncio

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
        duration: float = 3.0,
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
            duration: Total duration in seconds (default: 3.0)

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
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_typewriter_text(
                    text=text,
                    font_size=font_size,
                    font_weight=font_weight,
                    text_color=text_color,
                    cursor_color=cursor_color,
                    show_cursor=show_cursor,
                    type_speed=type_speed,
                    position=position,
                    align=align,
                    start_time=start_time,
                    duration=duration,
                )

                return ComponentResponse(
                    component="TypewriterText",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
