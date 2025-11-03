# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Container/tool.py
"""Container MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Container tool with the MCP server."""

    @mcp.tool
    async def remotion_add_container(
        start_time: float,
        position: str | None = None,
        width: str | None = None,
        height: str | None = None,
        padding: float = 40,
        content: str | None = None,
        duration: float = 5.0,
    ) -> str:
        """
        Add Container to the composition.

        Flexible positioning container for components

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_container(
                    position=position,
                    width=width,
                    height=height,
                    padding=padding,
                    content=content,
                    start_time=start_time,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="Container",
                    layout=position or "center",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
