# Component Builder Guide

This guide outlines how to build components in the chuk-motion library following modern best practices.

## Component Structure

Each component should have the following file structure:

```
ComponentName/
├── __init__.py          # Package initialization
├── schema.py           # Pydantic models and metadata
├── template.tsx.j2     # React/TypeScript template
├── builder.py          # Composition builder method
├── tool.py             # MCP tool registration
└── component.md        # Documentation
```

## 1. Schema Definition (`schema.py`)

The schema file defines the component's data model and metadata.

### Requirements:

```python
from typing import Any
from pydantic import BaseModel, Field
from ...base import ComponentMetadata


class ComponentNameProps(BaseModel):
    """Properties for ComponentName component."""

    # Define all props with type hints and Field descriptions
    prop_name: str = Field(description="Description of the property")
    optional_prop: float | None = Field(42, description="Optional with default")

    # Required timing props
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"  # Prevent invalid fields


# Component metadata
METADATA = ComponentMetadata(
    name="ComponentName",
    description="Brief description of what the component does",
    category="category_name",  # e.g., "layout", "animation", "frame", etc.
)


# MCP schema (for backward compatibility)
MCP_SCHEMA = {
    "description": "Brief description of what the component does",
    "category": "category_name",
    "schema": {
        "prop_name": {
            "type": "string",
            "required": True,
            "description": "Description of the property"
        },
        "optional_prop": {
            "type": "number",
            "default": 42,
            "description": "Optional with default"
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)"
        },
        "duration": {
            "type": "float",
            "default": 5.0,
            "description": "How long to show (seconds)"
        },
    },
    "example": {
        "prop_name": "example value",
        "optional_prop": 42,
        "start_time": 0.0,
        "duration": 5.0,
        "use_cases": [
            "Use case 1",
            "Use case 2",
        ],
    },
}
```

### Key Points:
- Use `Field()` for all properties with descriptions
- Set `extra = "forbid"` to prevent invalid props
- Include `start_time` and `duration` for timing
- Match MCP_SCHEMA with Pydantic model
- Provide example usage in MCP_SCHEMA

## 2. Template (`template.tsx.j2`)

The template is a Jinja2 template that generates React/TypeScript code.

### Requirements:

```tsx
{/* chuk-motion/src/chuk_motion/components/category/ComponentName/template.tsx.j2 */}
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

interface ComponentNameProps {
  // Define all props with TypeScript types
  propName: string;
  optionalProp?: number;
  startFrame: number;
  durationInFrames: number;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  propName,
  optionalProp = parseInt('[[ spacing.default_value ]]'),  // Use tokens!
  startFrame,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const relativeFrame = frame - startFrame;

  // Don't render if outside the time range
  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* Component content */}
    </AbsoluteFill>
  );
};
```

### Design Token Usage:

Always use design tokens instead of hardcoded values:

```tsx
// Colors
backgroundColor: '[[ colors.background.primary ]]'
color: '[[ colors.text.primary ]]'
borderColor: '[[ colors.border.light ]]'

// Spacing
padding: parseInt('[[ spacing.spacing.xl ]]')
gap: parseInt('[[ spacing.spacing.md ]]')
borderRadius: parseInt('[[ spacing.border_radius.md ]]')

// Typography
fontFamily: '[[ typography.fonts.body ]]'
fontSize: parseInt('[[ typography.sizes.body ]]')
fontWeight: '[[ typography.weights.normal ]]'

// Motion (for animations)
// Access via spring configurations or easing curves
```

### Available Token Categories:
- `colors.*` - Color palettes
- `spacing.*` - Spacing, margins, border radius
- `typography.*` - Fonts, sizes, weights, line heights
- `motion.*` - Animation timings and curves

### Key Points:
- Use `useCurrentFrame()` for frame-based timing
- Calculate `relativeFrame` for animations
- Return `null` when outside time range
- Use `AbsoluteFill` with `pointerEvents: 'none'`
- Use `parseInt()` when converting token values to numbers
- Always prefer design tokens over hardcoded values

## 3. Builder (`builder.py`)

The builder provides a fluent API for adding components to compositions.

### Requirements:

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    prop_name: str,
    optional_prop: float = 42,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add ComponentName to the composition.

    Args:
        builder: CompositionBuilder instance
        start_time: When to show (seconds)
        prop_name: Description of prop
        optional_prop: Optional prop with default
        duration: How long to show (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="ComponentName",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "prop_name": prop_name,
            "optional_prop": optional_prop,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,  # Adjust based on component type
    )
    builder.components.append(component)
    return builder
