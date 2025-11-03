#!/usr/bin/env python3
"""
Script to migrate remaining charts to the new modular Pydantic structure.

Migrates: BarChart, HorizontalBarChart, AreaChart, PieChart, DonutChart
"""

from pathlib import Path
import shutil
import json

# Chart definitions with their specific properties
CHARTS = {
    "BarChart": {
        "description": "Animated vertical bar chart for comparing categories",
        "props": {
            "data": "List of objects with label, value, and optional color",
            "title": "Optional chart title",
            "xlabel": "Optional x-axis label",
            "ylabel": "Optional y-axis label",
            "start_time": "When to show (seconds)",
            "duration": "How long to animate (seconds)",
        },
        "data_model": "BarDataPoint",
        "data_type": "List[BarDataPoint]",
        "example": [
            {"label": "Q1", "value": 45},
            {"label": "Q2", "value": 67},
        ],
    },
    "HorizontalBarChart": {
        "description": "Animated horizontal bar chart perfect for rankings with rank badges",
        "props": {
            "data": "List of objects with label, value, and optional color",
            "title": "Optional chart title",
            "xlabel": "Optional x-axis label",
            "start_time": "When to show (seconds)",
            "duration": "How long to animate (seconds)",
        },
        "data_model": "BarDataPoint",
        "data_type": "List[BarDataPoint]",
        "example": [
            {"label": "Comté", "value": 95},
            {"label": "Roquefort", "value": 90},
        ],
    },
    "AreaChart": {
        "description": "Animated area chart showing trends with filled gradient",
        "props": {
            "data": "Array of data points as [x, y] or {x, y, label}",
            "title": "Optional chart title",
            "xlabel": "Optional x-axis label",
            "ylabel": "Optional y-axis label",
            "start_time": "When to show (seconds)",
            "duration": "How long to animate (seconds)",
        },
        "data_model": "DataPoint",
        "data_type": "List[Union[List[float], DataPoint]]",
        "example": [[0, 10], [1, 25], [2, 45]],
    },
    "PieChart": {
        "description": "Animated pie chart for showing proportions and percentages",
        "props": {
            "data": "List of objects with label, value, and optional color",
            "title": "Optional chart title",
            "start_time": "When to show (seconds)",
            "duration": "How long to animate (seconds)",
        },
        "data_model": "PieDataPoint",
        "data_type": "List[PieDataPoint]",
        "example": [
            {"label": "Desktop", "value": 45},
            {"label": "Mobile", "value": 35},
        ],
    },
    "DonutChart": {
        "description": "Animated donut chart with center text for showing proportions",
        "props": {
            "data": "List of objects with label, value, and optional color",
            "title": "Optional chart title",
            "center_text": "Text to display in center",
            "start_time": "When to show (seconds)",
            "duration": "How long to animate (seconds)",
        },
        "data_model": "DonutDataPoint",
        "data_type": "List[DonutDataPoint]",
        "example": [
            {"label": "Complete", "value": 75},
            {"label": "In Progress", "value": 15},
        ],
    },
}


def create_schema_py(chart_name: str, chart_info: dict) -> str:
    """Generate schema.py content for a chart."""

    # Determine data point model
    if chart_info["data_model"] == "DataPoint":
        data_point_class = '''class DataPoint(BaseModel):
    """A single data point with x, y coordinates and optional label."""
    x: float
    y: float
    label: Optional[str] = None'''
    elif chart_info["data_model"] in ("BarDataPoint", "PieDataPoint", "DonutDataPoint"):
        data_point_class = f'''class {chart_info["data_model"]}(BaseModel):
    """A single data point with label and value."""
    label: str
    value: float
    color: Optional[str] = None'''
    else:
        data_point_class = ""

    # Build props fields
    props_fields = []
    for prop_name, prop_desc in chart_info["props"].items():
        if prop_name == "data":
            props_fields.append(f'    data: {chart_info["data_type"]} = Field(\n        description="{prop_desc}"\n    )')
        elif prop_name == "center_text":
            props_fields.append(f'    center_text: Optional[str] = Field(None, description="{prop_desc}")')
        elif prop_name in ("title", "xlabel", "ylabel"):
            props_fields.append(f'    {prop_name}: Optional[str] = Field(None, description="{prop_desc}")')
        elif prop_name == "start_time":
            props_fields.append(f'    start_time: float = Field(0.0, description="{prop_desc}")')
        elif prop_name == "duration":
            props_fields.append(f'    duration: float = Field(4.0, description="{prop_desc}")')

    props_class = f'''class {chart_name}Props(BaseModel):
    """Properties for {chart_name} component."""

{chr(10).join(props_fields)}

    class Config:
        extra = "forbid"'''

    return f'''"""{ chart_name} component schema and Pydantic models."""

from typing import List, Optional, Union
from pydantic import BaseModel, Field

from ...base import ComponentMetadata


{data_point_class}


{props_class}


# Component metadata
METADATA = ComponentMetadata(
    name="{chart_name}",
    description="{chart_info['description']}",
    category="chart"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {{
    "description": METADATA.description,
    "category": METADATA.category,
    "animations": {{
        "draw": "Chart draws with animation",
        "fade_in": "Chart fades in",
        "scale_in": "Chart scales from center"
    }},
    "schema": {{
        {_generate_mcp_schema_fields(chart_info["props"])}
    }},
    "example": {chart_info["example"]}
}}
'''


