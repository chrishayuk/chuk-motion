"""
LayoutEntrance JSX renderer.

Provides custom JSX rendering for LayoutEntrance component with nested children.
"""


def render_jsx(comp, render_child_fn, indent, snake_to_camel, format_prop_value):
    """
    Render LayoutEntrance component as JSX with nested child content.

    Args:
        comp: ComponentInstance to render
        render_child_fn: Function to recursively render child components
        indent: Current indentation level
        snake_to_camel: Function to convert snake_case to camelCase
        format_prop_value: Function to format prop values for JSX

    Returns:
        JSX string for the component, or None to use default rendering
    """
    spaces = " " * indent
    content = comp.props.get("content")

    # If no content or content is not a ComponentInstance, use default rendering
    if not content or not hasattr(content, "component_type"):
        return None

    # Format non-content props
    exclude_keys = ["content", "children"]
    props_lines = []
    for key, value in comp.props.items():
        if key not in exclude_keys and value is not None:
            camel_key = snake_to_camel(key)
            props_lines.append(f"{spaces}  {camel_key}={format_prop_value(value)}")
    props_str = "\n".join(props_lines) if props_lines else ""

    # Render the nested content
    content_jsx = render_child_fn(content, indent + 4)

    # Build JSX
    if props_str:
        return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}>
{content_jsx}
{spaces}</{comp.component_type}>"""
    else:
        return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}>
{content_jsx}
{spaces}</{comp.component_type}>"""
