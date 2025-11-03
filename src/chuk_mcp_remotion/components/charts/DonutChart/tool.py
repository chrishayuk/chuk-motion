# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/DonutChart/tool.py
"""DonutChart MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the DonutChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_donut_chart(
        data: str,
        title: str | None = None,
        center_text: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated donut chart to the composition.

        Animated donut chart with center text for showing proportions.

        Args:
            data: JSON array of data points
            title: Optional chart title
            center_text: Text to display in center
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            JSON with component info

        Example:
            await remotion_add_donut_chart(
                data='[{"label": "Complete", "value": 75}, {"label": "In Progress", "value": 15}]',
                title="Example Chart",
                start_time=3.0,
                duration=4.0
            )
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                project_manager.current_composition.add_donut_chart(
                    data=data_parsed,
                    title=title,
                    center_text=center_text,
                    start_time=start_time,
                    duration=duration,
                )

                return ChartComponentResponse(
                    component="DonutChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
