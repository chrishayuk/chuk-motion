# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Grid/tool.py
"""Grid MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Grid tool with the MCP server."""

    @mcp.tool
    async def remotion_add_grid(
        items: str,
        start_time: float,
        layout: str | None = None,
        gap: float = 20,
        padding: float = 40,
        duration: float = 5.0,
    ) -> str:
        """
        Add Grid to the composition.

        Grid layout for multiple items

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                items_parsed = json.loads(items)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid items JSON: {str(e)}").model_dump_json()

            try:
                project_manager.current_composition.add_grid(
                    layout=layout,
                    gap=gap,
                    padding=padding,
                    items=items_parsed,
                    start_time=start_time,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="Grid",
                    layout=layout or "2x2",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
