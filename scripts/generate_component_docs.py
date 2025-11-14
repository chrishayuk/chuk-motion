#!/usr/bin/env python3
"""Generate component.md documentation files for all components."""

import json
import sys
from pathlib import Path
from typing import Any

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def load_schema_module(component_path: Path, category_folder: str) -> Any:
    """Load the schema.py module from a component directory."""
    schema_file = component_path / "schema.py"
    if not schema_file.exists():
        return None

    try:
        # Construct the module path
        component_name = component_path.name
        module_path = f"chuk_motion.components.{category_folder}.{component_name}.schema"

        # Import the module
        module = __import__(module_path, fromlist=["METADATA", "MCP_SCHEMA"])
        return module
    except Exception as e:
        print(f"    Warning: Could not import schema: {e}")
        return None


def load_metadata_json(component_path: Path) -> dict | None:
    """Load METADATA.json if it exists."""
    metadata_file = component_path / "METADATA.json"
    if metadata_file.exists():
        with open(metadata_file) as f:
            return json.load(f)
    return None


def format_property(name: str, prop_info: dict) -> str:
    """Format a single property for documentation."""
    prop_type = prop_info.get("type", "any")
    required = prop_info.get("required", False)
    default = prop_info.get("default")
    description = prop_info.get("description", "")

    req_badge = "**Required**" if required else f"*Optional* (default: `{default}`)"

    lines = [f"### `{name}`"]
    lines.append(f"- Type: `{prop_type}`")
    lines.append(f"- {req_badge}")
    if description:
        lines.append(f"- {description}")

    # Add enum values if present
    if "values" in prop_info:
        values_str = ", ".join(f"`{v}`" for v in prop_info["values"])
        lines.append(f"- Values: {values_str}")

    return "\n".join(lines)


def generate_component_md(component_path: Path, category: str, category_folder: str) -> str:
    """Generate component.md content for a component."""
    component_name = component_path.name

    # Load schema module
    schema_module = load_schema_module(component_path, category_folder)
    if not schema_module:
        return None

    # Load metadata
    metadata_json = load_metadata_json(component_path)

    # Get MCP schema
    mcp_schema = getattr(schema_module, "MCP_SCHEMA", {})
    metadata = getattr(schema_module, "METADATA", None)

    # Extract information
    description = mcp_schema.get("description", metadata.description if metadata else "")
    schema_props = mcp_schema.get("schema", {})
    example = mcp_schema.get("example", {})
    variants = mcp_schema.get("variants", {})
    animations = mcp_schema.get("animations", {})

    # Build markdown content
    lines = [
        f"# {component_name}",
        "",
        description,
        "",
        "## Overview",
        "",
        f"The `{component_name}` component is a {category} component in the chuk-motion library.",
        "",
    ]

    # Use cases
    if metadata_json and "use_cases" in metadata_json:
        lines.extend([
            "## Use Cases",
            "",
        ])
        for use_case in metadata_json["use_cases"]:
            lines.append(f"- {use_case}")
        lines.append("")

    # Variants
    if variants:
        lines.extend([
            "## Variants",
            "",
        ])
        for variant_name, variant_desc in variants.items():
            lines.append(f"### `{variant_name}`")
            lines.append(variant_desc)
            lines.append("")

    # Animations
    if animations:
        lines.extend([
            "## Animations",
            "",
        ])
        for anim_name, anim_desc in animations.items():
            lines.append(f"### `{anim_name}`")
            lines.append(anim_desc)
            lines.append("")

    # Properties
    lines.extend([
        "## Properties",
        "",
    ])

    for prop_name, prop_info in schema_props.items():
        lines.append(format_property(prop_name, prop_info))
        lines.append("")

    # Example usage
    lines.extend([
        "## Example Usage",
        "",
        "### Python (MCP Tool)",
        "",
        "```python",
    ])

    if example:
        # Generate example code
        tool_name = f"remotion_add_{component_name.lower().replace('_', '_')}"
        lines.append(f"{tool_name}(")

        if isinstance(example, list):
            lines.append(f"    data={json.dumps(example, indent=8).replace('\\n', '\\n    ')},")
            lines.append(f"    title=\"Example Chart\",")
            lines.append(f"    duration=4.0")
        elif isinstance(example, dict):
            for key, value in example.items():
                if isinstance(value, str):
                    lines.append(f'    {key}="{value}",')
                else:
                    lines.append(f"    {key}={value},")

        lines.append(")")

    lines.extend([
        "```",
        "",
        "### TSX (Generated)",
        "",
        "The component generates TypeScript/React code that integrates with Remotion.",
        "",
    ])

    # Design tokens
    lines.extend([
        "## Design Tokens",
        "",
        f"This component uses the chuk-motion design token system for consistent styling:",
        "",
        "- **Colors**: Theme-aware color palettes",
        "- **Typography**: Video-optimized font scales",
        "- **Motion**: Spring physics and easing curves",
        "- **Spacing**: Consistent spacing and safe margins",
        "",
    ])

    # Tips and best practices
    lines.extend([
        "## Tips & Best Practices",
        "",
    ])

    if category == "chart":
        lines.extend([
            "- Keep data concise for readability on video",
            "- Use contrasting colors for better visibility",
            "- Consider animation duration based on data complexity",
            "- Test at your target resolution (1080p, 4K)",
            "",
        ])
    elif category == "overlay" or category == "scene":
        lines.extend([
            "- Keep text concise and readable",
            "- Test animations at target frame rate",
            "- Consider platform safe margins for social media",
            "- Match animation style to overall video aesthetic",
            "",
        ])
    elif category == "layout":
        lines.extend([
            "- Respect platform safe margins",
            "- Test with actual content before finalizing",
            "- Consider aspect ratio and target platform",
            "- Balance content density with readability",
            "",
        ])

    # Related components
    lines.extend([
        "## Related Components",
        "",
        f"Browse other {category} components in the [component library](../../../README.md).",
        "",
    ])

    # Footer
    lines.extend([
        "---",
        "",
        "*Generated documentation for chuk-motion component library*",
    ])

    return "\n".join(lines)


