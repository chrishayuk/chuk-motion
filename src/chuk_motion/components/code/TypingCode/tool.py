# chuk-motion/src/chuk_motion/components/code/TypingCode/tool.py
"""TypingCode MCP tool."""

import asyncio

from chuk_motion.models import CodeComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the TypingCode tool with the MCP server."""

    @mcp.tool
    async def remotion_add_typing_code(
        code: str,
        language: str | None = None,
        title: str | None = None,
        variant: str | None = None,
        cursor_style: str | None = None,
        typing_speed: str | None = None,
        show_line_numbers: bool = True,
        duration: float = 10.0,
    ) -> str:
        """
        Add TypingCode to the composition.

        Animated typing code effect with cursor

        Args:
            code: Code content to display with typing animation
            language: Programming language for syntax highlighting
            title: Optional title/filename
            variant: Style variant (minimal, terminal, editor, glass)
            cursor_style: Cursor appearance style
            typing_speed: Speed of typing animation
            show_line_numbers: Show line numbers (default: True)
            duration: Duration in seconds (default: 10.0)

        Returns:
            JSON with component info
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_typing_code(
                    code=code,
                    start_time=start_time,
                    language=language,
                    title=title,
                    variant=variant,
                    cursor_style=cursor_style,
                    typing_speed=typing_speed,
                    show_line_numbers=show_line_numbers,
                    duration=duration,
                )

                lines = len(code.split("\n"))
                return CodeComponentResponse(
                    component="TypingCode",
                    language=language or "text",
                    lines=lines,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
