"""MCP tool registration for BrowserFrame component."""

import json

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
        """Add a BrowserFrame component to the composition."""
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

        project = project_manager.get_active_project()
        track_name = "browser_windows"
        project.add_component_to_track(
            track_name=track_name,
            component_type=METADATA.name,
            props=props.model_dump(),
            start_frame=startFrame,
            duration=durationInFrames,
        )

        return f"Added {METADATA.name} component: {theme} theme at {position} showing {url}"
