"""MCP tool registration for BeforeAfterSlider component."""

from chuk_motion.models import ErrorResponse, LayoutComponentResponse

from .schema import METADATA, BeforeAfterSliderProps


def register_tool(mcp, project_manager):
    """Register the BeforeAfterSlider MCP tool."""

    @mcp.tool
    async def remotion_add_before_after_slider(
        startFrame: int,
        durationInFrames: int,
        beforeImage: str,
        afterImage: str,
        beforeLabel: str = "Before",
        afterLabel: str = "After",
        orientation: str = "horizontal",
        sliderPosition: float = 50.0,
        animateSlider: bool = True,
        sliderStartPosition: float = 0.0,
        sliderEndPosition: float = 100.0,
        showLabels: bool = True,
        labelPosition: str = "overlay",
        handleStyle: str = "default",
        width: int = 1200,
        height: int = 800,
        position: str = "center",
        borderRadius: int = 12,
    ) -> str:
        """
        Add a BeforeAfterSlider component to the composition.

        Interactive before/after image comparison with sliding divider.

        Args:
            startFrame: Frame to start showing the component
            durationInFrames: How many frames to show the component
            beforeImage: URL or path to before image
            afterImage: URL or path to after image
            beforeLabel: Label for before side
            afterLabel: Label for after side
            orientation: Slider orientation (horizontal, vertical)
            sliderPosition: Initial slider position (0-100)
            animateSlider: Animate slider movement
            sliderStartPosition: Animation start position
            sliderEndPosition: Animation end position
            showLabels: Show before/after labels
            labelPosition: Label position (overlay, top, bottom)
            handleStyle: Slider handle style
            width: Component width in pixels
            height: Component height in pixels
            position: Position on screen
            borderRadius: Corner radius in pixels

        Returns:
            JSON with component info
        """
        props = BeforeAfterSliderProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            beforeImage=beforeImage,
            afterImage=afterImage,
            beforeLabel=beforeLabel,
            afterLabel=afterLabel,
            orientation=orientation,  # type: ignore[arg-type]
            sliderPosition=sliderPosition,
            animateSlider=animateSlider,
            sliderStartPosition=sliderStartPosition,
            sliderEndPosition=sliderEndPosition,
            showLabels=showLabels,
            labelPosition=labelPosition,  # type: ignore[arg-type]
            handleStyle=handleStyle,  # type: ignore[arg-type]
            width=width,
            height=height,
            position=position,  # type: ignore[arg-type]
            borderRadius=borderRadius,
        )

        try:
            project = project_manager.get_active_project()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

        try:
            track_name = "comparisons"
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

            return LayoutComponentResponse(
                component="BeforeAfterSlider",
                layout=f"{orientation}-slider",
                start_time=start_seconds,
                duration=duration_seconds,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
