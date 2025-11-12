# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/StackedReaction/tool.py
"""StackedReaction MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.components.component_helpers import parse_nested_component
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the StackedReaction tool with the MCP server."""

    @mcp.tool
    async def remotion_add_stacked_reaction(
        original_content: str | None = None,
        reaction_content: str | None = None,
        layout: str = "vertical",
        reaction_size: float = 40,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add StackedReaction layout to the composition.

        Reaction video style with stacked feeds

        Args:
            original_content: JSON component for original video. Format: {"type": "ComponentName", "config": {...}}
            reaction_content: JSON component for reaction video. Same format as original_content
            layout: Layout style (vertical, horizontal, pip)
            reaction_size: Reaction panel size (percentage)
            gap: Gap between panels
            padding: Padding from edges
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
                original_parsed = json.loads(original_content) if original_content else None
                reaction_parsed = json.loads(reaction_content) if reaction_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                original_component = parse_nested_component(original_parsed)
                reaction_component = parse_nested_component(reaction_parsed)

                component = ComponentInstance(
                    component_type="StackedReaction",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "original_content": original_component,
                        "reaction_content": reaction_component,
                        "layout": layout,
                        "reaction_size": reaction_size,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="StackedReaction",
                    layout=layout,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
