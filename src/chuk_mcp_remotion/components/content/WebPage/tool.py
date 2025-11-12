# chuk-mcp-remotion/src/chuk_mcp_remotion/components/content/WebPage/tool.py
"""WebPage MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the WebPage tool with the MCP server."""

    @mcp.tool
    async def remotion_add_webpage(
        html: str = '<div style="padding: 40px; text-align: center;"><h1>Hello World</h1><p>This is a web page.</p></div>',
        css: str = "",
        base_styles: bool = True,
        scale: float = 1.0,
        scroll_y: float = 0,
        animate_scroll: bool = False,
        scroll_duration: float = 60,
        theme: str = "light",
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add WebPage to the composition.

        Render real HTML content with CSS styling. Perfect for showing actual web pages
        inside browser frames or as standalone content.

        Args:
            html: HTML content to render
            css: Custom CSS styles to apply
            base_styles: Include default styling for common HTML elements (typography, buttons, etc.)
            scale: Zoom level (1.0 = 100%, 0.5 = 50%, 2.0 = 200%)
            scroll_y: Vertical scroll position in pixels
            animate_scroll: Animate scroll from 0 to scroll_y over scroll_duration
            scroll_duration: Duration of scroll animation in frames (default 60 = 2 seconds at 30fps)
            theme: Visual theme (light, dark)
            duration: Duration in seconds or time string (e.g., "2s", "500ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            Add a landing page:
            ```
            html = '''
            <header style="text-align: center; padding: 60px 0;">
              <h1>Welcome to Our App</h1>
              <p>The best solution for your needs</p>
              <button>Get Started</button>
            </header>
            '''
            ```
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="WebPage",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "html": html,
                        "css": css,
                        "baseStyles": base_styles,
                        "scale": scale,
                        "scrollY": scroll_y,
                        "animateScroll": animate_scroll,
                        "scrollDuration": scroll_duration,
                        "theme": theme,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="WebPage",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