```

### Key Points:
- Type hint all parameters and return type
- Use `TYPE_CHECKING` to avoid circular imports
- Convert time to frames using `seconds_to_frames()`
- Return builder for method chaining
- Include all props in ComponentInstance

## 4. Tool (`tool.py`)

The tool registers an MCP tool for AI-driven component addition.

### Requirements:

```python
import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ErrorResponse, ComponentResponse  # Use appropriate response type


def register_tool(mcp, project_manager):
    """Register the ComponentName tool with the MCP server."""

    @mcp.tool
    async def remotion_add_component_name(
        prop_name: str,
        optional_prop: float = 42,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add ComponentName to the composition.

        Brief description of what the component does.

        Args:
            prop_name: Description of prop
            optional_prop: Optional prop with default
            duration: Duration in seconds
            track: Track name (default: "main")
            gap_before: Gap before component in seconds

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                # Parse nested components if applicable
                # nested_comp = parse_nested_component(json.loads(nested_json))

                component = ComponentInstance(
                    component_type="ComponentName",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "prop_name": prop_name,
                        "optional_prop": optional_prop,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="ComponentName",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
```

### Response Types:
- `ComponentResponse` - Generic component response
- `LayoutComponentResponse` - For layout components
- `ErrorResponse` - For errors

### Key Points:
- Use async/await with `run_in_executor`
- Always check for active project first
- Use `parse_nested_component()` for nested components
- Return typed responses (JSON serialized)
- Handle errors with ErrorResponse
- Tool name should be snake_case with `remotion_add_` prefix

## 5. Documentation (`component.md`)

Component documentation should follow this structure:

```markdown
# ComponentName

Brief description of what the component does

## Overview

The `ComponentName` component is a [category] component in the chuk-motion library.

## Properties

### `prop_name`
- Type: `string`
- **Required**
- Description of the property

### `optional_prop`
- Type: `number`
- *Optional* (default: `42`)
- Description of the property

### `start_time`
- Type: `float`
- **Required**
- When to show (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `5.0`)
- How long to show (seconds)

## Example Usage

### Python (MCP Tool)

\`\`\`python
remotion_add_component_name(
    prop_name="example",
    optional_prop=42,
    start_time=0.0,
    duration=5.0,
)
\`\`\`

### TSX (Generated)

The component generates TypeScript/React code that integrates with Remotion.

## Design Tokens

This component uses the chuk-motion design token system for consistent styling:

- **Colors**: Theme-aware color palettes
- **Typography**: Video-optimized font scales
- **Motion**: Spring physics and easing curves
- **Spacing**: Consistent spacing and safe margins

## Tips & Best Practices

- Best practice 1
- Best practice 2
- Best practice 3

## Related Components

Browse other [category] components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*
```

## 6. Package Init (`__init__.py`)

Simple package initialization:

```python
"""ComponentName component."""

from .builder import add_to_composition
from .schema import METADATA, ComponentNameProps

__all__ = ["add_to_composition", "ComponentNameProps", "METADATA"]
```

## Best Practices

### 1. Design Tokens
- **Always** use design tokens instead of hardcoded values
- Use `parseInt()` for numeric token values in TypeScript
- Reference tokens with `[[ token.path.here ]]` syntax

### 2. Type Safety
- Use proper type hints in Python (Pydantic models, function signatures)
- Use proper TypeScript interfaces
- Set `extra = "forbid"` in Pydantic Config

### 3. Error Handling
- Check for active project in MCP tools
- Return ErrorResponse for failures
- Use try/except blocks

### 4. Nested Components
- Use `parse_nested_component()` for nested component props
- Accept JSON strings in MCP tool parameters
- Document nested component format in docstrings

### 5. Timing
- Always use frame-based timing in templates
- Convert seconds to frames in builder
- Check frame range before rendering

### 6. Documentation
- Document all props with descriptions
- Include example usage
- Mention design tokens usage
- List use cases

## Example Component: ThreeColumnLayout

See `src/chuk_motion/components/layouts/ThreeColumnLayout/` for a complete reference implementation.

## Checklist

When creating a new component, ensure:

- [ ] `schema.py` with Pydantic model, METADATA, and MCP_SCHEMA
- [ ] `template.tsx.j2` with TypeScript interface and design tokens
- [ ] `builder.py` with type-hinted builder function
- [ ] `tool.py` with async MCP tool and error handling
- [ ] `component.md` with complete documentation
- [ ] `__init__.py` with proper exports
- [ ] All design tokens used (no hardcoded values)
- [ ] Proper type hints throughout
- [ ] Error handling in MCP tool
- [ ] Example usage in docs

## Questions?

Refer to existing components in `src/chuk_motion/components/` for examples, with `ThreeColumnLayout` being the canonical modern example.
