"""MCP tool registration for CodeDiff component."""

from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the CodeDiff MCP tool."""

    @mcp.tool
    async def remotion_add_code_diff(
        duration: float,
        lines: str = "[]",
        mode: str = "unified",
        language: str = "typescript",
        show_line_numbers: bool = True,
        show_heatmap: bool = False,
        title: str = "Code Comparison",
        left_label: str = "Before",
        right_label: str = "After",
        theme: str = "dark",
        width: int = 1400,
        height: int = 800,
        position: str = "center",
        animate_lines: bool = True,
    ) -> str:
        """
        Add a CodeDiff component to the composition.

        Side-by-side or unified code comparison with syntax highlighting.

        Args:
            duration: Duration in seconds
            lines: JSON array of diff lines with type and content
            mode: Display mode ("unified" or "split")
            language: Programming language for syntax highlighting
            show_line_numbers: Show line numbers
            show_heatmap: Show change heatmap visualization
            title: Optional title
            left_label: Label for left/before side
            right_label: Label for right/after side
            theme: Color theme (dark or light)
            width: Component width in pixels
            height: Component height in pixels
            position: Position on screen
            animate_lines: Animate line-by-line reveal

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

            builder.add_code_diff(
                start_time=start_time,
                duration=duration,
                lines=lines,
                mode=mode,
                language=language,
                show_line_numbers=show_line_numbers,
                show_heatmap=show_heatmap,
                title=title,
                left_label=left_label,
                right_label=right_label,
                theme=theme,
                width=width,
                height=height,
                position=position,
                animate_lines=animate_lines,
            )

            return ComponentResponse(
                component="CodeDiff",
                start_time=start_time,
                duration=duration,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
