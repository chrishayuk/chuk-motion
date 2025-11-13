"""
PanelCascade JSX renderer.

Provides custom JSX rendering for PanelCascade component with array of items.
"""


def render_jsx(comp, render_child_fn, indent, snake_to_camel, format_prop_value):
    """
    Render PanelCascade component as JSX with array of panel items.

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
    items = comp.props.get("items", [])

    # If no items or items is not a list, use default rendering
    if not items or not isinstance(items, list):
        return None

    # Format non-items props
    exclude_keys = ["items", "children"]
    props_lines = []
    for key, value in comp.props.items():
        if key not in exclude_keys and value is not None:
            camel_key = snake_to_camel(key)
            props_lines.append(f"{spaces}  {camel_key}={format_prop_value(value)}")
    props_str = "\n".join(props_lines) if props_lines else ""

    # Render each item as JSX
    items_jsx = []
    for item in items:
        if hasattr(item, "component_type"):  # It's a ComponentInstance
            item_jsx = render_child_fn(item, indent + 4)
            items_jsx.append(item_jsx)

    if not items_jsx:  # No valid items to render
        return None

    items_str = ",\n".join(items_jsx)

    # Build JSX
    if props_str:
        return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{props_str}
{spaces}>
{spaces}  {{[
{items_str}
{spaces}  ]}}
{spaces}</{comp.component_type}>"""
    else:
        return f"""{spaces}<{comp.component_type}
{spaces}  startFrame={{{comp.start_frame}}}
{spaces}  durationInFrames={{{comp.duration_frames}}}
{spaces}>
{spaces}  {{[
{items_str}
{spaces}  ]}}
{spaces}</{comp.component_type}>"""
