# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/AreaChart/tool.py
"""AreaChart MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the AreaChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_area_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        duration: float | str = 4.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add an animated bar chart to the composition.

        Animated vertical bar chart for comparing categories.

        Args:
            data: JSON array of data points
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            duration: How long to animate (seconds)
            track: Track name (default: "main")
            gap_before: Gap before component in seconds

        Returns:
            JSON with component info

        Example:
            await remotion_add_area_chart(
                data='[{"label": "Q1", "value": 45}, {"label": "Q2", "value": 67}]',
                title="Example Chart",
                duration=4.0
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="AreaChart",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "data": data_parsed,
                        "title": title,
                        "xlabel": xlabel,
                        "ylabel": ylabel,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ChartComponentResponse(
                    component="AreaChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
