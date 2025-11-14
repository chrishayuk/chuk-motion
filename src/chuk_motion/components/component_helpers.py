"""Shared helper functions for component tools."""

from chuk_motion.generator.composition_builder import ComponentInstance


def parse_nested_component(comp_dict):
    """
    Recursively convert nested component dicts to ComponentInstance objects.

    Handles arbitrarily deep nesting of components, such as:
    - ThreeColumnLayout containing VideoContent components
    - FocusStrip containing ThreeColumnLayout containing VideoContent
    - Grid containing multiple VideoContent components

    Args:
        comp_dict: Dictionary in format {"type": "ComponentName", "config": {...}}
                  or None or non-dict value

    Returns:
        ComponentInstance if comp_dict is a valid component dict,
        otherwise returns comp_dict as-is
    """
    if comp_dict is None:
        return None
    if not isinstance(comp_dict, dict):
        return comp_dict

    # Check for proper format: {"type": "X", "config": {...}}
    if "type" in comp_dict:
        config = comp_dict.get("config", {})

        # Recursively parse nested components in config
        parsed_config = {}
        for key, value in config.items():
            if isinstance(value, dict) and "type" in value:
                # Recursive nested component
                parsed_config[key] = parse_nested_component(value)
            elif isinstance(value, list):
                # Array of possibly nested components
                parsed_config[key] = [
                    parse_nested_component(item)
                    if isinstance(item, dict) and "type" in item
                    else item
                    for item in value
                ]
            else:
                parsed_config[key] = value

        return ComponentInstance(
            component_type=comp_dict["type"],
            start_frame=0,
            duration_frames=0,
            props=parsed_config,
            layer=5,
        )
    # If it's already a valid component dict without "type", return as-is
    return comp_dict
