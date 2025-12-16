# chuk-motion/src/chuk_motion/components/content/WebPage/tool.py
"""WebPage MCP tool."""

import asyncio

from chuk_motion.models import ComponentResponse, ErrorResponse


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
                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_web_page(
                    html=html,
                    start_time=start_time,
                    css=css,
                    base_styles=base_styles,
                    scale=scale,
                    scroll_y=scroll_y,
                    animate_scroll=animate_scroll,
                    scroll_duration=scroll_duration,
                    theme=theme,
                    duration=duration,
                )

                return ComponentResponse(
                    component="WebPage",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
