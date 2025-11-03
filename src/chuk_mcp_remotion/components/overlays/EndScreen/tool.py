# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/EndScreen/tool.py
"""EndScreen MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the EndScreen tool with the MCP server."""

    @mcp.tool
    async def remotion_add_end_screen(
        cta_text: str,
        thumbnail_url: str | None = None,
        variant: str | None = None,
        duration_seconds: float = 10.0,
    ) -> str:
        """
        Add EndScreen to the composition.

        YouTube end screen with CTAs and video suggestions

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_end_screen(
                    cta_text=cta_text,
                    thumbnail_url=thumbnail_url,
                    variant=variant,
                    duration_seconds=duration_seconds,
                )

                # Get the actual start time from the last added component
                last_component = project_manager.current_composition.components[-1]
                actual_start_time = last_component.start_frame / project_manager.current_composition.fps

                return OverlayComponentResponse(
                    component="EndScreen",
                    start_time=actual_start_time,
                    duration=duration_seconds,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
