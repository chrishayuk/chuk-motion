# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TitleScene/tool.py
"""TitleScene MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the TitleScene tool with the MCP server."""

    @mcp.tool
    async def remotion_add_title_scene(
        text: str,
        subtitle: str | None = None,
        variant: str | None = None,
        animation: str | None = None,
        duration_seconds: float = 3.0,
    ) -> str:
        """
        Add TitleScene to the composition.

        Full-screen animated title card for video openings

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_title_scene(
                    text=text,
                    subtitle=subtitle,
                    variant=variant,
                    animation=animation,
                    duration_seconds=duration_seconds,
                )

                return OverlayComponentResponse(
                    component="TitleScene", start_time=0.0, duration=duration_seconds
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
