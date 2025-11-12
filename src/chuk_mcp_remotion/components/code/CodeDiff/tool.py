"""MCP tool registration for CodeDiff component."""

import json

from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse

from .schema import METADATA, CodeDiffProps


def register_tool(mcp, project_manager):
    """Register the CodeDiff MCP tool."""

    @mcp.tool
    async def remotion_add_code_diff(
        startFrame: int,
        durationInFrames: int,
        lines: str = "[]",
        mode: str = "unified",
        language: str = "typescript",
        showLineNumbers: bool = True,
        showHeatmap: bool = False,
        title: str = "Code Comparison",
        leftLabel: str = "Before",
        rightLabel: str = "After",
        theme: str = "dark",
        width: int = 1400,
        height: int = 800,
        position: str = "center",
        animateLines: bool = True,
    ) -> str:
        """
        Add a CodeDiff component to the composition.

        Side-by-side or unified code comparison with syntax highlighting.

        Args:
            startFrame: Frame to start showing the component
            durationInFrames: How many frames to show the component
            lines: JSON array of diff lines with type and content
            mode: Display mode ("unified" or "split")
            language: Programming language for syntax highlighting
            showLineNumbers: Show line numbers
            showHeatmap: Show change heatmap visualization
            title: Optional title
            leftLabel: Label for left/before side
            rightLabel: Label for right/after side
            theme: Color theme (dark or light)
            width: Component width in pixels
            height: Component height in pixels
            position: Position on screen
            animateLines: Animate line-by-line reveal

        Returns:
            JSON with component info
        """
        # Parse lines JSON string
        try:
            lines_parsed = json.loads(lines)
        except json.JSONDecodeError:
            lines_parsed = []

        props = CodeDiffProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            lines=lines_parsed,
            mode=mode,  # type: ignore[arg-type]
            language=language,
            showLineNumbers=showLineNumbers,
            showHeatmap=showHeatmap,
            title=title,
            leftLabel=leftLabel,
            rightLabel=rightLabel,
            theme=theme,  # type: ignore[arg-type]
            width=width,
            height=height,
            position=position,  # type: ignore[arg-type]
            animateLines=animateLines,
        )

        try:
            project = project_manager.get_active_project()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

        try:
            track_name = "code_diffs"
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

            return ComponentResponse(
                component="CodeDiff",
                start_time=start_seconds,
                duration=duration_seconds,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
