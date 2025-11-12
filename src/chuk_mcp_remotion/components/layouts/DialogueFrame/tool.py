# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/DialogueFrame/tool.py
"""DialogueFrame MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.components.component_helpers import parse_nested_component
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the DialogueFrame tool with the MCP server."""

    @mcp.tool
    async def remotion_add_dialogue_frame(
        left_speaker: str | None = None,
        right_speaker: str | None = None,
        center_content: str | None = None,
        speaker_size: float = 40,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add DialogueFrame layout to the composition.

        For conversation/dialogue scenes with two speakers

        Args:
            left_speaker: JSON component for left speaker. Format: {"type": "ComponentName", "config": {...}}
                Example:
                {
                    "type": "VideoContent",
                    "config": {
                        "src": "speaker1.mp4",
                        "fit": "cover"
                    }
                }
            right_speaker: JSON component for right speaker. Same format as left_speaker
            center_content: JSON component for center content (captions, etc.). Same format
            speaker_size: Speaker panel size (percentage)
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
                left_parsed = json.loads(left_speaker) if left_speaker else None
                right_parsed = json.loads(right_speaker) if right_speaker else None
                center_parsed = json.loads(center_content) if center_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                left_component = parse_nested_component(left_parsed)
                right_component = parse_nested_component(right_parsed)
                center_component = parse_nested_component(center_parsed)

                component = ComponentInstance(
                    component_type="DialogueFrame",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "left_speaker": left_component,
                        "right_speaker": right_component,
                        "center_content": center_component,
                        "speaker_size": speaker_size,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="DialogueFrame",
                    layout="dialogue",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
