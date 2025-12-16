"""MCP tool registration for BrowserFrame component."""

from chuk_motion.models import ErrorResponse, FrameComponentResponse


def register_tool(mcp, project_manager):
    """Register the BrowserFrame MCP tool."""

    @mcp.tool
    async def remotion_add_browser_frame(
        duration: float,
        url: str = "https://example.com",
        theme: str = "chrome",
        tabs: str | None = None,
        show_status: bool = False,
        status_text: str = "",
        content: str = "",
        width: int = 1200,
        height: int = 800,
        position: str = "center",
        shadow: bool = True,
    ) -> str:
        """
        Add a BrowserFrame component to the composition.

        Browser window mockup with address bar, tabs, and content area.

        Args:
            duration: Duration in seconds
            url: URL to display in address bar
            theme: Browser theme (chrome, firefox, safari, etc.)
            tabs: JSON array of tab objects with title and active state
            show_status: Show status bar at bottom
            status_text: Text for status bar
            content: Content to display in browser viewport
            width: Browser width in pixels
            height: Browser height in pixels
            position: Position on screen
            shadow: Show window shadow

        Returns:
            JSON with component info
        """
        if not project_manager.current_timeline:
            return ErrorResponse(
                error="No active project. Create a project first."
            ).model_dump_json()

        try:
            builder = project_manager.current_timeline
            start_time = builder.get_total_duration_seconds()

            builder.add_browser_frame(
                start_time=start_time,
                duration=duration,
                url=url,
                theme=theme,
                tabs=tabs if tabs else None,
                show_status=show_status,
                status_text=status_text,
                content=content,
                width=width,
                height=height,
                position=position,
                shadow=shadow,
            )

            return FrameComponentResponse(
                component="BrowserFrame",
                position=position,
                theme=theme,
                start_time=start_time,
                duration=duration,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
