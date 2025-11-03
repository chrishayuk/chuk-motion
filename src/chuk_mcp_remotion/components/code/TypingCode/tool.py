# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/TypingCode/tool.py
"""TypingCode MCP tool."""

import asyncio

from chuk_mcp_remotion.models import CodeComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the TypingCode tool with the MCP server."""

    @mcp.tool
    async def remotion_add_typing_code(
        code: str,
        start_time: float,
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

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_typing_code(
                    code=code,
                    language=language,
                    title=title,
                    variant=variant,
                    cursor_style=cursor_style,
                    typing_speed=typing_speed,
                    show_line_numbers=show_line_numbers,
                    start_time=start_time,
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
