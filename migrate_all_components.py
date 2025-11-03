#!/usr/bin/env python3
"""
Script to migrate ALL remaining components to the new modular Pydantic structure.

Reads from the existing registry and generates modular components.
"""

from pathlib import Path
import shutil
import json
import sys
import ast

# Read the components registry directly from the file
def load_component_registry():
    """Load COMPONENT_REGISTRY from components.py file."""
    components_file = Path(__file__).parent / "src" / "chuk_mcp_remotion" / "registry" / "components.py"
    content = components_file.read_text()

    # Parse the Python file and extract COMPONENT_REGISTRY
    tree = ast.parse(content)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "COMPONENT_REGISTRY":
                    # Evaluate the dictionary
                    return ast.literal_eval(node.value)
    return {}

COMPONENT_REGISTRY = load_component_registry()


# Components to skip (already migrated)
SKIP_COMPONENTS = {
    "LineChart", "BarChart", "HorizontalBarChart",
    "AreaChart", "PieChart", "DonutChart"
}


def generate_pydantic_props_class(component_name: str, schema: dict) -> str:
    """Generate Pydantic Props class from schema."""
    fields = []

    for prop_name, prop_info in schema.items():
        prop_type = prop_info.get("type", "str")
        required = prop_info.get("required", False)
        default = prop_info.get("default")
        description = prop_info.get("description", "")

        # Map types
        if prop_type == "string":
            py_type = "str"
        elif prop_type == "number" or prop_type == "float":
            py_type = "float"
        elif prop_type == "integer":
            py_type = "int"
        elif prop_type == "boolean":
            py_type = "bool"
        elif prop_type == "array":
            py_type = "List[Any]"
        else:
            py_type = "Any"

        # Make optional if not required
        if not required:
            py_type = f"Optional[{py_type}]"
            if default is None or default == "":
                field_str = f'    {prop_name}: {py_type} = Field(None, description="{description}")'
            else:
                default_repr = repr(default) if isinstance(default, str) else default
                field_str = f'    {prop_name}: {py_type} = Field({default_repr}, description="{description}")'
        else:
            field_str = f'    {prop_name}: {py_type} = Field(description="{description}")'

        fields.append(field_str)

    return "\n".join(fields)


def create_schema_py(component_name: str, component_info: dict) -> str:
    """Generate schema.py content."""

    category = component_info.get("category", "content")
    description = component_info.get("description", "")
    schema = component_info.get("schema", {})

    props_class_body = generate_pydantic_props_class(component_name, schema)

    # Determine imports needed
    imports = ["from typing import Optional, Any, List"]
    imports.append("from pydantic import BaseModel, Field")
    imports.append("from ...base import ComponentMetadata")

    return f'''"""{component_name} component schema and Pydantic models."""

{chr(10).join(imports)}


class {component_name}Props(BaseModel):
    """Properties for {component_name} component."""

{props_class_body}

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="{component_name}",
    description="{description}",
    category="{category}"
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {json.dumps(component_info, indent=4)}
'''


def create_tool_py(component_name: str, component_info: dict) -> str:
    """Generate tool.py content."""

    schema = component_info.get("schema", {})
    description = component_info.get("description", "")

    # Build function parameters
    params = []
    call_params = []

    for prop_name, prop_info in schema.items():
        prop_type = prop_info.get("type", "str")
        required = prop_info.get("required", False)
        default = prop_info.get("default")

        # Map to Python types for function signature
        if prop_type == "string":
            if required:
                params.append(f"{prop_name}: str")
            else:
                params.append(f"{prop_name}: Optional[str] = None")
        elif prop_type in ("number", "float"):
            if required:
                params.append(f"{prop_name}: float")
            else:
                default_val = default if default is not None else 0.0
                params.append(f"{prop_name}: float = {default_val}")
        elif prop_type == "integer":
            if required:
                params.append(f"{prop_name}: int")
            else:
                default_val = default if default is not None else 0
                params.append(f"{prop_name}: int = {default_val}")
        elif prop_type == "boolean":
            default_val = default if default is not None else False
            params.append(f"{prop_name}: bool = {default_val}")
        elif prop_type == "array":
            params.append(f"{prop_name}: str")  # JSON string for arrays
        else:
            params.append(f"{prop_name}: Optional[str] = None")

        # Handle JSON parsing for arrays
        if prop_type == "array":
            call_params.append(f"{prop_name}=json.loads({prop_name})")
        else:
            call_params.append(f"{prop_name}={prop_name}")

    method_name = _camel_to_snake(component_name)
    params_joined = ",\n        ".join(params) if params else ""
    call_params_joined = ",\n                ".join(call_params) if call_params else ""

    return f'''"""{component_name} MCP tool."""

import asyncio
import json
from typing import Optional


def register_tool(mcp, project_manager):
    """Register the {component_name} tool with the MCP server."""

    @mcp.tool
    async def remotion_add_{method_name}(
        {params_joined}
    ) -> str:
        """
        Add {component_name} to the composition.

        {description}

        Returns:
            JSON with component info
        """
        def _add():
            if not project_manager.current_composition:
                return json.dumps({{"error": "No active project. Create a project first."}})

            try:
                project_manager.current_composition.add_{method_name}(
                    {call_params_joined}
                )
                return json.dumps({{
                    "component": "{component_name}",
                    "status": "added"
                }})
            except Exception as e:
                return json.dumps({{"error": str(e)}})

        return await asyncio.get_event_loop().run_in_executor(None, _add)
'''


