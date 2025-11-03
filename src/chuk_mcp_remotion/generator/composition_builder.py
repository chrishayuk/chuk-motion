"""
Composition Builder - Combines components into complete video compositions.

Manages the timeline, layering, and sequencing of video components.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ComponentInstance:
    """Represents an instance of a component in the timeline."""

    component_type: str  # TitleScene, LowerThird, etc.
    start_frame: int
    duration_frames: int
    props: dict[str, Any] = field(default_factory=dict)
    layer: int = 0  # Higher layers render on top


class CompositionBuilder:
    """Builds complete video compositions from components."""

    def __init__(
        self, fps: int = 30, width: int = 1920, height: int = 1080, transparent: bool = False
    ):
        """
        Initialize composition builder.

        Args:
            fps: Frames per second (default: 30)
            width: Video width in pixels (default: 1920)
            height: Video height in pixels (default: 1080)
            transparent: Use transparent background (default: False)
        """
        self.fps = fps
        self.width = width
        self.height = height
        self.components: list[ComponentInstance] = []
        self.theme = "tech"
        self.transparent = transparent

    def seconds_to_frames(self, seconds: float) -> int:
        """Convert seconds to frames."""
        return int(seconds * self.fps)

    def frames_to_seconds(self, frames: int) -> float:
        """Convert frames to seconds."""
        return frames / self.fps

    def create_code_block_instance(
        self,
        code: str,
        language: str = "javascript",
        title: str | None = None,
        start_frame: int = 0,
        duration_frames: int = 150,
        variant: str = "editor",
        animation: str = "fade_in",
        show_line_numbers: bool = True,
    ) -> ComponentInstance:
        """
        Create a CodeBlock instance without adding it to the composition.
        Useful for creating children for layout components.
        """
        return ComponentInstance(
            component_type="CodeBlock",
            start_frame=start_frame,
            duration_frames=duration_frames,
            props={
                "code": code,
                "language": language,
                "title": title,
                "variant": variant,
                "animation": animation,
                "show_line_numbers": show_line_numbers,
            },
            layer=5,
        )

    def add_title_scene(
        self,
        text: str,
        subtitle: str | None = None,
        duration_seconds: float = 3.0,
        variant: str = "bold",
        animation: str = "fade_zoom",
    ) -> "CompositionBuilder":
        """
        Add a title scene to the composition.

        Args:
            text: Main title text
            subtitle: Optional subtitle
            duration_seconds: Duration in seconds
            variant: Style variant
            animation: Animation style

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="TitleScene",
            start_frame=self._get_next_start_frame(),
            duration_frames=self.seconds_to_frames(duration_seconds),
            props={"title": text, "subtitle": subtitle, "variant": variant, "animation": animation},
            layer=0,
        )
        self.components.append(component)
        return self

    def add_line_chart(
        self,
        data: list,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> "CompositionBuilder":
        """
        Add an animated line chart to the composition.

        Args:
            data: List of [x, y] data points
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="LineChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title, "xlabel": xlabel, "ylabel": ylabel},
            layer=5,  # Charts render above main content but below overlays
        )
        self.components.append(component)
        return self

    def add_bar_chart(
        self,
        data: list,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> "CompositionBuilder":
        """
        Add an animated vertical bar chart to the composition.

        Args:
            data: List of {label, value, color?} dicts
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="BarChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title, "xlabel": xlabel, "ylabel": ylabel},
            layer=5,
        )
        self.components.append(component)
        return self

    def add_horizontal_bar_chart(
        self,
        data: list,
        title: str | None = None,
        xlabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
    ) -> "CompositionBuilder":
        """
        Add an animated horizontal bar chart to the composition.

        Args:
            data: List of {label, value, color?} dicts
            title: Optional chart title
            xlabel: Optional x-axis label
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="HorizontalBarChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title, "xlabel": xlabel},
            layer=5,
        )
        self.components.append(component)
        return self

    def add_area_chart(
        self,
        data: list,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> "CompositionBuilder":
        """
        Add an animated area chart to the composition.

        Args:
            data: List of [x, y] data points
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="AreaChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title, "xlabel": xlabel, "ylabel": ylabel},
            layer=5,
        )
        self.components.append(component)
        return self

    def add_pie_chart(
        self,
        data: list,
        title: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> "CompositionBuilder":
        """
        Add an animated pie chart to the composition.

        Args:
            data: List of {label, value, color?} dicts
            title: Optional chart title
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="PieChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title},
            layer=5,
        )
        self.components.append(component)
        return self

    def add_donut_chart(
        self,
        data: list,
        title: str | None = None,
        center_text: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> "CompositionBuilder":
        """
        Add an animated donut chart to the composition.

        Args:
            data: List of {label, value, color?} dicts
            title: Optional chart title
            center_text: Text to display in center
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="DonutChart",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"data": data, "title": title, "centerText": center_text},
            layer=5,
        )
        self.components.append(component)
        return self

    def add_lower_third(
        self,
        name: str,
        title: str | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        variant: str = "glass",
        position: str = "bottom_left",
    ) -> "CompositionBuilder":
        """
        Add a lower third overlay to the composition.

        Args:
            name: Main name/text
            title: Optional subtitle
            start_time: When to show (seconds)
            duration: How long to show (seconds)
            variant: Style variant
            position: Screen position

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="LowerThird",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={"name": name, "title": title, "variant": variant, "position": position},
            layer=10,  # Overlays render on top
        )
        self.components.append(component)
        return self

    def add_code_block(
        self,
        code: str,
        language: str = "javascript",
        title: str | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        variant: str = "editor",
        animation: str = "fade_in",
        show_line_numbers: bool = True,
    ) -> "CompositionBuilder":
        """
        Add a static code block to the composition.

        Args:
            code: Code content to display
            language: Programming language
            title: Optional title/filename
            start_time: When to show (seconds)
            duration: How long to show (seconds)
            variant: Style variant (minimal, terminal, editor, glass)
            animation: Entrance animation
            show_line_numbers: Show line numbers

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="CodeBlock",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "code": code,
                "language": language,
                "title": title,
                "variant": variant,
                "animation": animation,
                "show_line_numbers": show_line_numbers,
            },
            layer=5,  # Code blocks render with charts
        )
        self.components.append(component)
        return self

    def add_typing_code(
        self,
        code: str,
        language: str = "javascript",
        title: str | None = None,
        start_time: float = 0.0,
        duration: float = 10.0,
        variant: str = "editor",
        cursor_style: str = "line",
        typing_speed: str = "normal",
        show_line_numbers: bool = True,
    ) -> "CompositionBuilder":
        """
        Add an animated typing code effect to the composition.

        Args:
            code: Code to type out
            language: Programming language
            title: Optional title/filename
            start_time: When to start (seconds)
            duration: How long to type (seconds)
            variant: Style variant (minimal, terminal, editor, hacker)
            cursor_style: Cursor appearance (block, line, underline, none)
            typing_speed: Typing speed (slow, normal, fast, instant)
            show_line_numbers: Show line numbers

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="TypingCode",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "code": code,
                "language": language,
                "title": title,
                "variant": variant,
                "cursor_style": cursor_style,
                "typing_speed": typing_speed,
                "show_line_numbers": show_line_numbers,
            },
            layer=5,  # Code blocks render with charts
        )
        self.components.append(component)
        return self

    def add_container(
        self,
        child_component: ComponentInstance,
        position: str = "center",
        width: str = "auto",
        height: str = "auto",
        max_width: str | None = None,
        max_height: str | None = None,
        padding: int = 40,
    ) -> "CompositionBuilder":
        """
        Add a container layout that positions a child component.

        Args:
            child_component: The component to position
            position: Position on screen (center, top-left, top-right, etc.)
            width: Container width
            height: Container height
            max_width: Maximum width constraint
            max_height: Maximum height constraint
            padding: Padding from edges

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="Container",
            start_frame=child_component.start_frame,
            duration_frames=child_component.duration_frames,
            props={
                "position": position,
                "width": width,
                "height": height,
                "max_width": max_width,
                "max_height": max_height,
                "padding": padding,
                "children": child_component,  # Store child component
            },
            layer=child_component.layer,
        )
        self.components.append(component)
        return self

    def add_grid(
        self,
        child_components: list[ComponentInstance],
        start_time: float = 0.0,
        duration: float = 5.0,
        layout: str = "3x3",
        gap: int = 20,
        padding: int = 40,
        align_items: str | None = None,
        justify_items: str | None = None,
    ) -> "CompositionBuilder":
        """
        Add a grid layout that arranges multiple components.

        Args:
            child_components: List of components to arrange in grid
            start_time: When to show (seconds)
            duration: How long to show (seconds)
            layout: Grid layout (1x2, 2x1, 2x2, 3x2, 2x3, 3x3, 4x2, 2x4)
            gap: Gap between grid items
            padding: Padding from edges
            align_items: CSS align-items value
            justify_items: CSS justify-items value

        Returns:
            Self for chaining
        """
        component = ComponentInstance(
            component_type="Grid",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "layout": layout,
                "gap": gap,
                "padding": padding,
                "align_items": align_items,
                "justify_items": justify_items,
                "children": child_components,  # Store child components
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_over_the_shoulder_layout(
        self,
        host_view: ComponentInstance | None = None,
        screen_content: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        host_position: str = "left",
        host_size: int = 35,
        gap: int = 20,
        border_width: int = 2,
        padding: int = 40,
    ) -> "CompositionBuilder":
        """Add OverTheShoulderLayout to composition."""
        component = ComponentInstance(
            component_type="OverTheShoulderLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "host_position": host_position,
                "host_size": host_size,
                "gap": gap,
                "border_width": border_width,
                "padding": padding,
                "hostView": host_view,
                "screenContent": screen_content,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_dialogue_frame_layout(
        self,
        character_a: ComponentInstance | None = None,
        character_b: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        character_a_label: str = "",
        character_b_label: str = "",
        gap: int = 20,
        border_width: int = 2,
        padding: int = 40,
    ) -> "CompositionBuilder":
        """Add DialogueFrameLayout to composition."""
        component = ComponentInstance(
            component_type="DialogueFrameLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "character_a_label": character_a_label,
                "character_b_label": character_b_label,
                "gap": gap,
                "border_width": border_width,
                "padding": padding,
                "characterA": character_a,
                "characterB": character_b,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_stacked_reaction_layout(
        self,
        original_clip: ComponentInstance | None = None,
        reactor_face: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        clip_ratio: int = 65,
        gap: int = 20,
        show_labels: bool = True,
        border_width: int = 2,
        padding: int = 40,
    ) -> "CompositionBuilder":
        """Add StackedReactionLayout to composition."""
        component = ComponentInstance(
            component_type="StackedReactionLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "clip_ratio": clip_ratio,
                "gap": gap,
                "show_labels": show_labels,
                "border_width": border_width,
                "padding": padding,
                "originalClip": original_clip,
                "reactorFace": reactor_face,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_hud_style_layout(
        self,
        gameplay: ComponentInstance | None = None,
        webcam: ComponentInstance | None = None,
        chat_overlay: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        webcam_position: str = "top-left",
        webcam_size: int = 15,
        show_chat: bool = True,
        chat_width: int = 25,
    ) -> "CompositionBuilder":
        """Add HUDStyleLayout to composition."""
        component = ComponentInstance(
            component_type="HUDStyleLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "webcam_position": webcam_position,
                "webcam_size": webcam_size,
                "show_chat": show_chat,
                "chat_width": chat_width,
                "gameplay": gameplay,
                "webcam": webcam,
                "chatOverlay": chat_overlay,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_performance_multi_cam_layout(
        self,
        front_cam: ComponentInstance | None = None,
        overhead_cam: ComponentInstance | None = None,
        hand_cam: ComponentInstance | None = None,
        detail_cam: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        labels: dict[str, str] | None = None,
        gap: int = 20,
        show_labels: bool = True,
        border_width: int = 2,
        padding: int = 40,
    ) -> "CompositionBuilder":
        """Add PerformanceMultiCamLayout to composition."""
        if labels is None:
            labels = {
                "front": "FRONT VIEW",
                "overhead": "OVERHEAD",
                "hand": "HAND CAM",
                "detail": "DETAIL",
            }

        component = ComponentInstance(
            component_type="PerformanceMultiCamLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "labels": labels,
                "gap": gap,
                "show_labels": show_labels,
                "border_width": border_width,
                "padding": padding,
                "frontCam": front_cam,
                "overheadCam": overhead_cam,
                "handCam": hand_cam,
                "detailCam": detail_cam,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_focus_strip_layout(
        self,
        host_strip: ComponentInstance | None = None,
        background_content: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        strip_height: int = 30,
        strip_position: str = "center",
        background_blur: int = 5,
        border_width: int = 2,
        strip_shadow: bool = True,
    ) -> "CompositionBuilder":
        """Add FocusStripLayout to composition."""
        component = ComponentInstance(
            component_type="FocusStripLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "strip_height": strip_height,
                "strip_position": strip_position,
                "background_blur": background_blur,
                "border_width": border_width,
                "strip_shadow": strip_shadow,
                "hostStrip": host_strip,
                "backgroundContent": background_content,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_split_screen(
        self,
        left_panel: ComponentInstance | None = None,
        right_panel: ComponentInstance | None = None,
        top_panel: ComponentInstance | None = None,
        bottom_panel: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        orientation: str = "horizontal",
        ratio: float = 0.5,
        gap: int = 20,
        padding: int = 40,
        divider_width: int = 2,
        divider_color: str | None = None,
    ) -> "CompositionBuilder":
        """Add SplitScreen layout to composition."""
        component = ComponentInstance(
            component_type="SplitScreen",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "orientation": orientation,
                "ratio": ratio,
                "gap": gap,
                "padding": padding,
                "divider_width": divider_width,
                "divider_color": divider_color,
                "leftPanel": left_panel,
                "rightPanel": right_panel,
                "topPanel": top_panel,
                "bottomPanel": bottom_panel,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_three_by_three_grid(
        self,
        children: list[ComponentInstance],
        start_time: float = 0.0,
        duration: float = 5.0,
        padding: int = 40,
        gap: int = 20,
        border_width: int | None = None,
        border_color: str = "rgba(255,255,255,0.2)",
        cell_background: str | None = None,
    ) -> "CompositionBuilder":
        """Add ThreeByThreeGrid layout to composition."""
        component = ComponentInstance(
            component_type="ThreeByThreeGrid",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "padding": padding,
                "gap": gap,
                "border_width": border_width,
                "border_color": border_color,
                "cell_background": cell_background,
                "children": children,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_three_column_layout(
        self,
        left: ComponentInstance | None = None,
        center: ComponentInstance | None = None,
        right: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        left_width: int = 33,
        center_width: int = 34,
        right_width: int = 33,
        gap: int = 20,
        padding: int = 40,
        border_width: int | None = None,
    ) -> "CompositionBuilder":
        """Add ThreeColumnLayout to composition."""
        component = ComponentInstance(
            component_type="ThreeColumnLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "left_width": left_width,
                "center_width": center_width,
                "right_width": right_width,
                "gap": gap,
                "padding": padding,
                "border_width": border_width,
                "left": left,
                "center": center,
                "right": right,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_three_row_layout(
        self,
        top: ComponentInstance | None = None,
        middle: ComponentInstance | None = None,
        bottom: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        top_height: int = 33,
        middle_height: int = 34,
        bottom_height: int = 33,
        gap: int = 20,
        padding: int = 40,
        border_width: int | None = None,
    ) -> "CompositionBuilder":
        """Add ThreeRowLayout to composition."""
        component = ComponentInstance(
            component_type="ThreeRowLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "top_height": top_height,
                "middle_height": middle_height,
                "bottom_height": bottom_height,
                "gap": gap,
                "padding": padding,
                "border_width": border_width,
                "top": top,
                "middle": middle,
                "bottom": bottom,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_asymmetric_layout(
        self,
        main_feed: ComponentInstance | None = None,
        demo1: ComponentInstance | None = None,
        demo2: ComponentInstance | None = None,
        overlay: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        layout: str = "main-right",
        main_ratio: int = 67,
        padding: int = 40,
        gap: int = 20,
        border_width: int | None = None,
    ) -> "CompositionBuilder":
        """Add AsymmetricLayout to composition."""
        component = ComponentInstance(
            component_type="AsymmetricLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "layout": layout,
                "main_ratio": main_ratio,
                "padding": padding,
                "gap": gap,
                "border_width": border_width,
                "mainFeed": main_feed,
                "demo1": demo1,
                "demo2": demo2,
                "overlay": overlay,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_pip_layout(
        self,
        main_content: ComponentInstance | None = None,
        pip_content: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        pip_position: str = "bottom-right",
        pip_size: int = 20,
        pip_border_width: int = 2,
        padding: int = 20,
    ) -> "CompositionBuilder":
        """Add PiPLayout to composition."""
        component = ComponentInstance(
            component_type="PiPLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "pip_position": pip_position,
                "pip_size": pip_size,
                "pip_border_width": pip_border_width,
                "padding": padding,
                "mainContent": main_content,
                "pipContent": pip_content,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_vertical_layout(
        self,
        top_content: ComponentInstance | None = None,
        bottom_content: ComponentInstance | None = None,
        caption_bar: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        layout: str = "top-bottom",
        content_ratio: int = 70,
        gap: int = 10,
        padding: int = 20,
    ) -> "CompositionBuilder":
        """Add VerticalLayout to composition."""
        component = ComponentInstance(
            component_type="VerticalLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "layout": layout,
                "content_ratio": content_ratio,
                "gap": gap,
                "padding": padding,
                "topContent": top_content,
                "bottomContent": bottom_content,
                "captionBar": caption_bar,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_timeline_layout(
        self,
        main_content: ComponentInstance | None = None,
        milestones: list[ComponentInstance] | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        timeline_height: int = 15,
        timeline_position: str = "bottom",
        show_progress: bool = True,
        padding: int = 20,
    ) -> "CompositionBuilder":
        """Add TimelineLayout to composition."""
        component = ComponentInstance(
            component_type="TimelineLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "timeline_height": timeline_height,
                "timeline_position": timeline_position,
                "show_progress": show_progress,
                "padding": padding,
                "mainContent": main_content,
                "milestones": milestones or [],
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_mosaic_layout(
        self,
        clips: list[ComponentInstance],
        start_time: float = 0.0,
        duration: float = 5.0,
        style: str = "hero-corners",
        gap: int = 15,
        border_width: int = 2,
        padding: int = 20,
    ) -> "CompositionBuilder":
        """Add MosaicLayout to composition."""
        component = ComponentInstance(
            component_type="MosaicLayout",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "style": style,
                "gap": gap,
                "border_width": border_width,
                "padding": padding,
                "clips": clips,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_container_layout(
        self,
        content: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        padding: int = 80,
        border_width: int = 2,
        border_radius: int = 8,
        border_color: str = "rgba(255,255,255,0.2)",
    ) -> "CompositionBuilder":
        """Add Container layout to composition."""
        component = ComponentInstance(
            component_type="Container",
            start_frame=self.seconds_to_frames(start_time),
            duration_frames=self.seconds_to_frames(duration),
            props={
                "padding": padding,
                "border_width": border_width,
                "border_radius": border_radius,
                "border_color": border_color,
                "content": content,
            },
            layer=5,
        )
        self.components.append(component)
        return self

    def add_grid_layout(
        self,
        children: list[ComponentInstance],
        start_time: float = 0.0,
        duration: float = 5.0,
        layout: str = "2x2",
        padding: int = 40,
        gap: int = 20,
        border_width: int | None = None,
    ) -> "CompositionBuilder":
        """Add Grid layout (alias for add_grid)."""
        return self.add_grid(
            child_components=children,
            start_time=start_time,
            duration=duration,
            layout=layout,
            gap=gap,
            padding=padding,
        )

    def add_split_screen_layout(
        self,
        left_panel: ComponentInstance | None = None,
        right_panel: ComponentInstance | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
        orientation: str = "horizontal",
        gap: int = 20,
        divider_width: int = 3,
    ) -> "CompositionBuilder":
        """Add SplitScreen layout (alias for add_split_screen)."""
        return self.add_split_screen(
            left_panel=left_panel,
            right_panel=right_panel,
            start_time=start_time,
            duration=duration,
            orientation=orientation,
            gap=gap,
            divider_width=divider_width,
        )

    def _get_next_start_frame(self) -> int:
        """Get the start frame for the next sequential component."""
        if not self.components:
            return 0

        # Find the last component on layer 0 (main content)
        layer_0_components = [c for c in self.components if c.layer == 0]
        if not layer_0_components:
            return 0

        last = max(layer_0_components, key=lambda c: c.start_frame + c.duration_frames)
        return last.start_frame + last.duration_frames

    def get_total_duration_frames(self) -> int:
        """Get total duration of the composition in frames."""
        if not self.components:
            return 0
        return max(c.start_frame + c.duration_frames for c in self.components)

    def get_total_duration_seconds(self) -> float:
        """Get total duration of the composition in seconds."""
        return self.frames_to_seconds(self.get_total_duration_frames())

    def generate_composition_tsx(self) -> str:
        """
        Generate the main VideoComposition.tsx component.

        Returns:
            TSX code for the complete composition
        """
        # Sort components by layer (lower layers first)
        sorted_components = sorted(self.components, key=lambda c: c.layer)

        # Find all nested children to exclude from top-level rendering
        nested_children = self._find_nested_children(sorted_components)

        # Generate import statements (recursively find all component types)
        unique_types = self._find_all_component_types(sorted_components)
        imports = "\n".join(
            [
                f"import {{ {comp_type} }} from './components/{comp_type}';"
                for comp_type in sorted(unique_types)
            ]
        )

        # Generate component JSX (only top-level components)
        components_jsx = []
        for comp in sorted_components:
            # Skip if this component is a child of another component
            if id(comp) in nested_children:
                continue

            jsx = self._render_component_jsx(comp, indent=6)
            components_jsx.append(jsx)

        components_jsx_str = "\n".join(components_jsx)

        # Background color: transparent or black
        background_color = "transparent" if self.transparent else "#000"

        # Generate complete composition
        tsx = f"""import React from 'react';
import {{ AbsoluteFill }} from 'remotion';
{imports}

interface VideoCompositionProps {{
  theme: string;
}}

export const VideoComposition: React.FC<VideoCompositionProps> = ({{ theme }}) => {{
  return (
    <AbsoluteFill style={{{{ backgroundColor: '{background_color}' }}}}>
{components_jsx_str}
    </AbsoluteFill>
  );
}};
"""
        return tsx

    def _find_all_component_types(self, components: list[ComponentInstance]) -> set:
        """Recursively find all component types including nested children."""
        types = set()

        def collect_types(comp):
            types.add(comp.component_type)

            # Check for nested children
            layout_types = [
                "Grid",
                "Container",
                "SplitScreen",
                "ThreeColumnLayout",
                "ThreeRowLayout",
                "ThreeByThreeGrid",
                "AsymmetricLayout",
                "OverTheShoulderLayout",
                "DialogueFrameLayout",
                "StackedReactionLayout",
                "HUDStyleLayout",
                "PerformanceMultiCamLayout",
                "FocusStripLayout",
                "PiPLayout",
                "VerticalLayout",
                "TimelineLayout",
                "MosaicLayout",
            ]

            if comp.component_type in layout_types:
                children = comp.props.get("children")
                if isinstance(children, list):
                    for child in children:
                        if isinstance(child, ComponentInstance):
                            collect_types(child)
                elif isinstance(children, ComponentInstance):
                    collect_types(children)

                # For SplitScreen and ThreeColumn/ThreeRow layouts
                for key in ["left", "right", "top", "bottom", "center", "middle"]:
                    child = comp.props.get(key)
                    if isinstance(child, ComponentInstance):
                        collect_types(child)

                # For specialized layouts
                specialized_keys = [
                    "mainFeed",
                    "demo1",
                    "demo2",
                    "overlay",  # AsymmetricLayout
                    "hostView",
                    "screenContent",  # OverTheShoulder
                    "characterA",
                    "characterB",  # DialogueFrame
                    "originalClip",
                    "reactorFace",  # StackedReaction
                    "gameplay",
                    "webcam",
                    "chatOverlay",  # HUDStyle
                    "frontCam",
                    "overheadCam",
                    "handCam",
                    "detailCam",  # PerformanceMultiCam
                    "hostStrip",
                    "backgroundContent",  # FocusStrip
                    "mainContent",
                    "pipContent",  # PiPLayout
                    "topContent",
                    "bottomContent",
                    "captionBar",  # VerticalLayout
                    "milestones",
                    "clips",  # TimelineLayout, MosaicLayout
                    "content",  # Container
                    "leftPanel",
                    "rightPanel",
                    "topPanel",
                    "bottomPanel",  # SplitScreen
                ]
                for key in specialized_keys:
                    child = comp.props.get(key)
                    if isinstance(child, ComponentInstance):
                        collect_types(child)

        for comp in components:
            collect_types(comp)

        return types

    def _find_nested_children(self, components: list[ComponentInstance]) -> set:
        """Find all components that are children of layout components."""
        nested = set()
        layout_types = [
            "Grid",
            "Container",
            "SplitScreen",
            "ThreeColumnLayout",
            "ThreeRowLayout",
            "ThreeByThreeGrid",
            "AsymmetricLayout",
            "OverTheShoulderLayout",
            "DialogueFrameLayout",
            "StackedReactionLayout",
            "HUDStyleLayout",
            "PerformanceMultiCamLayout",
            "FocusStripLayout",
            "PiPLayout",
            "VerticalLayout",
            "TimelineLayout",
            "MosaicLayout",
        ]

        for comp in components:
            if comp.component_type in layout_types:
                # Get children from props
                children = comp.props.get("children")
                if isinstance(children, list):
                    for child in children:
                        if isinstance(child, ComponentInstance):
                            nested.add(id(child))
                elif isinstance(children, ComponentInstance):
                    nested.add(id(children))

                # For SplitScreen and ThreeColumn/ThreeRow layouts
                for key in ["left", "right", "top", "bottom", "center", "middle"]:
                    child = comp.props.get(key)
                    if isinstance(child, ComponentInstance):
                        nested.add(id(child))

                # For specialized layouts
                specialized_keys = [
                    "mainFeed",
                    "demo1",
                    "demo2",
                    "overlay",  # AsymmetricLayout
                    "hostView",
                    "screenContent",  # OverTheShoulder
                    "characterA",
                    "characterB",  # DialogueFrame
                    "originalClip",
                    "reactorFace",  # StackedReaction
                    "gameplay",
                    "webcam",
                    "chatOverlay",  # HUDStyle
                    "frontCam",
                    "overheadCam",
                    "handCam",
                    "detailCam",  # PerformanceMultiCam
                    "hostStrip",
                    "backgroundContent",  # FocusStrip
                    "mainContent",
                    "pipContent",  # PiPLayout
                    "topContent",
                    "bottomContent",
                    "captionBar",  # VerticalLayout
                    "milestones",
                    "clips",  # TimelineLayout, MosaicLayout
                    "content",  # Container
                    "leftPanel",
                    "rightPanel",
                    "topPanel",
                    "bottomPanel",  # SplitScreen
                ]
                for key in specialized_keys:
                    child = comp.props.get(key)
                    if isinstance(child, ComponentInstance):
                        nested.add(id(child))
        return nested

    def _render_component_jsx(self, comp: ComponentInstance, indent: int = 0) -> str:
        """Render a component as JSX, including nested children."""
        # Check if this is a layout component with children
        layout_types = [
            "Grid",
            "Container",
            "SplitScreen",
            "ThreeColumnLayout",
            "ThreeRowLayout",
            "ThreeByThreeGrid",
            "AsymmetricLayout",
            "OverTheShoulderLayout",
            "DialogueFrameLayout",
            "StackedReactionLayout",
            "HUDStyleLayout",
            "PerformanceMultiCamLayout",
            "FocusStripLayout",
            "PiPLayout",
            "VerticalLayout",
            "TimelineLayout",
            "MosaicLayout",
        ]
        has_children = comp.component_type in layout_types

        if has_children:
            return self._render_layout_component(comp, indent)
        else:
            return self._render_simple_component(comp, indent)

    def _render_simple_component(self, comp: ComponentInstance, indent: int) -> str:
        """Render a simple component without children."""
        spaces = " " * indent

        # Format props (exclude children-related props)
        props_lines = []
        for key, value in comp.props.items():
            if key not in ["children", "left", "right", "top", "bottom"] and value is not None:
                props_lines.append(f"{spaces}  {key}={self._format_prop_value(value)}")
        props_str = "\n".join(props_lines) if props_lines else ""

        if props_str:
            return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}/>"""
        else:
            return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}/>"""

    def _render_layout_component(self, comp: ComponentInstance, indent: int) -> str:
        """Render a layout component with nested children."""
        spaces = " " * indent

        # Format non-children props
        # Exclude child component props from regular props
        exclude_keys = [
            "children",
            "left",
            "right",
            "top",
            "bottom",
            "center",
            "middle",
            "mainFeed",
            "demo1",
            "demo2",
            "overlay",  # AsymmetricLayout
            "hostView",
            "screenContent",  # OverTheShoulder
            "characterA",
            "characterB",  # DialogueFrame
            "originalClip",
            "reactorFace",  # StackedReaction
            "gameplay",
            "webcam",
            "chatOverlay",  # HUDStyle
            "frontCam",
            "overheadCam",
            "handCam",
            "detailCam",  # PerformanceMultiCamLayout
            "hostStrip",
            "backgroundContent",  # FocusStrip
            "mainContent",
            "pipContent",  # PiPLayout
            "topContent",
            "bottomContent",
            "captionBar",  # VerticalLayout
            "milestones",
            "clips",  # TimelineLayout, MosaicLayout
            "content",  # Container
            "leftPanel",
            "rightPanel",
            "topPanel",
            "bottomPanel",  # SplitScreen
        ]
        props_lines = []
        for key, value in comp.props.items():
            if key not in exclude_keys and value is not None:
                props_lines.append(f"{spaces}  {key}={self._format_prop_value(value)}")
        props_str = "\n".join(props_lines) if props_lines else ""

        # Render children based on component type
        if comp.component_type == "Grid":
            children = comp.props.get("children", [])
            if isinstance(children, list):
                children_jsx = []
                for child in children:
                    if isinstance(child, ComponentInstance):
                        child_jsx = self._render_component_jsx(child, indent + 4)
                        children_jsx.append(child_jsx)
                # Join with commas for JSX array
                children_str = ",\n".join(children_jsx)
            else:
                children_str = ""

            if props_str:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}>
{spaces}  {{[
{children_str}
{spaces}  ]}}
{spaces}</{comp.component_type}>"""
            else:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}>
{spaces}  {{[
{children_str}
{spaces}  ]}}
{spaces}</{comp.component_type}>"""

        elif comp.component_type == "Container":
            child = comp.props.get("children")
            if isinstance(child, ComponentInstance):
                child_jsx = self._render_component_jsx(child, indent + 4)
            else:
                child_jsx = ""

            if props_str:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}>
{child_jsx}
{spaces}</{comp.component_type}>"""
            else:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}>
{child_jsx}
{spaces}</{comp.component_type}>"""

        elif comp.component_type == "SplitScreen":
            # Render left/right or top/bottom based on direction
            direction = comp.props.get("direction", "horizontal")
            if direction == "horizontal":
                left = comp.props.get("left")
                right = comp.props.get("right")
                left_jsx = (
                    self._render_component_jsx(left, indent + 4)
                    if isinstance(left, ComponentInstance)
                    else ""
                )
                right_jsx = (
                    self._render_component_jsx(right, indent + 4)
                    if isinstance(right, ComponentInstance)
                    else ""
                )

                if props_str:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}  left={{
{left_jsx}
{spaces}  }}
{spaces}  right={{
{right_jsx}
{spaces}  }}
{spaces}/>"""
                else:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}  left={{
{left_jsx}
{spaces}  }}
{spaces}  right={{
{right_jsx}
{spaces}  }}
{spaces}/>"""
            else:  # vertical
                top = comp.props.get("top")
                bottom = comp.props.get("bottom")
                top_jsx = (
                    self._render_component_jsx(top, indent + 4)
                    if isinstance(top, ComponentInstance)
                    else ""
                )
                bottom_jsx = (
                    self._render_component_jsx(bottom, indent + 4)
                    if isinstance(bottom, ComponentInstance)
                    else ""
                )

                if props_str:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}  top={{
{top_jsx}
{spaces}  }}
{spaces}  bottom={{
{bottom_jsx}
{spaces}  }}
{spaces}/>"""
                else:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}  top={{
{top_jsx}
{spaces}  }}
{spaces}  bottom={{
{bottom_jsx}
{spaces}  }}
{spaces}/>"""

        # Handle specialized layouts (OverTheShoulder, DialogueFrame, ThreeColumn, ThreeRow, Asymmetric, etc.)
        elif comp.component_type in [
            "OverTheShoulderLayout",
            "DialogueFrameLayout",
            "StackedReactionLayout",
            "HUDStyleLayout",
            "PerformanceMultiCamLayout",
            "FocusStripLayout",
            "ThreeColumnLayout",
            "ThreeRowLayout",
            "AsymmetricLayout",
            "ThreeByThreeGrid",
            "PiPLayout",
            "VerticalLayout",
            "TimelineLayout",
            "MosaicLayout",
        ]:
            # Map layout types to their prop keys
            layout_prop_keys = {
                "OverTheShoulderLayout": ["hostView", "screenContent"],
                "DialogueFrameLayout": ["characterA", "characterB"],
                "StackedReactionLayout": ["originalClip", "reactorFace"],
                "HUDStyleLayout": ["gameplay", "webcam", "chatOverlay"],
                "PerformanceMultiCamLayout": ["frontCam", "overheadCam", "handCam", "detailCam"],
                "FocusStripLayout": ["hostStrip", "backgroundContent"],
                "ThreeColumnLayout": ["left", "center", "right"],
                "ThreeRowLayout": ["top", "middle", "bottom"],
                "AsymmetricLayout": ["mainFeed", "demo1", "demo2", "overlay"],
                "ThreeByThreeGrid": ["children"],
                "PiPLayout": ["mainContent", "pipContent"],
                "VerticalLayout": ["topContent", "bottomContent", "captionBar"],
                "TimelineLayout": ["mainContent", "milestones"],
                "MosaicLayout": ["children"],
            }

            prop_keys = layout_prop_keys.get(comp.component_type, [])
            child_props = []

            for key in prop_keys:
                child = comp.props.get(key)
                if isinstance(child, ComponentInstance):
                    child_jsx = self._render_component_jsx(child, indent + 4)
                    child_props.append(f"{spaces}  {key}={{\n{child_jsx}\n{spaces}  }}")
                elif isinstance(child, list) and key == "children":
                    # Handle array of children (e.g., ThreeByThreeGrid)
                    children_jsx = []
                    for child_item in child:
                        if isinstance(child_item, ComponentInstance):
                            child_jsx = self._render_component_jsx(child_item, indent + 4)
                            children_jsx.append(child_jsx)
                    children_str = ",\n".join(children_jsx)
                    child_props.append(f"{spaces}  {key}={{[\n{children_str}\n{spaces}  ]}}")
                elif child is None:
                    # Only add undefined for optional child props
                    pass  # Don't render undefined props

            children_str = "\n".join(child_props)

            if props_str:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{children_str}
{spaces}/>"""
            else:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{children_str}
{spaces}/>"""

        # Fallback
        return self._render_simple_component(comp, indent)

    def _format_prop_value(self, value: Any) -> str:
        """Format a prop value for JSX."""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "{" + str(value).lower() + "}"
        elif isinstance(value, (int, float)):
            return "{" + str(value) + "}"
        elif isinstance(value, dict):
            # Format dict as JS object literal
            import json

            return "{" + json.dumps(value) + "}"
        elif isinstance(value, list):
            # Format list as JS array
            import json

            return "{" + json.dumps(value) + "}"
        else:
            return f"{{{value}}}"

    def to_dict(self) -> dict[str, Any]:
        """
        Export composition as dictionary.

        Returns:
            Dictionary representation of the composition
        """
        return {
            "fps": self.fps,
            "width": self.width,
            "height": self.height,
            "theme": self.theme,
            "duration_frames": self.get_total_duration_frames(),
            "duration_seconds": self.get_total_duration_seconds(),
            "components": [
                {
                    "type": c.component_type,
                    "start_frame": c.start_frame,
                    "duration_frames": c.duration_frames,
                    "start_time": self.frames_to_seconds(c.start_frame),
                    "duration": self.frames_to_seconds(c.duration_frames),
                    "layer": c.layer,
                    "props": c.props,
                }
                for c in self.components
            ],
        }