def generate_category_readme(category_path: Path, category_folder: str, category_name: str, components: list[str]) -> str:
    """Generate README.md for a category folder."""
    # Category titles and descriptions
    category_info = {
        "charts": ("Charts", "Data visualization components with animated charts for showing metrics, trends, and proportions."),
        "overlays": ("Overlays", "UI overlay components for titles, lower thirds, end screens, and text emphasis."),
        "layouts": ("Layouts", "Layout components for organizing content in professional video arrangements."),
        "animations": ("Animations", "Animation components for dynamic visual effects."),
        "code": ("Code", "Code display components with syntax highlighting and typing animations."),
        "text-animations": ("Text Animations", "Text animation components with dynamic typography effects."),
        "frames": ("Frames", "Frame components for realistic device and browser mockups."),
        "content": ("Content", "Content container components for organizing and presenting information."),
        "transitions": ("Transitions", "Transition components for smooth scene changes."),
    }

    title, description = category_info.get(category_folder, (category_folder.title(), ""))

    lines = [
        f"# {title}",
        "",
        description,
        "",
        f"## Components ({len(components)})",
        "",
    ]

    # List each component with link
    for component in sorted(components):
        lines.append(f"- **[{component}](./{component}/component.md)** - View documentation")

    lines.extend([
        "",
        "## Usage",
        "",
        "Each component has detailed documentation including:",
        "",
        "- Component overview and description",
        "- Available variants and animations",
        "- Property specifications",
        "- Example usage (Python MCP tools)",
        "- Design token integration",
        "- Tips and best practices",
        "",
        "Click on any component above to view its full documentation.",
        "",
        "---",
        "",
        "*Part of the [chuk-motion](../../../../README.md) component library*",
    ])

    return "\n".join(lines)


def main():
    """Generate component.md for all components and category READMEs."""
    src_path = Path(__file__).parent.parent / "src" / "chuk_motion" / "components"

    # Map of category folders to category names
    categories = {
        "charts": "chart",
        "overlays": "overlay",
        "layouts": "layout",
        "animations": "animation",
        "code": "code",
        "text-animations": "text-animation",
        "frames": "frame",
        "content": "content",
        "transitions": "transition",
    }

    generated_count = 0
    category_components = {cat: [] for cat in categories.keys()}

    for category_folder, category_name in categories.items():
        category_path = src_path / category_folder
        if not category_path.exists():
            continue

        # Find all component directories (those with schema.py)
        for component_dir in category_path.iterdir():
            if not component_dir.is_dir():
                continue
            if component_dir.name.startswith("_"):
                continue

            schema_file = component_dir / "schema.py"
            if not schema_file.exists():
                # Check for components without schema (like text-animations)
                tool_file = component_dir / "tool.py"
                metadata_file = component_dir / "METADATA.json"
                if not (tool_file.exists() or metadata_file.exists()):
                    continue

            print(f"Generating docs for {category_folder}/{component_dir.name}...")

            content = generate_component_md(component_dir, category_name, category_folder)
            if content:
                output_file = component_dir / "component.md"
                with open(output_file, "w", encoding="utf-8", errors="replace") as f:
                    f.write(content)
                generated_count += 1
                category_components[category_folder].append(component_dir.name)
                print(f"  ✓ Created {output_file}")

        # Generate category README
        if category_components[category_folder]:
            readme_content = generate_category_readme(
                category_path,
                category_folder,
                category_name,
                category_components[category_folder]
            )
            readme_file = category_path / "README.md"
            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(readme_content)
            print(f"  ✓ Created {readme_file}")

    print(f"\n✓ Generated {generated_count} component.md files")
    print(f"✓ Generated {len([c for c in category_components.values() if c])} category READMEs")


if __name__ == "__main__":
    main()
