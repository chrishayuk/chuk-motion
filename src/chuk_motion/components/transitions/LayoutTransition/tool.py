"""LayoutTransition MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the LayoutTransition tool with the MCP server."""

    @mcp.tool
    async def remotion_add_layout_transition(
        first_content: str,
        second_content: str,
        transition_type: str = "crossfade",
        transition_start: float = 2.0,
        transition_duration: float = 1.0,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add LayoutTransition for animated scene-to-scene transitions.

        Creates smooth animated transitions between two layouts or scenes. Supports
        multiple transition styles with motion token integration for consistent timing.

        Perfect for: Scene changes, layout switches, content transitions, slideshows

        Example transition_type values and their effects:
        - crossfade: Smooth opacity blend (professional, subtle)
        - slide_horizontal: Push left, slide in right (sequential content)
        - slide_vertical: Push up, slide in from bottom (mobile-like)
        - cube_rotate: 3D rotation effect (dramatic, attention-grabbing)
        - parallax_push: Depth effect with layers (cinematic, premium)

        Example first_content Grid layout:
        {
            "type": "Grid",
            "config": {
                "layout": "3x3",
                "items": [
                    {"type": "CodeBlock", "config": {"code": "Panel 1"}},
                    {"type": "CodeBlock", "config": {"code": "Panel 2"}}
                ]
            }
        }

        Example second_content Container:
        {
            "type": "Container",
            "config": {
                "position": "center",
                "content": {"type": "TitleScene", "config": {"text": "Next Scene"}}
            }
        }

        Args:
            first_content: JSON component for first scene (format: {"type": "ComponentName", "config": {...}})
            second_content: JSON component for second scene (format: {"type": "ComponentName", "config": {...}})
            transition_type: Transition style - one of: crossfade, slide_horizontal, slide_vertical, cube_rotate, parallax_push (default: "crossfade")
                - "crossfade": Smooth opacity blend
                - "slide_horizontal": Slide left/right
                - "slide_vertical": Slide up/down
                - "cube_rotate": 3D cube rotation effect
                - "parallax_push": Parallax depth effect
            transition_start: When to start transition in seconds (default: 2.0)
            transition_duration: Duration of transition animation in seconds (default: 1.0)
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")

        Returns:
            JSON with component info

        Example:
            # Crossfade between two layouts
            remotion_add_layout_transition(
                first_content='{"type":"Grid","config":{"items":[...]}}',
                second_content='{"type":"Container","config":{"content":{...}}}',
                transition_type="crossfade",
                transition_start=2.0,
                transition_duration=1.0,
                duration=5.0
            )

            # Slide transition between scenes
            remotion_add_layout_transition(
                first_content='{"type":"TitleScene","config":{"text":"Chapter 1"}}',
                second_content='{"type":"TitleScene","config":{"text":"Chapter 2"}}',
                transition_type="slide_horizontal",
                transition_duration=0.8
            )

            # 3D cube rotation effect
            remotion_add_layout_transition(
                first_content='{"type":"ThreeColumnLayout","config":{...}}',
                second_content='{"type":"SplitScreen","config":{...}}',
                transition_type="cube_rotate",
                transition_duration=1.5
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

                # Validate that we got ComponentInstance objects
                if not isinstance(first_component, ComponentInstance) or not isinstance(
                    second_component, ComponentInstance
                ):
                    return ErrorResponse(
                        error="Invalid content format. Use format: {'type': 'ComponentName', 'config': {...}}"
                    ).model_dump_json()

                # Validate transition type
                valid_types = [
                    "crossfade",
                    "slide_horizontal",
                    "slide_vertical",
                    "cube_rotate",
                    "parallax_push",
                ]
                if transition_type not in valid_types:
                    return ErrorResponse(
                        error=f"Invalid transition_type. Must be one of: {', '.join(valid_types)}"
                    ).model_dump_json()

                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                builder.add_layout_transition(
                    start_time=start_time,
                    first_content=first_component,
                    second_content=second_component,
                    transition_type=transition_type,
                    transition_start=transition_start,
                    transition_duration=transition_duration,
                    duration=duration,
                )

                return ComponentResponse(
                    component="LayoutTransition",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
