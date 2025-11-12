#!/usr/bin/env python3
"""
Script to generate layout component boilerplate following the new pattern.
"""
import os
import json

# Layout definitions
LAYOUTS = {
    "ThreeRowLayout": {
        "description": "Header + Main + Footer arrangements with configurable heights",
        "tool_name": "remotion_add_three_row_layout",
        "props": {
            "top": {"type": "component", "default": None, "description": "Content for top row"},
            "middle": {"type": "component", "default": None, "description": "Content for middle row"},
            "bottom": {"type": "component", "default": None, "description": "Content for bottom row"},
            "top_height": {"type": "number", "default": 25, "description": "Top row height (percentage)"},
            "middle_height": {"type": "number", "default": 50, "description": "Middle row height (percentage)"},
            "bottom_height": {"type": "number", "default": 25, "description": "Bottom row height (percentage)"},
            "gap": {"type": "number", "default": 20, "description": "Gap between rows (pixels)"},
            "padding": {"type": "number", "default": 40, "description": "Padding around layout (pixels)"},
        },
        "template_type": "three_row"
    },
    "AsymmetricLayout": {
        "description": "Main feed (2/3) + two demo panels (1/3 stacked) - perfect for tutorials",
        "tool_name": "remotion_add_asymmetric_layout",
        "props": {
            "main": {"type": "component", "default": None, "description": "Main content (left 2/3)"},
            "top_side": {"type": "component", "default": None, "description": "Top sidebar content"},
            "bottom_side": {"type": "component", "default": None, "description": "Bottom sidebar content"},
            "main_width": {"type": "number", "default": 66.67, "description": "Main content width (percentage)"},
            "gap": {"type": "number", "default": 20, "description": "Gap between panels (pixels)"},
            "padding": {"type": "number", "default": 40, "description": "Padding around layout (pixels)"},
        },
        "template_type": "asymmetric"
    },
    "PiP": {
        "description": "Picture-in-Picture webcam overlay with customizable positions",
        "tool_name": "remotion_add_pip",
        "props": {
            "main": {"type": "component", "default": None, "description": "Main content"},
            "overlay": {"type": "component", "default": None, "description": "PiP overlay content"},
            "position": {"type": "enum", "default": "bottom-right", "values": ["bottom-right", "bottom-left", "top-right", "top-left"], "description": "Overlay position"},
            "overlay_size": {"type": "number", "default": 20, "description": "Overlay size (percentage of screen)"},
            "margin": {"type": "number", "default": 40, "description": "Margin from edges (pixels)"},
        },
        "template_type": "pip"
    },
    "Vertical": {
        "description": "9:16 optimized for Shorts/TikTok/Reels with multiple layout styles",
        "tool_name": "remotion_add_vertical",
        "props": {
            "top": {"type": "component", "default": None, "description": "Top content"},
            "bottom": {"type": "component", "default": None, "description": "Bottom content"},
            "layout_style": {"type": "enum", "default": "top-bottom", "values": ["top-bottom", "caption-content", "content-caption", "split-vertical"], "description": "Vertical layout style"},
            "gap": {"type": "number", "default": 20, "description": "Gap between sections (pixels)"},
            "padding": {"type": "number", "default": 40, "description": "Padding around layout (pixels)"},
        },
        "template_type": "vertical"
    },
}


def create_schema_file(component_name, config):
    """Generate schema.py file."""
    props_class = f"{component_name}Props"

    # Build Pydantic fields
    pydantic_fields = []
    for prop_name, prop_config in config["props"].items():
        prop_type = prop_config["type"]
        default = prop_config.get("default")
        description = prop_config["description"]

        if prop_type == "component":
            type_hint = "Any | None"
            field_default = "None"
        elif prop_type == "number":
            type_hint = "float | None"
            field_default = str(default) if default is not None else "None"
        elif prop_type == "enum":
            type_hint = "str | None"
            field_default = f'"{default}"' if default else "None"
        else:
            type_hint = "Any | None"
            field_default = "None"

        pydantic_fields.append(
            f'    {prop_name}: {type_hint} = Field({field_default}, description="{description}")'
        )

    # Add standard timing fields
    pydantic_fields.append('    start_time: float = Field(description="When to show (seconds)")')
    pydantic_fields.append('    duration: float | None = Field(5.0, description="How long to show (seconds)")')

    content = f'''# chuk-motion/src/chuk_motion/components/layouts/{component_name}/schema.py
"""{component_name} component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class {props_class}(BaseModel):
    """Properties for {component_name} component."""

{chr(10).join(pydantic_fields)}

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="{component_name}",
    description="{config['description']}",
    category="layout",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {{
    "description": "{config['description']}",
    "category": "layout",
    "schema": {{
        # Add schema details here
    }},
}}
'''
    return content


