"""MCP tool registration for BeforeAfterSlider component."""

from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the BeforeAfterSlider MCP tool."""

    @mcp.tool
    async def remotion_add_before_after_slider(
        duration: float,
        before_image: str,
        after_image: str,
        before_label: str = "Before",
        after_label: str = "After",
        orientation: str = "horizontal",
        slider_position: float = 50.0,
        animate_slider: bool = True,
        slider_start_position: float = 0.0,
        slider_end_position: float = 100.0,
        show_labels: bool = True,
        label_position: str = "overlay",
        handle_style: str = "default",
        width: int = 1200,
        height: int = 800,
        position: str = "center",
        border_radius: int = 12,
    ) -> str:
        """
        Add a BeforeAfterSlider component to the composition.

        Interactive before/after image comparison with sliding divider.

        Args:
            duration: Duration in seconds
            before_image: URL or path to before image
            after_image: URL or path to after image
            before_label: Label for before side
            after_label: Label for after side
            orientation: Slider orientation (horizontal, vertical)
            slider_position: Initial slider position (0-100)
            animate_slider: Animate slider movement
            slider_start_position: Animation start position
            slider_end_position: Animation end position
            show_labels: Show before/after labels
            label_position: Label position (overlay, top, bottom)
            handle_style: Slider handle style
            width: Component width in pixels
            height: Component height in pixels
            position: Position on screen
            border_radius: Corner radius in pixels

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

            builder.add_before_after_slider(
                start_time=start_time,
                duration=duration,
                before_image=before_image,
                after_image=after_image,
                before_label=before_label,
                after_label=after_label,
                orientation=orientation,
                slider_position=slider_position,
                animate_slider=animate_slider,
                slider_start_position=slider_start_position,
                slider_end_position=slider_end_position,
                show_labels=show_labels,
                label_position=label_position,
                handle_style=handle_style,
                width=width,
                height=height,
                position=position,
                border_radius=border_radius,
            )

            return LayoutComponentResponse(
                component="BeforeAfterSlider",
                layout=f"{orientation}-slider",
                start_time=start_time,
                duration=duration,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
