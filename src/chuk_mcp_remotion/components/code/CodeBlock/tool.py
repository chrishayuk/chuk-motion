# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/CodeBlock/tool.py
"""CodeBlock MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import CodeComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the CodeBlock tool with the MCP server."""

    @mcp.tool
    async def remotion_add_code_block(
        code: str,
        language: str | None = None,
        title: str | None = None,
        variant: str | None = None,
        animation: str | None = None,
        show_line_numbers: bool = True,
        duration: float = 5.0,
        track: str = "main",
        gap_before: float | None = None,
    ) -> str:
        """
        Add CodeBlock to the composition.

        Syntax-highlighted code display with animated entrance

        Args:
            code: Code content to display
            language: Programming language for syntax highlighting
            title: Optional title/filename
            variant: Style variant (minimal, terminal, editor, glass)
            animation: Entrance animation
            show_line_numbers: Show line numbers
            duration: Duration in seconds
            track: Track name (default: "main")
            gap_before: Gap before component in seconds (overrides track default)

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="CodeBlock",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "code": code,
                        "language": language,
                        "title": title,
                        "variant": variant,
                        "animation": animation,
                        "show_line_numbers": show_line_numbers,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                lines = len(code.split("\n"))
                return CodeComponentResponse(
                    component="CodeBlock",
                    language=language or "text",
                    lines=lines,
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
