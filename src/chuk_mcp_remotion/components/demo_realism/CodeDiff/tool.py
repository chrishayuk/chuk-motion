"""MCP tool registration for CodeDiff component."""

import json
from .schema import CodeDiffProps, MCP_SCHEMA, METADATA


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
        """Add a CodeDiff component to the composition."""
        # Parse lines JSON string
        try:
            lines_parsed = json.loads(lines)
        except json.JSONDecodeError:
            lines_parsed = []

        props = CodeDiffProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            lines=lines_parsed,
            mode=mode,
            language=language,
            showLineNumbers=showLineNumbers,
            showHeatmap=showHeatmap,
            title=title,
            leftLabel=leftLabel,
            rightLabel=rightLabel,
            theme=theme,
            width=width,
            height=height,
            position=position,
            animateLines=animateLines,
        )

        project = project_manager.get_active_project()
        track_name = "code_diffs"
        project.add_component_to_track(
            track_name=track_name,
            component_type=METADATA.name,
            props=props.model_dump(),
            start_frame=startFrame,
            duration=durationInFrames,
        )

        line_count = len(lines)
        return f"Added {METADATA.name} component: {mode} mode with {line_count} lines at {position}"
