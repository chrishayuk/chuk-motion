# chuk-motion/src/chuk_motion/components/charts/DonutChart/tool.py
"""DonutChart MCP tool."""

import asyncio
import json

from chuk_motion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the DonutChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_donut_chart(
        data: str,
        title: str | None = None,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated donut chart to the composition.

        Animated donut chart for showing proportions with a center hole.

        Args:
            data: JSON array of {label, value} objects. Optionally include "color" per slice.
                Format: [{"label": "Free", "value": 55}, {"label": "Pro", "value": 30}]
            title: Optional chart title
            duration: How long to animate in seconds (default: 4.0)

        Returns:
            JSON with component info

        Example:
            await remotion_add_donut_chart(
                data='[{"label": "Free", "value": 55}, {"label": "Pro", "value": 30}, {"label": "Enterprise", "value": 15}]',
                title="Plan Distribution",
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
                builder.add_donut_chart(
                    data=data_parsed,
                    title=title,
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
