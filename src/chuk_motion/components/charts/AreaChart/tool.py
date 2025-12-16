# chuk-motion/src/chuk_motion/components/charts/AreaChart/tool.py
"""AreaChart MCP tool."""

import asyncio
import json

from chuk_motion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the AreaChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_area_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated area chart to the composition.

        Animated area chart for showing volume and trends over time.

        Args:
            data: JSON array of [x, y] pairs or {x, y, label} objects.
                Format: [[0, 10], [1, 25], [2, 45]] or
                        [{"x": 0, "y": 10, "label": "Week 1"}, {"x": 1, "y": 25, "label": "Week 2"}]
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            duration: How long to animate in seconds (default: 4.0)

        Returns:
            JSON with component info

        Example:
            await remotion_add_area_chart(
                data='[[0, 15], [1, 30], [2, 45], [3, 60]]',
                title="Engagement Growth",
                duration=4.0
            )
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_area_chart(
                    data=data_parsed,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    start_time=start_time,
                    duration=duration,
                )

                return ChartComponentResponse(
                    component="AreaChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
