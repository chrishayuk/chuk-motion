# chuk-motion/src/chuk_motion/components/__init__.py
"""Component system for chuk-motion.

Auto-discovers and loads all components from their modular folders.
Each component is self-contained with its own Pydantic models.
"""

import importlib
import logging
from pathlib import Path

from .base import ComponentInfo

logger = logging.getLogger(__name__)


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
                module_path = f"chuk_motion.components.{category_name}.{component_name}"
                module = importlib.import_module(module_path)

                # Get component metadata - try schema.py first (new refactored components)
                metadata = getattr(module, "METADATA", None)
                if not metadata:
                    # Try importing from schema.py (new component structure)
                    try:
                        schema_module_path = f"{module_path}.schema"
                        schema_module = importlib.import_module(schema_module_path)
                        metadata = getattr(schema_module, "METADATA", None)
                    except ImportError:
                        pass

                # Skip components without metadata
                if not metadata:
                    logger.debug(f"Component {component_name} has no METADATA, skipping")
                    continue

                # Get register_tool function - try tool.py if not in __init__.py
                register_tool = getattr(module, "register_tool", None)
                if not register_tool:
                    try:
                        tool_module_path = f"{module_path}.tool"
                        tool_module = importlib.import_module(tool_module_path)
                        register_tool = getattr(tool_module, "register_tool", None)
                    except ImportError:
                        pass

                # Get add_to_composition function - try builder.py if not in __init__.py
                add_to_composition = getattr(module, "add_to_composition", None)
                if not add_to_composition:
                    try:
                        builder_module_path = f"{module_path}.builder"
                        builder_module = importlib.import_module(builder_module_path)
                        add_to_composition = getattr(builder_module, "add_to_composition", None)
                    except ImportError:
                        pass

                # Create ComponentInfo
                component_info = ComponentInfo(
                    metadata=metadata,
                    template_path=template_file if template_file.exists() else None,
                    register_tool=register_tool,
                    add_to_composition=add_to_composition,
                    directory_name=category_name,  # Store actual directory name
                )

                components[component_name] = component_info

            except Exception as e:
                logger.warning(f"Failed to load component {component_name}: {e}", exc_info=True)
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

            module_path = f"chuk_motion.components.{directory}.{name}"
            module = importlib.import_module(module_path)
            mcp_schema = getattr(module, "MCP_SCHEMA", None)

            # Try schema.py if not found in __init__.py (new component structure)
            if not mcp_schema:
                try:
                    schema_module_path = f"{module_path}.schema"
                    schema_module = importlib.import_module(schema_module_path)
                    mcp_schema = getattr(schema_module, "MCP_SCHEMA", None)
                except ImportError:
                    pass

            if mcp_schema:
                registry[name] = mcp_schema
        except Exception as e:
            logger.warning(f"Could not get MCP schema for {name}: {e}")

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
                logger.warning(f"Failed to register tool for {name}: {e}", exc_info=True)

    logger.debug(f"Registered {registered_count} component tools")


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


def register_all_renderers(composition_builder_class):
    """
    Register all component-specific JSX renderers dynamically.

    Args:
        composition_builder_class: CompositionBuilder class to register renderers with
    """
    components = discover_components()
    registered_count = 0

    for name, comp_info in components.items():
        # Try to import the component's renderer module
        try:
            directory = comp_info.directory_name
            if not directory:
                continue

            module_path = f"chuk_motion.components.{directory}.{name}.renderer"
            module = importlib.import_module(module_path)

            # Get the render_jsx function
            render_jsx = getattr(module, "render_jsx", None)
            if render_jsx:
                composition_builder_class._component_renderers[name] = render_jsx
                registered_count += 1
        except (ImportError, AttributeError):
            # No renderer for this component - that's okay, not all need custom rendering
            pass

    if registered_count > 0:
        logger.debug(f"Registered {registered_count} custom component renderers")


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
    "register_all_renderers",
]