def _generate_mcp_schema_fields(props: dict) -> str:
    """Generate MCP schema fields."""
    fields = []
    for prop_name, prop_desc in props.items():
        if prop_name == "data":
            fields.append(f'''        "data": {{
            "type": "array",
            "required": True,
            "description": "{prop_desc}"
        }}''')
        elif prop_name in ("title", "xlabel", "ylabel", "center_text"):
            fields.append(f'''        "{prop_name}": {{
            "type": "string",
            "default": "",
            "description": "{prop_desc}"
        }}''')
        elif prop_name in ("start_time", "duration"):
            default = "0.0" if prop_name == "start_time" else "4.0"
            fields.append(f'''        "{prop_name}": {{
            "type": "float",
            "required": True,
            "description": "{prop_desc}"
        }}''')
    return ",\n".join(fields)


def create_tool_py(chart_name: str, chart_info: dict) -> str:
    """Generate tool.py content for a chart."""

    # Build function parameters
    params = ["data: str"]
    for prop_name in chart_info["props"].keys():
        if prop_name == "data":
            continue
        elif prop_name in ("title", "xlabel", "ylabel", "center_text"):
            params.append(f"{prop_name}: Optional[str] = None")
        elif prop_name == "start_time":
            params.append("start_time: float = 0.0")
        elif prop_name == "duration":
            default = "5.0" if "Horizontal" in chart_name else "4.0"
            params.append(f"duration: float = {default}")

    # Build method call parameters
    call_params = []
    for prop_name in chart_info["props"].keys():
        if prop_name == "data":
            call_params.append("data=data_parsed")
        else:
            call_params.append(f"{prop_name}={prop_name}")

    # Build result dict fields
    result_fields = [
        '"component": "' + chart_name + '"',
        '"data_points": len(data_parsed)',
        '"start_time": start_time',
        '"duration": duration'
    ]
    if "title" in chart_info["props"]:
        result_fields.insert(2, '"title": title')

    method_name = _camel_to_snake(chart_name)

    params_joined = ",\n        ".join(params)
    call_params_joined = ",\n                ".join(call_params)
    result_fields_joined = ",\n                ".join(result_fields)
    tool_args_doc = _generate_tool_args_doc(chart_info["props"])
    example_json = json.dumps(chart_info["example"])
    chart_desc = chart_info["description"]

    return f'''"""{chart_name} MCP tool."""

import asyncio
import json
from typing import Optional


def register_tool(mcp, project_manager):
    """Register the {chart_name} tool with the MCP server."""

    @mcp.tool
    async def remotion_add_{method_name}(
        {params_joined}
    ) -> str:
        """
        Add an animated {chart_name.replace("Chart", " chart").lower()} to the composition.

        {chart_desc}.

        Args:
            data: JSON array of data points
            {tool_args_doc}

        Returns:
            JSON with component info

        Example:
            await remotion_add_{method_name}(
                data='{example_json}',
                title="Example Chart",
                start_time=3.0,
                duration=4.0
            )
        """
        def _add():
            if not project_manager.current_composition:
                return json.dumps({{"error": "No active project. Create a project first."}})

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return json.dumps({{"error": f"Invalid data JSON: {{str(e)}}"}})

            project_manager.current_composition.add_{method_name}(
                {call_params_joined}
            )

            return json.dumps({{
                {result_fields_joined}
            }})

        return await asyncio.get_event_loop().run_in_executor(None, _add)
'''


