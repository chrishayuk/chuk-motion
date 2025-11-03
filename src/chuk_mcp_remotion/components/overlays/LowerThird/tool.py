# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/LowerThird/tool.py
"""LowerThird MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the LowerThird tool with the MCP server."""

    @mcp.tool
    async def remotion_add_lower_third(
        name: str,
        start_time: float,
        title: str | None = None,
        variant: str | None = None,
        position: str | None = None,
        duration: float = 5.0,
    ) -> str:
        """
        Add LowerThird to the composition.

        Name plate overlay with title and subtitle (like TV graphics)

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_lower_third(
                    name=name,
                    title=title,
                    variant=variant,
                    position=position,
                    start_time=start_time,
                    duration=duration,
                )

                return OverlayComponentResponse(
                    component="LowerThird", start_time=start_time, duration=duration
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
