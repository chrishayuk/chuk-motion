"""PanelCascade MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the PanelCascade tool with the MCP server."""

    @mcp.tool
    async def remotion_add_panel_cascade(
        items: str,
        cascade_type: str = "from_edges",
        stagger_delay: float = 0.08,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add PanelCascade for staggered panel entrance animations.

        Creates beautiful staggered animations for multi-panel layouts. Each panel
        animates in with a short delay, creating a cascading reveal effect.
        Perfect for Grid, ThreeColumn, Mosaic, and other multi-panel layouts.

        Perfect for: Grid layouts, multi-column content, photo galleries, feature showcases

        Example cascade_type values and their effects:
        - from_edges: Slide from nearest edge (spatial, intelligent, professional)
        - from_center: Scale radially from center (attention-grabbing, focal)
        - bounce_in: Bounce with overshoot (playful, energetic)
        - sequential_left: Left→right sequence (reading order, familiar)
        - sequential_right: Right→left sequence (reverse flow)
        - sequential_top: Top→bottom sequence (vertical flow)
        - wave: Diagonal wave pattern (dynamic, flowing)

        Example items array for 3x3 grid:
        [
            {"type": "CodeBlock", "config": {"code": "Panel 1", "language": "python"}},
            {"type": "CodeBlock", "config": {"code": "Panel 2", "language": "javascript"}},
            {"type": "CodeBlock", "config": {"code": "Panel 3", "language": "rust"}},
            {"type": "DemoBox", "config": {}},
            {"type": "DemoBox", "config": {}},
            {"type": "DemoBox", "config": {}},
            {"type": "Counter", "config": {"start_value": 0, "end_value": 1000}},
            {"type": "Counter", "config": {"start_value": 0, "end_value": 2000}},
            {"type": "Counter", "config": {"start_value": 0, "end_value": 3000}}
        ]

        Stagger delay recommendations:
        - 0.05-0.08s: Fast (TikTok/Shorts, sprint tempo)
        - 0.08-0.12s: Balanced (YouTube, medium tempo)
        - 0.12-0.2s: Deliberate (Presentations, slow tempo)

        Args:
            items: JSON array of panel components (format: [{"type": "ComponentName", "config": {...}}, ...])
            cascade_type: Cascade style - one of: from_edges, from_center, bounce_in, sequential_left, sequential_right, sequential_top, wave (default: "from_edges")
                - "from_edges": Panels slide in from nearest screen edge (spatial, professional)
                - "from_center": Panels scale out from center (radial, attention-grabbing)
                - "bounce_in": Panels bounce in with slight overshoot (playful, energetic)
                - "sequential_left": Left to right sequence (reading order, familiar)
                - "sequential_right": Right to left sequence (reverse flow)
                - "sequential_top": Top to bottom sequence (vertical flow)
                - "wave": Wave pattern across panels (dynamic, flowing)
            stagger_delay: Delay between each panel animation in seconds (default: 0.08)
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Cascade grid panels from edges
            remotion_add_panel_cascade(
                items='[{"type":"CodeBlock","config":{"code":"Panel 1"}},{"type":"CodeBlock","config":{"code":"Panel 2"}},{"type":"CodeBlock","config":{"code":"Panel 3"}}]',
                cascade_type="from_edges",
                stagger_delay=0.08,
                duration=10.0
            )

            # Bounce in panels playfully
            remotion_add_panel_cascade(
                items='[{"type":"DemoBox","config":{}},{"type":"DemoBox","config":{}}]',
                cascade_type="bounce_in",
                stagger_delay=0.12
            )

            # Sequential left-to-right cascade
            remotion_add_panel_cascade(
                items='[...]',
                cascade_type="sequential_left",
                stagger_delay=0.1
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse items array
                items_parsed = json.loads(items)

                if not isinstance(items_parsed, list):
                    return ErrorResponse(
                        error="items must be a JSON array of components"
                    ).model_dump_json()

                # Parse each item
                panel_components = []
                for item in items_parsed:
                    component = parse_nested_component(item)
                    # Validate that we got a ComponentInstance
                    if not isinstance(component, ComponentInstance):
                        return ErrorResponse(
                            error="Invalid item format. Each item must be: {'type': 'ComponentName', 'config': {...}}"
                        ).model_dump_json()
                    panel_components.append(component)

                # Validate cascade type
                valid_types = [
                    "from_edges",
                    "from_center",
                    "bounce_in",
                    "sequential_left",
                    "sequential_right",
                    "sequential_top",
                    "wave",
                ]
                if cascade_type not in valid_types:
                    return ErrorResponse(
                        error=f"Invalid cascade_type. Must be one of: {', '.join(valid_types)}"
                    ).model_dump_json()

                # Build props
                props = {
                    "items": panel_components,
                    "cascadeType": cascade_type,
                    "staggerDelay": stagger_delay,
                }

                component = ComponentInstance(
                    component_type="PanelCascade",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="PanelCascade",
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
