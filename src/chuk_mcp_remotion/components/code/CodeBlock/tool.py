# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/CodeBlock/tool.py
"""CodeBlock MCP tool."""

import asyncio

from chuk_mcp_remotion.models import CodeComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the CodeBlock tool with the MCP server."""

    @mcp.tool
    async def remotion_add_code_block(
        code: str,
        start_time: float,
        language: str | None = None,
        title: str | None = None,
        variant: str | None = None,
        animation: str | None = None,
        show_line_numbers: bool = True,
        duration: float = 5.0,
    ) -> str:
        """
        Add CodeBlock to the composition.

        Syntax-highlighted code display with animated entrance

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_code_block(
                    code=code,
                    language=language,
                    title=title,
                    variant=variant,
                    animation=animation,
                    show_line_numbers=show_line_numbers,
                    start_time=start_time,
                    duration=duration,
                )

                lines = len(code.split("\n"))
                return CodeComponentResponse(
                    component="CodeBlock",
                    language=language or "text",
                    lines=lines,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
