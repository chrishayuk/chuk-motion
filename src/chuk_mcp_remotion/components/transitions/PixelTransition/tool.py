# chuk-mcp-remotion/src/chuk_mcp_remotion/components/transitions/PixelTransition/tool.py
"""PixelTransition MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.components.component_helpers import parse_nested_component
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the PixelTransition tool with the MCP server."""

    @mcp.tool
    async def remotion_add_pixel_transition(
        first_content: str,
        second_content: str,
        grid_size: int = 10,
        pixel_color: str | None = None,
        transition_start: float = 2.0,
        transition_duration: float = 1.0,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add PixelTransition animated transition effect to the composition.

        Creates a pixelated dissolve transition between two pieces of content. Pixels
        animate in with random stagger to cover the first content, then animate out
        to reveal the second content.

        Perfect for: Scene transitions, content reveals, before/after showcases

        Args:
            first_content: JSON string of first content component (format: {"type": "ComponentName", "config": {...}})
            second_content: JSON string of second content component (format: {"type": "ComponentName", "config": {...}})
            grid_size: Number of pixels per row/column (default: 10 = 10x10 = 100 pixels)
            pixel_color: Color of transition pixels (uses primary color if not specified)
            transition_start: When to start transition in seconds (default: 2.0)
            transition_duration: Duration of transition animation in seconds (default: 1.0)
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Transition between two title cards
            remotion_add_pixel_transition(
                first_content='{"type":"TitleScene","config":{"text":"Before","variant":"bold"}}',
                second_content='{"type":"TitleScene","config":{"text":"After","variant":"glass"}}',
                grid_size=12,
                transition_start=2.0,
                transition_duration=1.0,
                duration=5.0
            )

            # Transition between chart and text
            remotion_add_pixel_transition(
                first_content='{"type":"BarChart","config":{"data":[...],"title":"Sales Data"}}',
                second_content='{"type":"TextOverlay","config":{"text":"Record Growth","size":"large"}}',
                grid_size=15,
                pixel_color="#00D9FF"
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse nested content
                first_parsed = json.loads(first_content)
                second_parsed = json.loads(second_content)

                first_component = parse_nested_component(first_parsed)
                second_component = parse_nested_component(second_parsed)

                if first_component is None or second_component is None:
                    return ErrorResponse(
                        error="Invalid content format. Use format: {'type': 'ComponentName', 'config': {...}}"
                    ).model_dump_json()

                # Build props
                props = {
                    "firstContent": first_component,
                    "secondContent": second_component,
                    "gridSize": grid_size,
                    "transitionStart": int(transition_start * 30),  # Convert to frames
                    "transitionDuration": int(transition_duration * 30),  # Convert to frames
                }

                if pixel_color:
                    props["pixelColor"] = pixel_color

                component = ComponentInstance(
                    component_type="PixelTransition",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="PixelTransition",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
