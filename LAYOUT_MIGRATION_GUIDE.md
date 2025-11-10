# Layout Migration Guide

## Completed Layouts ✅
- ThreeByThreeGrid
- ThreeColumnLayout
- ThreeRowLayout
- Container (existing)
- Grid (existing)
- SplitScreen (existing)

## Remaining Layouts to Migrate

### Core Layouts
1. **AsymmetricLayout** - Main feed (2/3) + two demo panels (1/3 stacked)
2. **PiP** - Picture-in-Picture with positions (bottom-right, bottom-left, top-right, top-left)
3. **Vertical** - 9:16 optimized layouts: top-bottom, caption-content, content-caption, split-vertical

### Specialized Layouts
4. **OverTheShoulder** - Looking over someone's shoulder perspective
5. **DialogueFrame** - For conversation/dialogue scenes
6. **StackedReaction** - Reaction video style with stacked feeds
7. **HUDStyle** - Heads-up display style with overlay elements
8. **PerformanceMultiCam** - Multi-camera performance view
9. **FocusStrip** - Focused strip/banner layout
10. **Timeline** - Progress/timeline overlay with milestones
11. **Mosaic** - Irregular collage with layered clips

## Layout Component Structure

Each layout needs 5 files in `src/chuk_mcp_remotion/components/layouts/{LayoutName}/`:

### 1. `schema.py`
```python
"""Component schema and Pydantic models."""
from typing import Any
from pydantic import BaseModel, Field
from ...base import ComponentMetadata

class {LayoutName}Props(BaseModel):
    """Properties for {LayoutName} component."""
    # Define props here
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"

METADATA = ComponentMetadata(
    name="{LayoutName}",
    description="Description",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Description",
    "category": "layout",
    "schema": {...},
    "example": {...},
}
```

### 2. `builder.py`
```python
"""Composition builder method."""
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder

def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    # ... other props
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add {LayoutName} to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="{LayoutName}",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={...},
        layer=0,
    )
    builder.components.append(component)
    return builder
```

### 3. `tool.py`
```python
"""MCP tool."""
import asyncio
import json
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse

def register_tool(mcp, project_manager):
    """Register the tool with the MCP server."""

    @mcp.tool
    async def remotion_add_{layout_name}(
        # props
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """Tool description."""

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            # Parse JSON components
            # Create component
            # Add to timeline

            return LayoutComponentResponse(...).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
```

### 4. `template.tsx.j2`
```tsx
{/* Template with token usage */}
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

interface {LayoutName}Props {
  startFrame: number;
  durationInFrames: number;
  // other props
}

export const {LayoutName}: React.FC<{LayoutName}Props> = ({
  startFrame,
  durationInFrames,
  padding = parseInt('[[ spacing.spacing.xl ]]'),
  gap = parseInt('[[ spacing.spacing.md ]]'),
  border_radius = parseInt('[[ spacing.border_radius.md ]]'),
  // other props with token defaults
}) => {
  const frame = useCurrentFrame();

  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* Layout implementation */}
    </AbsoluteFill>
  );
};
```

### 5. `__init__.py`
```python
"""Component export."""
from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, {LayoutName}Props
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "{LayoutName}Props",
    "register_tool",
    "add_to_composition",
]
```

## Key Requirements

### Token Usage
Always use design tokens in templates:
- **Spacing**: `parseInt('[[ spacing.spacing.xl ]]')` for padding (32px)
- **Spacing**: `parseInt('[[ spacing.spacing.md ]]')` for gap (16px)
- **Border radius**: `parseInt('[[ spacing.border_radius.md ]]')` (8px)

### Component Registration
After creating a layout, update `src/chuk_mcp_remotion/components/layouts/__init__.py` to export it.

### Common Props Pattern
Most layouts share these props:
- `gap`: spacing between elements (default: 20px, but use token in template)
- `padding`: outer padding (default: 40px, but use token in template)
- `border_width`: optional border
- `border_color`: border color (default: 'rgba(255, 255, 255, 0.2)')
- `border_radius`: corner radius (use token)
- `start_time`: when to show
- `duration`: how long to show

## Layout-Specific Details

### AsymmetricLayout
- `main`: left 2/3 content
- `top_side`: top right 1/3
- `bottom_side`: bottom right 1/3
- Main column 66.67%, side 33.33%

### PiP
- `main`: full background
- `overlay`: small overlay
- `position`: "bottom-right" | "bottom-left" | "top-right" | "top-left"
- `overlay_size`: percentage of screen (default: 20)
- `margin`: margin from edges

### Vertical
- Optimized for 9:16 aspect ratio
- `layout_style`: "top-bottom" | "caption-content" | "content-caption" | "split-vertical"
- `top` and `bottom` content props

### OverTheShoulder, DialogueFrame, StackedReaction, etc.
Reference test files in `tests/templates/layouts/` for expected props and behavior.

## Testing
Each layout should have tests in `tests/components/layouts/{LayoutName}/test_{layoutname}.py` following the pattern in existing tests.
