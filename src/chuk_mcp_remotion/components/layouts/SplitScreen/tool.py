# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/SplitScreen/tool.py
"""SplitScreen MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the SplitScreen tool with the MCP server."""

    @mcp.tool
    async def remotion_add_split_screen(
        start_time: float,
        orientation: str | None = None,
        layout: str | None = None,
        gap: float = 20,
        left_content: str | None = None,
        right_content: str | None = None,
        duration: float = 5.0,
    ) -> str:
        """
        Add SplitScreen to the composition.

        Layout component for side-by-side content

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_split_screen(
                    orientation=orientation,
                    layout=layout,
                    gap=gap,
                    left_content=left_content,
                    right_content=right_content,
                    start_time=start_time,
                    duration=duration,
                )

                layout_desc = f"{orientation or 'horizontal'}-{layout or '50-50'}"
                return LayoutComponentResponse(
                    component="SplitScreen",
                    layout=layout_desc,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