def create_builder_py(component_name: str, component_info: dict) -> str:
    """Generate builder.py content."""

    schema = component_info.get("schema", {})
    category = component_info.get("category", "content")

    # Build function parameters
    params = []
    props_dict = []

    for prop_name, prop_info in schema.items():
        prop_type = prop_info.get("type", "str")
        required = prop_info.get("required", False)
        default = prop_info.get("default")

        if prop_type == "string":
            if required:
                params.append(f"{prop_name}: str")
            else:
                params.append(f"{prop_name}: Optional[str] = None")
        elif prop_type in ("number", "float"):
            if required:
                params.append(f"{prop_name}: float")
            else:
                default_val = default if default is not None else 0.0
                params.append(f"{prop_name}: float = {default_val}")
        elif prop_type == "integer":
            if required:
                params.append(f"{prop_name}: int")
            else:
                default_val = default if default is not None else 0
                params.append(f"{prop_name}: int = {default_val}")
        elif prop_type == "boolean":
            default_val = default if default is not None else False
            params.append(f"{prop_name}: bool = {default_val}")
        elif prop_type == "array":
            params.append(f"{prop_name}: list")
        else:
            params.append(f"{prop_name}: Optional[str] = None")

        props_dict.append(f'"{prop_name}": {prop_name}')

    params_joined = ",\n    ".join(params) if params else ""
    props_dict_joined = ",\n            ".join(props_dict) if props_dict else ""

    # Determine layer based on category
    if category == "overlay":
        layer = 10
    elif category == "chart":
        layer = 5
    else:
        layer = 0

    return f'''"""{component_name} composition builder method."""

from typing import Optional, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder, ComponentInstance


def add_to_composition(
    builder: "CompositionBuilder",
    {params_joined}
) -> "CompositionBuilder":
    """
    Add {component_name} to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(locals().get("duration_seconds") or locals().get("duration", 3.0))

    component = ComponentInstance(
        component_type="{component_name}",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={{
            {props_dict_joined}
        }},
        layer={layer}
    )
    builder.components.append(component)
    return builder
'''


def create_init_py(component_name: str) -> str:
    """Generate __init__.py content."""

    return f'''"""{component_name} component."""

from .schema import METADATA, MCP_SCHEMA, {component_name}Props
from .tool import register_tool
from .builder import add_to_composition

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "{component_name}Props",
    "register_tool",
    "add_to_composition"
]
'''


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def migrate_component(component_name: str, component_info: dict, base_path: Path):
    """Migrate a single component to the new structure."""

    category = component_info.get("category", "content")

    # Map category to folder name
    category_folder = {
        "scene": "overlays",
        "overlay": "overlays",
        "chart": "charts",
        "animation": "animations",
        "layout": "layouts",
        "content": "content"
    }.get(category, category)

    component_dir = base_path / "src" / "chuk_mcp_remotion" / "components" / category_folder / component_name
    component_dir.mkdir(parents=True, exist_ok=True)

    print(f"Migrating {component_name} (category: {category})...")

    # Create schema.py
    schema_content = create_schema_py(component_name, component_info)
    (component_dir / "schema.py").write_text(schema_content)

    # Create tool.py
    tool_content = create_tool_py(component_name, component_info)
    (component_dir / "tool.py").write_text(tool_content)

    # Create builder.py
    builder_content = create_builder_py(component_name, component_info)
    (component_dir / "builder.py").write_text(builder_content)

    # Create __init__.py
    init_content = create_init_py(component_name)
    (component_dir / "__init__.py").write_text(init_content)

    # Try to copy template if it exists
    template_locations = [
        base_path / "src" / "chuk_mcp_remotion" / "generator" / "templates" / "overlays" / f"{component_name}.tsx.j2",
        base_path / "src" / "chuk_mcp_remotion" / "generator" / "templates" / "content" / f"{component_name}.tsx.j2",
    ]

    template_copied = False
    for old_template in template_locations:
        if old_template.exists():
            new_template = component_dir / "template.tsx.j2"
            shutil.copy(old_template, new_template)
            print(f"  ✓ Copied template from {old_template.parent.name}")
            template_copied = True
            break

    if not template_copied:
        print(f"  ⚠ Template not found (will need to be created)")

    print(f"  ✓ Created schema.py, tool.py, builder.py, __init__.py")


def main():
    """Run the migration."""
    base_path = Path(__file__).parent

    print("=" * 60)
    print("Migrating ALL components to modular Pydantic structure")
    print("=" * 60)
    print()

    migrated_count = 0

    for component_name, component_info in COMPONENT_REGISTRY.items():
        if component_name in SKIP_COMPONENTS:
            print(f"Skipping {component_name} (already migrated)")
            continue

        migrate_component(component_name, component_info, base_path)
        migrated_count += 1
        print()

    print("=" * 60)
    print(f"Migration complete! Migrated {migrated_count} components.")
    print(f"Skipped {len(SKIP_COMPONENTS)} components (already done).")
    print("=" * 60)


if __name__ == "__main__":
    main()