def _generate_tool_args_doc(props: dict) -> str:
    """Generate tool args documentation."""
    docs = []
    for prop_name, prop_desc in props.items():
        if prop_name != "data":
            docs.append(f"{prop_name}: {prop_desc}")
    return "\n            ".join(docs)


def create_builder_py(chart_name: str, chart_info: dict) -> str:
    """Generate builder.py content for a chart."""

    # Build function parameters
    params = ["data: list"]
    for prop_name in chart_info["props"].keys():
        if prop_name == "data":
            continue
        elif prop_name in ("title", "xlabel", "ylabel", "center_text"):
            params.append(f"{prop_name}: Optional[str] = None")
        elif prop_name == "start_time":
            params.append("start_time: float = 0.0")
        elif prop_name == "duration":
            default = "5.0" if "Horizontal" in chart_name else "4.0"
            params.append(f"duration: float = {default}")

    # Build props dict
    props_dict = ['"data": data']
    for prop_name in chart_info["props"].keys():
        if prop_name == "data":
            continue
        elif prop_name == "center_text":
            props_dict.append('"centerText": center_text')
        else:
            props_dict.append(f'"{prop_name}": {prop_name}')

    params_joined = ",\n    ".join(params)
    props_dict_joined = ",\n            ".join(props_dict)
    builder_args_doc = _generate_builder_args_doc(chart_info["props"])

    return f'''"""{chart_name} composition builder method."""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder, ComponentInstance


def add_to_composition(
    builder: "CompositionBuilder",
    {params_joined}
) -> "CompositionBuilder":
    """
    Add an animated {chart_name.replace("Chart", " chart").lower()} to the composition.

    Args:
        builder: CompositionBuilder instance
        {builder_args_doc}

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    component = ComponentInstance(
        component_type="{chart_name}",
        start_frame=builder.seconds_to_frames(start_time),
        duration_frames=builder.seconds_to_frames(duration),
        props={{
            {props_dict_joined}
        }},
        layer=5
    )
    builder.components.append(component)
    return builder
'''


def _generate_builder_args_doc(props: dict) -> str:
    """Generate builder args documentation."""
    docs = []
    for prop_name, prop_desc in props.items():
        docs.append(f"{prop_name}: {prop_desc}")
    return "\n        ".join(docs)


def create_init_py(chart_name: str, chart_info: dict) -> str:
    """Generate __init__.py content for a chart."""

    data_model = chart_info["data_model"]

    return f'''"""{chart_name} component."""

from .schema import METADATA, MCP_SCHEMA, {chart_name}Props, {data_model}
from .tool import register_tool
from .builder import add_to_composition

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "{chart_name}Props",
    "{data_model}",
    "register_tool",
    "add_to_composition"
]
'''


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def migrate_chart(chart_name: str, chart_info: dict, base_path: Path):
    """Migrate a single chart to the new structure."""

    chart_dir = base_path / "src" / "chuk_mcp_remotion" / "components" / "charts" / chart_name
    chart_dir.mkdir(parents=True, exist_ok=True)

    print(f"Migrating {chart_name}...")

    # Create schema.py
    schema_content = create_schema_py(chart_name, chart_info)
    (chart_dir / "schema.py").write_text(schema_content)

    # Create tool.py
    tool_content = create_tool_py(chart_name, chart_info)
    (chart_dir / "tool.py").write_text(tool_content)

    # Create builder.py
    builder_content = create_builder_py(chart_name, chart_info)
    (chart_dir / "builder.py").write_text(builder_content)

    # Create __init__.py
    init_content = create_init_py(chart_name, chart_info)
    (chart_dir / "__init__.py").write_text(init_content)

    # Copy template if it exists
    old_template = base_path / "src" / "chuk_mcp_remotion" / "generator" / "templates" / "content" / f"{chart_name}.tsx.j2"
    new_template = chart_dir / "template.tsx.j2"

    if old_template.exists():
        shutil.copy(old_template, new_template)
        print(f"  ✓ Copied template")
    else:
        print(f"  ⚠ Template not found: {old_template}")

    print(f"  ✓ Created schema.py, tool.py, builder.py, __init__.py")


def main():
    """Run the migration."""
    base_path = Path(__file__).parent

    print("=" * 60)
    print("Migrating charts to modular Pydantic structure")
    print("=" * 60)

    for chart_name, chart_info in CHARTS.items():
        migrate_chart(chart_name, chart_info, base_path)
        print()

    print("=" * 60)
    print(f"Migration complete! Migrated {len(CHARTS)} charts.")
    print("=" * 60)


if __name__ == "__main__":
    main()