def create_builder_file(component_name, config):
    """Generate builder.py file."""
    # Build parameter list
    params = ["builder: \"CompositionBuilder\""]
    for prop_name, prop_config in config["props"].items():
        default = prop_config.get("default")
        if prop_config["type"] == "component":
            params.append(f'{prop_name}: Any | None = None')
        elif prop_config["type"] == "number":
            params.append(f'{prop_name}: float = {default}')
        elif prop_config["type"] == "enum":
            params.append(f'{prop_name}: str = "{default}"')

    params.append("start_time: float")
    params.append("duration: float = 5.0")

    # Build props dict
    props_items = [f'"{k}": {k}' for k in config["props"].keys()]
    props_items.extend(['"start_time": start_time', '"duration": duration'])

    content = f'''# chuk-motion/src/chuk_motion/components/layouts/{component_name}/builder.py
"""{component_name} composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    {(",\n    ").join(params)}
) -> "CompositionBuilder":
    """
    Add {component_name} to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="{component_name}",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={{
            {", ".join(props_items)}
        }},
        layer=0,
    )
    builder.components.append(component)
    return builder
'''
    return content


def create_tool_file(component_name, config):
    """Generate tool.py file."""
    tool_name = config["tool_name"]

    # Build parameters
    params = []
    for prop_name, prop_config in config["props"].items():
        if prop_config["type"] == "component":
            params.append(f'{prop_name}: str | None = None')
        elif prop_config["type"] == "number":
            default = prop_config.get("default")
            params.append(f'{prop_name}: float = {default}')
        elif prop_config["type"] == "enum":
            default = prop_config.get("default")
            params.append(f'{prop_name}: str = "{default}"')

    params.extend([
        'duration: float | str = 5.0',
        'track: str = "main"',
        'gap_before: float | str | None = None'
    ])

    # Build JSON parsing
    json_parsing = []
    for prop_name, prop_config in config["props"].items():
        if prop_config["type"] == "component":
            json_parsing.append(f'                {prop_name}_parsed = json.loads({prop_name}) if {prop_name} else None')

    # Build props dict
    props_items = []
    for prop_name, prop_config in config["props"].items():
        if prop_config["type"] == "component":
            props_items.append(f'                        "{prop_name}": {prop_name}_parsed')
        else:
            props_items.append(f'                        "{prop_name}": {prop_name}')

    content = f'''# chuk-motion/src/chuk_motion/components/layouts/{component_name}/tool.py
"""{component_name} MCP tool."""

import asyncio
import json

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the {component_name} tool with the MCP server."""

    @mcp.tool
    async def {tool_name}(
        {(",\n        ").join(params)}
    ) -> str:
        """
        Add {component_name} to the composition.

        {config['description']}

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
{chr(10).join(json_parsing)}
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {{str(e)}}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="{component_name}",
                    start_frame=0,
                    duration_frames=0,
                    props={{
{(",\n").join(props_items)}
                    }},
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="{component_name}",
                    layout="custom",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
'''
    return content


def create_init_file(component_name):
    """Generate __init__.py file."""
    props_class = f"{component_name}Props"
    content = f'''"""{component_name} component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, {props_class}
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "{props_class}",
    "register_tool",
    "add_to_composition",
]
'''
    return content


def main():
    base_path = "src/chuk_motion/components/layouts"

    for component_name, config in LAYOUTS.items():
        component_path = os.path.join(base_path, component_name)
        os.makedirs(component_path, exist_ok=True)

        print(f"Creating {component_name}...")

        # Create schema.py
        with open(os.path.join(component_path, "schema.py"), "w") as f:
            f.write(create_schema_file(component_name, config))

        # Create builder.py
        with open(os.path.join(component_path, "builder.py"), "w") as f:
            f.write(create_builder_file(component_name, config))

        # Create tool.py
        with open(os.path.join(component_path, "builder.py"), "w") as f:
            f.write(create_tool_file(component_name, config))

        # Create __init__.py
        with open(os.path.join(component_path, "__init__.py"), "w") as f:
            f.write(create_init_file(component_name))

        print(f"  ✓ Created {component_name}")

    print("\nAll layouts created successfully!")


if __name__ == "__main__":
    main()
