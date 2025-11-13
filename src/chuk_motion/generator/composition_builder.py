"""
Composition Builder - Combines components into complete video compositions.

Manages the timeline, layering, and sequencing of video components.

## Dynamic Builder Methods

All component builder methods (add_line_chart, add_code_block, etc.) are
dynamically registered at runtime by discover_components() and
register_all_builders() in src/chuk_motion/components/__init__.py.

Each component directory (e.g., src/chuk_motion/components/charts/LineChart/)
contains a builder.py file with an add_to_composition() function. These
functions are automatically discovered and converted into methods on the
CompositionBuilder class.

This design ensures:
- Single source of truth: Component logic lives only in component/builder.py
- Automatic discovery: New components are automatically available
- Consistency: All components follow the same pattern
- Maintainability: Update one place, not multiple files

Usage:
    from chuk_motion.generator.composition_builder import CompositionBuilder
    from chuk_motion.components import register_all_builders

    # Register all component builder methods
    register_all_builders(CompositionBuilder)

    # Create composition and use dynamically added methods
    builder = CompositionBuilder(fps=30)
    builder.add_title_scene(text="Hello", duration_seconds=3.0)
    builder.add_line_chart(data=[[0,10],[1,20]], start_time=3.0)
"""

from dataclasses import dataclass, field
from typing import Any


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


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

    # Class-level registry for component-specific renderers
    _component_renderers: dict = {}

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

    # =========================================================================
    # COMPONENT BUILDER METHODS ARE DYNAMICALLY ADDED
    # =========================================================================
    #
    # All add_* methods (add_line_chart, add_code_block, etc.) are dynamically
    # registered at runtime by the register_all_builders() function in
    # src/chuk_motion/components/__init__.py
    #
    # This function discovers all components and automatically creates builder
    # methods from each component's builder.py file, ensuring:
    #   - Single source of truth (no duplication)
    #   - Automatic discovery of new components
    #   - Consistency across all components
    #
    # See: src/chuk_motion/components/__init__.py:138-164
    # =========================================================================

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
                "OverTheShoulder",
                "DialogueFrame",
                "StackedReaction",
                "HUDStyle",
                "PerformanceMultiCam",
                "FocusStrip",
                "PiP",
                "Vertical",
                "Timeline",
                "Mosaic",
                # Frame components with content prop
                "BrowserFrame",
                "DeviceFrame",
                "Terminal",
                # Transition components
                "PixelTransition",
                "LayoutTransition",
                # Animation wrapper components
                "LayoutEntrance",
                "PanelCascade",
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
                    "firstContent",
                    "secondContent",  # PixelTransition
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
            "OverTheShoulder",
            "DialogueFrame",
            "StackedReaction",
            "PixelTransition",
            "LayoutTransition",
            "HUDStyle",
            "PerformanceMultiCam",
            "FocusStrip",
            "PiP",
            "Vertical",
            "Timeline",
            "Mosaic",
            # Animation wrappers
            "LayoutEntrance",
            "PanelCascade",
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
                    "firstContent",
                    "secondContent",  # PixelTransition
                ]
                for key in specialized_keys:
                    child = comp.props.get(key)
                    if isinstance(child, ComponentInstance):
                        nested.add(id(child))
        return nested

    def _render_component_jsx(self, comp: ComponentInstance, indent: int = 0) -> str:
        """Render a component as JSX, including nested children."""
        # Try component-specific custom renderer FIRST (highest priority)
        custom_jsx = self._try_custom_renderer(comp, indent)
        if custom_jsx is not None:
            return custom_jsx

        # Check if this is a layout component with children
        layout_types = [
            "Grid",
            "Container",
            "SplitScreen",
            "ThreeColumnLayout",
            "ThreeRowLayout",
            "ThreeByThreeGrid",
            "AsymmetricLayout",
            "OverTheShoulder",
            "DialogueFrame",
            "StackedReaction",
            "HUDStyle",
            "PerformanceMultiCam",
            "FocusStrip",
            "PiP",
            "Vertical",
            "Timeline",
            "Mosaic",
            # Frame components with content prop
            "BrowserFrame",
            "DeviceFrame",
            "Terminal",
            # Transition components
            "PixelTransition",
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
        # Convert snake_case keys to camelCase for TypeScript
        props_lines = []
        for key, value in comp.props.items():
            if key not in ["children", "left", "right", "top", "bottom"] and value is not None:
                camel_key = snake_to_camel(key)
                props_lines.append(f"{spaces}  {camel_key}={self._format_prop_value(value)}")
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
        # Exclude child component props from regular props (using snake_case names to match templates)
        exclude_keys = [
            "children",
            "left",
            "right",
            "top",
            "bottom",
            "center",
            "middle",
            # AsymmetricLayout
            "main",
            "top_side",
            "bottom_side",
            # OverTheShoulder
            "screen_content",
            "shoulder_overlay",
            # DialogueFrame
            "left_speaker",
            "right_speaker",
            "center_content",
            # StackedReaction
            "original_content",
            "reaction_content",
            # HUDStyle
            "main_content",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
            # PerformanceMultiCam
            "primary_cam",
            "secondary_cams",
            # FocusStrip
            "focus_content",
            # PiP
            "mainContent",
            "pipContent",
            # Vertical
            "topContent",
            "bottomContent",
            "captionBar",
            # Timeline / Mosaic
            "clips",
            # Container
            "content",
            # PixelTransition
            "firstContent",
            "secondContent",
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
            children = comp.props.get("children")
            # Handle single child or array of children
            if isinstance(children, ComponentInstance):
                child_jsx = self._render_component_jsx(children, indent + 4)
            elif isinstance(children, list) and len(children) > 0:
                # If array with single item, render it directly
                if len(children) == 1 and isinstance(children[0], ComponentInstance):
                    child_jsx = self._render_component_jsx(children[0], indent + 4)
                else:
                    # Multiple children - render them all
                    children_jsxs = []
                    for child_item in children:
                        if isinstance(child_item, ComponentInstance):
                            children_jsxs.append(self._render_component_jsx(child_item, indent + 4))
                    child_jsx = "\n".join(children_jsxs)
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
            "OverTheShoulder",
            "DialogueFrame",
            "StackedReaction",
            "HUDStyle",
            "PerformanceMultiCam",
            "FocusStrip",
            "ThreeColumnLayout",
            "ThreeRowLayout",
            "AsymmetricLayout",
            "ThreeByThreeGrid",
            "PiP",
            "Vertical",
            "Timeline",
            "Mosaic",
        ]:
            # Map layout types to their prop keys (using snake_case names to match templates)
            layout_prop_keys = {
                "OverTheShoulder": ["screen_content", "shoulder_overlay"],
                "DialogueFrame": ["left_speaker", "center_content", "right_speaker"],
                "StackedReaction": ["original_content", "reaction_content"],
                "HUDStyle": [
                    "main_content",
                    "top_left",
                    "top_right",
                    "bottom_left",
                    "bottom_right",
                ],
                "PerformanceMultiCam": ["primary_cam", "secondary_cams"],
                "FocusStrip": ["main_content", "focus_content"],
                "ThreeColumnLayout": ["left", "center", "right"],
                "ThreeRowLayout": ["top", "middle", "bottom"],
                "AsymmetricLayout": ["main", "top_side", "bottom_side"],
                "ThreeByThreeGrid": ["children"],
                "PiP": ["mainContent", "pipContent"],
                "Vertical": ["top", "bottom"],
                "Timeline": ["main_content"],
                "Mosaic": ["clips"],
            }

            prop_keys = layout_prop_keys.get(comp.component_type, [])
            child_props = []

            for key in prop_keys:
                child = comp.props.get(key)
                if isinstance(child, ComponentInstance):
                    child_jsx = self._render_component_jsx(child, indent + 4)
                    child_props.append(f"{spaces}  {key}={{\n{child_jsx}\n{spaces}  }}")
                elif isinstance(child, list):
                    # Handle array of children (e.g., ThreeByThreeGrid, secondary_cams, clips)
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

        # Handle frame components (BrowserFrame, DeviceFrame, Terminal)
        elif comp.component_type in ["BrowserFrame", "DeviceFrame", "Terminal"]:
            content = comp.props.get("content")
            if isinstance(content, ComponentInstance):
                content_jsx = self._render_component_jsx(content, indent + 4)
                if props_str:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}  content={{
{content_jsx}
{spaces}  }}
{spaces}/>"""
                else:
                    return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}  content={{
{content_jsx}
{spaces}  }}
{spaces}/>"""
            else:
                # No content, render as simple component
                return self._render_simple_component(comp, indent)

        # Handle transition components (PixelTransition)
        elif comp.component_type == "PixelTransition":
            first_content = comp.props.get("firstContent")
            second_content = comp.props.get("secondContent")

            first_jsx = (
                self._render_component_jsx(first_content, indent + 4)
                if isinstance(first_content, ComponentInstance)
                else ""
            )
            second_jsx = (
                self._render_component_jsx(second_content, indent + 4)
                if isinstance(second_content, ComponentInstance)
                else ""
            )

            if props_str:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}  firstContent={{
{first_jsx}
{spaces}  }}
{spaces}  secondContent={{
{second_jsx}
{spaces}  }}
{spaces}/>"""
            else:
                return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}  firstContent={{
{first_jsx}
{spaces}  }}
{spaces}  secondContent={{
{second_jsx}
{spaces}  }}
{spaces}/>"""

        # Fallback to default rendering
        return self._render_simple_component(comp, indent)

    def _try_custom_renderer(self, comp: ComponentInstance, indent: int) -> str | None:
        """Try to use a component-specific custom renderer if available."""
        # Check if this component has a custom renderer
        renderer = self._component_renderers.get(comp.component_type)
        if renderer:
            try:
                return renderer(comp, self._render_component_jsx, indent, snake_to_camel, self._format_prop_value)
            except Exception as e:
                print(f"Warning: Custom renderer for {comp.component_type} failed: {e}")
                return None
        return None

    def _serialize_value(self, value: Any) -> Any:
        """Recursively serialize values to JSON-compatible types."""
        from dataclasses import asdict, is_dataclass

        from pydantic import BaseModel

        if isinstance(value, BaseModel):
            # Recursively serialize Pydantic models using model_dump
            try:
                dumped = value.model_dump(mode="python")
                # Recursively process the dumped dict in case it contains more BaseModels
                return self._serialize_value(dumped)
            except Exception as e:
                print(f"Warning: Could not serialize {type(value).__name__}: {e}")
                # Fallback: try to convert to dict manually
                return str(value)
        elif is_dataclass(value) and not isinstance(value, type):
            # Handle dataclasses (like ComponentInstance)
            dumped = asdict(value)
            # Recursively process the dumped dict
            return self._serialize_value(dumped)
        elif isinstance(value, dict):
            # Recursively serialize dict values
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # Recursively serialize list items
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, tuple):
            # Convert tuples to lists
            return [self._serialize_value(item) for item in value]
        else:
            # Return primitive types as-is
            return value

    def _format_prop_value(self, value: Any) -> str:
        """Format a prop value for JSX."""
        import json

        if isinstance(value, str):
            # Use template literals for strings (supports multiline and quotes)
            # Escape backticks and ${} in the string
            escaped = value.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
            return "{`" + escaped + "`}"
        elif isinstance(value, bool):
            return "{" + str(value).lower() + "}"
        elif isinstance(value, (int, float)):
            return "{" + str(value) + "}"
        elif isinstance(value, (dict, list)) or hasattr(value, "model_dump"):
            # Serialize complex types (dicts, lists, Pydantic models)
            serialized = self._serialize_value(value)
            try:
                return "{" + json.dumps(serialized) + "}"
            except TypeError:
                # Debug: print what failed
                print(f"DEBUG: Failed to serialize value of type {type(value)}")
                print(f"DEBUG: Serialized type: {type(serialized)}")
                print(f"DEBUG: Serialized value: {serialized}")
                raise
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
