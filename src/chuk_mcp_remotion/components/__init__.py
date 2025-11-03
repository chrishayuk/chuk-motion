# chuk-mcp-remotion/src/chuk_mcp_remotion/components/__init__.py
"""Component system for chuk-mcp-remotion.

Auto-discovers and loads all components from their modular folders.
Each component is self-contained with its own Pydantic models.
"""

import importlib
from pathlib import Path

from .base import ComponentInfo


def discover_components() -> dict[str, ComponentInfo]:
    """
    Discover all components by walking the components directory structure.

    Returns:
        Dictionary mapping component names to their ComponentInfo
    """
    components: dict[str, ComponentInfo] = {}
    components_dir = Path(__file__).parent

    # Walk through category folders (charts, overlays, etc.)
    for category_path in components_dir.iterdir():
        if not category_path.is_dir() or category_path.name.startswith("_"):
            continue

        if category_path.name in ("__pycache__",):
            continue

        category_name = category_path.name

        # Walk through component folders within each category
        for component_path in category_path.iterdir():
            if not component_path.is_dir() or component_path.name.startswith("_"):
                continue

            if component_path.name in ("__pycache__",):
                continue

            component_name = component_path.name

            # Check if component has required files
            init_file = component_path / "__init__.py"
            template_file = component_path / "template.tsx.j2"

            if not init_file.exists():
                continue

            try:
                # Import the component module
                module_path = f"chuk_mcp_remotion.components.{category_name}.{component_name}"
                module = importlib.import_module(module_path)

                # Get component metadata (Pydantic model)
                metadata = getattr(module, "METADATA", None)
                if not metadata:
                    print(f"Warning: Component {component_name} missing METADATA")
                    continue

                # Create ComponentInfo
                component_info = ComponentInfo(
                    metadata=metadata,
                    template_path=template_file if template_file.exists() else None,
                    register_tool=getattr(module, "register_tool", None),
                    add_to_composition=getattr(module, "add_to_composition", None),
                    directory_name=category_name,  # Store actual directory name
                )

                components[component_name] = component_info

            except Exception as e:
                print(f"Warning: Failed to load component {component_name}: {e}")
                import traceback

                traceback.print_exc()
                continue

    return components


def get_component_registry() -> dict[str, dict]:
    """
    Get the component registry (MCP schemas) for MCP tools list.

    Returns:
        Dictionary mapping component names to their MCP schemas
    """
    components = discover_components()
    registry = {}

    for name, comp_info in components.items():
        try:
            # Import module to get MCP_SCHEMA
            # Use directory_name (actual folder) not category (metadata field)
            directory = comp_info.directory_name
            if not directory:
                continue

            module_path = f"chuk_mcp_remotion.components.{directory}.{name}"
            module = importlib.import_module(module_path)
            mcp_schema = getattr(module, "MCP_SCHEMA", None)

            if mcp_schema:
                registry[name] = mcp_schema
        except Exception as e:
            print(f"Warning: Could not get MCP schema for {name}: {e}")

    return registry


def register_all_tools(mcp, project_manager):
    """
    Register all component tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        project_manager: ProjectManager instance
    """
    components = discover_components()
    registered_count = 0

    for name, comp_info in components.items():
        if comp_info.register_tool:
            try:
                comp_info.register_tool(mcp, project_manager)
                registered_count += 1
            except Exception as e:
                print(f"Warning: Failed to register tool for {name}: {e}")
                import traceback

                traceback.print_exc()

    print(f"Registered {registered_count} component tools", flush=True)


def register_all_builders(composition_builder_class):
    """
    Register all composition builder methods dynamically.

    Args:
        composition_builder_class: CompositionBuilder class to add methods to
    """
    components = discover_components()

    for name, comp_info in components.items():
        if comp_info.add_to_composition:
            # Create a method name like "add_line_chart"
            method_name = f"add_{_camel_to_snake(name)}"

            # Create a wrapper function that calls the component's builder
            def make_method(component_builder, m_name=method_name, c_name=name):
                def method(self, *args, **kwargs):
                    return component_builder(self, *args, **kwargs)

                method.__name__ = m_name
                method.__doc__ = f"Add {c_name} component to composition"
                return method

            # Add the method to the class
            setattr(
                composition_builder_class, method_name, make_method(comp_info.add_to_composition)
            )


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


# Export functions
__all__ = [
    "ComponentInfo",
    "discover_components",
    "get_component_registry",
    "register_all_tools",
    "register_all_builders",
]
