# chuk-mcp-remotion/src/chuk_mcp_remotion/components/animations/Counter/tool.py
"""Counter MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import CounterComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the Counter tool with the MCP server."""

    @mcp.tool
    async def remotion_add_counter(
        end_value: float,
        start_value: float = 0,
        prefix: str | None = None,
        suffix: str | None = None,
        decimals: int = 0,
        animation: str | None = None,
        duration: float = 2.0,
        track: str = "main",
        gap_before: float | None = None,
    ) -> str:
        """
        Add Counter to the composition.

        Animated number counter for statistics and metrics

        Args:
            end_value: Ending number
            start_value: Starting number (default: 0)
            prefix: Text before number (e.g., "$")
            suffix: Text after number (e.g., "%")
            decimals: Number of decimal places
            animation: Animation style
            duration: Duration in seconds
            track: Track name (default: "main")
            gap_before: Gap before component in seconds

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="Counter",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "start_value": start_value,
                        "end_value": end_value,
                        "prefix": prefix,
                        "suffix": suffix,
                        "decimals": decimals,
                        "animation": animation,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return CounterComponentResponse(
                    component="Counter",
                    start_value=start_value,
                    end_value=end_value,
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
