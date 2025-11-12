"""MCP tool registration for BrowserFrame component."""

import json

from chuk_motion.models import ErrorResponse, FrameComponentResponse

from .schema import METADATA, BrowserFrameProps


def register_tool(mcp, project_manager):
    """Register the BrowserFrame MCP tool."""

    @mcp.tool
    async def remotion_add_browser_frame(
        startFrame: int,
        durationInFrames: int,
        url: str = "https://example.com",
        theme: str = "chrome",
        tabs: str | None = None,
        showStatus: bool = False,
        statusText: str = "",
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
            startFrame: Frame to start showing the component
            durationInFrames: How many frames to show the component
            url: URL to display in address bar
            theme: Browser theme (chrome, firefox, safari, etc.)
            tabs: JSON array of tab objects with title and active state
            showStatus: Show status bar at bottom
            statusText: Text for status bar
            content: Content to display in browser viewport
            width: Browser width in pixels
            height: Browser height in pixels
            position: Position on screen
            shadow: Show window shadow

        Returns:
            JSON with component info
        """
        # Parse tabs JSON string if provided
        tabs_parsed = None
        if tabs:
            try:
                tabs_parsed = json.loads(tabs)
            except json.JSONDecodeError:
                tabs_parsed = None

        props = BrowserFrameProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            url=url,
            theme=theme,  # type: ignore[arg-type]
            tabs=tabs_parsed,
            showStatus=showStatus,
            statusText=statusText,
            content=content,
            width=width,
            height=height,
            position=position,  # type: ignore[arg-type]
            shadow=shadow,
        )

        try:
            project = project_manager.get_active_project()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

        try:
            track_name = "browser_windows"
            project.add_component_to_track(
                track_name=track_name,
                component_type=METADATA.name,
                props=props.model_dump(),
                start_frame=startFrame,
                duration=durationInFrames,
            )

            # Calculate duration in seconds (assuming 30fps)
            duration_seconds = durationInFrames / 30.0
            start_seconds = startFrame / 30.0

            return FrameComponentResponse(
                component="BrowserFrame",
                position=position,
                theme=theme,
                start_time=start_seconds,
                duration=duration_seconds,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
