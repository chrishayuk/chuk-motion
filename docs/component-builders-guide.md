# Component Builder's Guide

A comprehensive guide for creating new components in the chuk-motion system.

## Table of Contents

1. [Overview](#overview)
2. [Component Architecture](#component-architecture)
3. [File Structure](#file-structure)
4. [Step-by-Step Component Creation](#step-by-step-component-creation)
5. [Template Guidelines](#template-guidelines)
6. [Design Token Usage](#design-token-usage)
7. [Common Patterns](#common-patterns)
8. [Testing & Validation](#testing--validation)
9. [Troubleshooting](#troubleshooting)

---

## Overview

Each component in this system consists of **5 required files** that work together to provide:
- Python-based configuration and validation (Pydantic)
- MCP tool registration for API exposure
- Composition builder integration
- TSX template for Remotion rendering

### Component Categories

Components are organized into categories:
- `charts/` - Data visualization components
- `overlays/` - UI overlays (lower thirds, text, buttons)
- `layouts/` - Layout components (grid, split screen, containers)
- `code/` - Code display components
- `animations/` - Animation components
- `content/` - Content display components
- `demo_realism/` - Realistic UI mockups for demos

---

## Component Architecture

```
src/chuk_motion/components/
└── [category]/
    └── [ComponentName]/
        ├── __init__.py          # Component registration
        ├── schema.py            # Pydantic schema
        ├── tool.py              # MCP tool registration
        ├── builder.py           # CompositionBuilder method
        └── template.tsx.j2      # React/Remotion TSX template
```

---

## File Structure

### 1. `__init__.py`

**Purpose**: Registers the component and exports its builder method

```python
"""[ComponentName] - [Brief description]."""

from .builder import add_to_composition

__all__ = ["add_to_composition"]
```

### 2. `schema.py`

**Purpose**: Defines Pydantic models for validation

```python
"""Pydantic schema for [ComponentName] component."""

from pydantic import BaseModel, Field
from typing import Literal

class [ComponentName]Props(BaseModel):
    """Props for [ComponentName] component."""

    # Required props
    startFrame: int
    durationInFrames: int

    # Component-specific props
    title: str = Field(default="", description="Title text")
    variant: Literal["minimal", "standard", "bold"] = "standard"

    # Layout props
    position: Literal["center", "top-left", "top-right", ...] = "center"

    # Style props
    width: int = Field(default=800, ge=100, le=1920)
    height: int = Field(default=600, ge=100, le=1080)
```

**Key Points**:
- Always include `startFrame` and `durationInFrames`
- Use `Literal` for constrained string values
- Use `Field()` for defaults and validation
- Add helpful descriptions

### 3. `tool.py`

**Purpose**: Registers the MCP tool for API exposure

```python
"""MCP tool registration for [ComponentName]."""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server import Server

def register_tool(mcp, project_manager):
    """Register the [ComponentName] MCP tool."""

    @mcp.tool
    async def remotion_add_[component_name](
        startFrame: int,
        durationInFrames: int,
        title: str = "",
        variant: str = "standard",
        position: str = "center",
        width: int = 800,
        height: int = 600,
        # Use str for array/object parameters
        options: str = "{}",
    ) -> str:
        """Add a [ComponentName] component to the composition.

        Args:
            startFrame: Starting frame number
            durationInFrames: Duration in frames
            title: Title text
            variant: Style variant
            position: Position on screen
            width: Component width
            height: Component height
            options: JSON string for additional options

        Returns:
            Success message
        """
        # Parse JSON parameters
        options_parsed = json.loads(options) if options else {}

        # Add to composition...
        return "✓ [ComponentName] added successfully"
```

**Critical Rules**:
- **Never** use `@mcp.tool(name=..., description=..., schema=...)`
- Use `@mcp.tool` decorator only
- **Never** use `List[dict]` - use `str` and parse JSON
- Always parse JSON string parameters
- Use `TYPE_CHECKING` for type hints

### 4. `builder.py`

**Purpose**: Provides fluent API method for CompositionBuilder

```python
"""Composition builder method for [ComponentName] component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_motion.generator.composition_builder import CompositionBuilder

def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    title: str = "",
    variant: str = "standard",
    position: str = "center",
    width: int = 800,
    height: int = 600,
) -> "CompositionBuilder":
    """Add a [ComponentName] component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        title: Title text
        variant: Style variant
        position: Position on screen
        width: Component width
        height: Component height

    Returns:
        The builder instance for method chaining
    """
    from chuk_motion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    # Create component instance
    component = ComponentInstance(
        component_type="[ComponentName]",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "title": title,
            "variant": variant,
            "position": position,
            "width": width,
            "height": height,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,  # Adjust based on component type
    )

    builder.components.append(component)
    return builder
```

**Key Points**:
- Accept **seconds** not frames (`start_time`, `duration`)
- Convert to frames using `builder.seconds_to_frames()`
- Use `ComponentInstance` not Pydantic models
- Append to `builder.components`
- Return `builder` for chaining
- Layer values: 0=background, 5=content, 10=overlays

### 5. `template.tsx.j2`

**Purpose**: Jinja2 template that generates React/Remotion component

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';

interface [ComponentName]Props {
  startFrame: number;
  durationInFrames: number;
  title: string;
  variant: 'minimal' | 'standard' | 'bold';
  position: string;
  width: number;
  height: number;
}

export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  startFrame,
  durationInFrames,
  title = '',
  variant = 'standard',
  position = 'center',
  width = 800,
  height = 600,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Visibility check
  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  const relativeFrame = frame - startFrame;

  // Position mapping
  const positionMap: Record<string, React.CSSProperties> = {
    center: {
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
    },
    'top-left': { top: '[[ spacing.spacing.xl ]]', left: '[[ spacing.spacing.xl ]]' },
    'top-center': { top: '[[ spacing.spacing.xl ]]', left: '50%', transform: 'translateX(-50%)' },
    // ... more positions
  };

  // Entrance animation
  const entrance = spring({
    frame: relativeFrame,
    fps,
    config: {
      damping: [[ motion.default_spring.config.damping ]],
      stiffness: [[ motion.default_spring.config.stiffness ]],
      mass: [[ motion.default_spring.config.mass ]],
    },
  });

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          ...positionMap[position],
          width,
          height,
          opacity: entrance,
          transform: `${positionMap[position]?.transform || ''} scale(${entrance})`,
        }}
      >
        {/* Component content */}
        <div style={{
          background: '[[ colors.primary[0] ]]',
          color: '[[ colors.text ]]',
          padding: '[[ spacing.spacing.lg ]]',
          borderRadius: '[[ spacing.border_radius.lg ]]',
          fontFamily: "'[[ "', '".join(typography.body_font.fonts) ]]'",
          fontSize: 36,
          fontWeight: [[ typography.font_weights.bold ]],
        }}>
          {title}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Template Guidelines

### Jinja2 Delimiters

**IMPORTANT**: Use custom delimiters to avoid JSX conflicts:
- Variables: `[[ variable ]]` not `{{ variable }}`
- Blocks: `[% if %] ... [% endif %]` not `{% if %}`

### Available Template Variables

The following variables are available in templates:

```javascript
// Component configuration (from props)
config = {}  // Empty - props come from VideoComposition

// Theme data
theme = { colors: {...}, typography: {...}, motion: {...} }
colors = theme.colors
typography = { ...theme.typography, font_sizes, font_weights, ... }
motion = theme.motion
spacing = SPACING_TOKENS
font_sizes = TYPOGRAPHY_TOKENS['font_sizes']['video_1080p']
```

### Design Token Access

#### ✅ CORRECT Usage

```tsx
// Spacing - tokens already include "px"
padding: '[[ spacing.spacing.lg ]]'      // → "24px"
borderRadius: '[[ spacing.border_radius.md ]]'  // → "8px"

// Colors
background: '[[ colors.primary[0] ]]'    // → "#007bff"
color: '[[ colors.text ]]'               // → "#ffffff"

// Typography
fontFamily: "'[[ "', '".join(typography.body_font.fonts) ]]'"
fontWeight: [[ typography.font_weights.bold ]]  // → 700

// Motion
damping: [[ motion.default_spring.config.damping ]]

// Font sizes - use hardcoded values
fontSize: 36  // For 1080p
```

#### ❌ INCORRECT Usage

```tsx
// DON'T add "px" to spacing tokens
padding: '[[ spacing.xl ]]px'  // Wrong! Becomes "32pxpx"

// DON'T use template variables for fps
fps: [[ fps ]]  // Wrong! Not available in template

// DON'T use smooth_spring
damping: [[ motion.smooth_spring.config.damping ]]  // Wrong!

// DON'T use mono_font
fontFamily: [[ typography.mono_font.fonts ]]  // Wrong! Use code_font

// DON'T use font_sizes template variable
fontSize: [[ font_sizes.lg ]]  // Wrong! Use hardcoded number
```

### Getting FPS

Always use `useVideoConfig()`:

```tsx
const { fps } = useVideoConfig();

// Then use it
const animation = spring({
  frame: relativeFrame,
  fps,  // ✅ Correct
  config: { ... }
});
```

### Handling JSON String Props

For props that receive JSON strings (arrays/objects):

```tsx
interface ComponentProps {
  tabs?: TabConfig[] | string;  // Accept both types
  // ...
}

export const Component: React.FC<ComponentProps> = ({
  tabs,
  // ...
}) => {
  // Parse if string
  const parsedTabs: TabConfig[] = typeof tabs === 'string'
    ? JSON.parse(tabs)
    : (tabs || []);

  // Use parsedTabs throughout component
  return (
    <div>
      {parsedTabs.map((tab, i) => ...)}
    </div>
  );
};
```

---

## Design Token Usage

### Spacing Tokens

```python
SPACING_TOKENS = {
    "spacing": {
        "xs": "8px",
        "sm": "12px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
        "2xl": "48px",
    },
    "border_radius": {
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
    }
}
```

**Access**: `spacing.spacing.lg` → "24px"

### Color Tokens

```python
colors = {
    "primary": ["#007bff", "#0056b3", ...],  # Gradient steps
    "accent": ["#ff4081", ...],
    "text": "#ffffff",
    "background": "#000000",
}
```

**Access**: `colors.primary[0]` or `colors.text`

### Typography Tokens

```python
typography = {
    "body_font": { "fonts": ["Inter", "SF Pro Text", ...] },
    "code_font": { "fonts": ["JetBrains Mono", ...] },
    "font_weights": {
        "regular": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700,
    }
}
```

**Access**:
- `typography.body_font.fonts` (join with ", ")
- `typography.font_weights.bold` → 700

### Motion Tokens

```python
motion = {
    "default_spring": {
        "config": {
            "damping": 200,
            "stiffness": 200,
            "mass": 0.5,
        }
    }
}
```

**Access**: `motion.default_spring.config.damping`

---

## Common Patterns

### Standard Component Structure

```tsx
export const Component: React.FC<Props> = ({
  startFrame,
  durationInFrames,
  ...props
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Visibility check
  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  const relativeFrame = frame - startFrame;

  // 2. Parse JSON props if needed
  const parsedData = typeof data === 'string' ? JSON.parse(data) : data;

  // 3. Position mapping
  const positionMap = { /* ... */ };

  // 4. Entrance animation
  const entrance = spring({
    frame: relativeFrame,
    fps,
    config: {
      damping: [[ motion.default_spring.config.damping ]],
      stiffness: [[ motion.default_spring.config.stiffness ]],
      mass: [[ motion.default_spring.config.mass ]],
    },
  });

  // 5. Render
  return (
    <AbsoluteFill>
      {/* Component content */}
    </AbsoluteFill>
  );
};
```

### Position Mapping Pattern

```tsx
const positionMap: Record<string, React.CSSProperties> = {
  center: {
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
  },
  'top-left': {
    top: '[[ spacing.spacing.xl ]]',
    left: '[[ spacing.spacing.xl ]]'
  },
  'top-center': {
    top: '[[ spacing.spacing.xl ]]',
    left: '50%',
    transform: 'translateX(-50%)'
  },
  'top-right': {
    top: '[[ spacing.spacing.xl ]]',
    right: '[[ spacing.spacing.xl ]]'
  },
  'center-left': {
    top: '50%',
    left: '[[ spacing.spacing.xl ]]',
    transform: 'translateY(-50%)'
  },
  'center-right': {
    top: '50%',
    right: '[[ spacing.spacing.xl ]]',
    transform: 'translateY(-50%)'
  },
  'bottom-left': {
    bottom: '[[ spacing.spacing.xl ]]',
    left: '[[ spacing.spacing.xl ]]'
  },
  'bottom-center': {
    bottom: '[[ spacing.spacing.xl ]]',
    left: '50%',
    transform: 'translateX(-50%)'
  },
  'bottom-right': {
    bottom: '[[ spacing.spacing.xl ]]',
    right: '[[ spacing.spacing.xl ]]'
  },
};
```

### Spring Animation Pattern

```tsx
// Entrance animation
const entrance = spring({
  frame: relativeFrame,
  fps,
  config: {
    damping: [[ motion.default_spring.config.damping ]],
    stiffness: [[ motion.default_spring.config.stiffness ]],
    mass: [[ motion.default_spring.config.mass ]],
  },
});

// Use in styles
style={{
  opacity: entrance,
  transform: `scale(${entrance})`,
}}
```

### Typing Animation Pattern

```tsx
const typeText = (text: string, startFrame: number, speed: number = 0.05) => {
  const charsToShow = Math.floor((relativeFrame - startFrame) / (fps * speed));
  return text.slice(0, Math.max(0, charsToShow));
};

// Usage
const displayedText = typeText(content, 20, 0.04);
```

---

## Step-by-Step Component Creation

### 1. Choose Category and Name

```bash
# Decide on category and component name
CATEGORY="overlays"
COMPONENT="CallToAction"
```

### 2. Create Directory Structure

```bash
mkdir -p src/chuk_motion/components/$CATEGORY/$COMPONENT
```

### 3. Create `__init__.py`

```python
"""CallToAction - Animated call-to-action button with customizable styles."""

from .builder import add_to_composition

__all__ = ["add_to_composition"]
```

### 4. Create `schema.py`

Define your Pydantic model with all props and validation.

### 5. Create `tool.py`

Register the MCP tool following the patterns above.

### 6. Create `builder.py`

Create the CompositionBuilder method.

### 7. Create `template.tsx.j2`

Create the React/Remotion component template.

### 8. Register Category (if new)

If adding a new category, update:

```python
# src/chuk_motion/generator/component_builder.py
self.template_categories = [
    "charts",
    "overlays",
    "layouts",
    "code",
    "animations",
    "content",
    "demo_realism",
    "your_new_category",  # Add here
]
```

### 9. Test Component

Create a test example:

```python
# examples/test_my_component.py
from chuk_motion.utils.project_manager import ProjectManager
from chuk_motion.generator.composition_builder import CompositionBuilder

manager = ProjectManager()
project = manager.create_project("test_component", theme="tech")

manager.current_composition = CompositionBuilder(fps=30, width=1920, height=1080)
manager.current_composition.add_call_to_action(
    start_time=1.0,
    duration=3.0,
    text="Click Me!",
    variant="bold",
)

manager.generate_composition()
```

### 10. Run and Validate

```bash
python examples/test_my_component.py
cd remotion-projects/test_component
npm install
npm run build
```

---

## Testing & Validation

### Checklist

- [ ] All 5 files created and properly structured
- [ ] Pydantic schema validates correctly
- [ ] MCP tool registers without errors (check decorator!)
- [ ] Builder method uses time-based API (seconds)
- [ ] Template uses correct Jinja2 delimiters `[[ ]]`
- [ ] Design tokens accessed correctly (no double "px")
- [ ] FPS obtained from `useVideoConfig()`
- [ ] JSON props parsed if needed
- [ ] Component renders without errors
- [ ] Entrance animation works smoothly
- [ ] Position mapping works for all positions
- [ ] Component follows design system

### Common Test Cases

1. **Minimal props**: Test with only required props
2. **All props**: Test with all optional props set
3. **Edge cases**: Test extreme values (very long text, tiny dimensions)
4. **JSON props**: Test with both array and string formats
5. **Multiple instances**: Test with several instances at different times
6. **Layer conflicts**: Test with components on different layers

---

## Troubleshooting

### Build Errors

#### "Module not found: Error: Can't resolve './components/MyComponent'"

**Cause**: Component TSX file not generated

**Fix**: Ensure category is registered in `component_builder.py` template_categories

#### "TypeError: X.map is not a function"

**Cause**: Array prop passed as JSON string but not parsed

**Fix**: Add JSON parsing in component:
```tsx
const parsed = typeof prop === 'string' ? JSON.parse(prop) : prop;
```

#### "Transform failed: Unexpected ','"

**Cause**: Template variable rendered empty (e.g., `fps: ,`)

**Fix**: Don't use template variables for runtime values like `fps`. Use `useVideoConfig()` instead.

#### "'dict object' has no attribute 'X'"

**Cause**: Incorrect token access in template

**Fix**: Check token structure:
- `spacing.spacing.lg` not `spacing.lg`
- `motion.default_spring` not `motion.smooth_spring`
- `typography.code_font` not `typography.mono_font`

### Template Rendering Issues

#### "8pxpx" or double units

**Cause**: Adding "px" to spacing tokens that already include it

**Fix**: Use `[[ spacing.spacing.lg ]]` not `[[ spacing.spacing.lg ]]px`

#### Font family not rendering

**Cause**: Incorrect join syntax

**Fix**: Use `"'[[ "', '".join(typography.body_font.fonts) ]]'"`

### MCP Registration Errors

#### "unhashable type: 'list'"

**Cause**: Using `List[dict]` in tool parameters

**Fix**: Use `str` and parse JSON

#### "unexpected keyword argument 'schema'"

**Cause**: Using old decorator syntax

**Fix**: Use only `@mcp.tool` without any parameters

---

## Best Practices

1. **Always validate props** with Pydantic schemas
2. **Use design tokens** instead of hardcoded values where possible
3. **Follow naming conventions**: PascalCase for components
4. **Document everything**: Add docstrings and comments
5. **Test thoroughly**: Check all variants and edge cases
6. **Keep templates simple**: Complex logic should be in helpers
7. **Reuse patterns**: Follow existing component structures
8. **Version control**: Commit each component separately
9. **Performance**: Avoid expensive calculations in render
10. **Accessibility**: Consider text contrast and sizing

---

## Reference Examples

### Simple Component
See: `src/chuk_motion/components/overlays/TextOverlay/`

### Complex Component with JSON Props
See: `src/chuk_motion/components/demo_realism/BrowserFrame/`

### Layout Component with Children
See: `src/chuk_motion/components/layouts/Grid/`

### Chart Component
See: `src/chuk_motion/components/charts/LineChart/`

---

## Quick Reference Card

```
Template Delimiters:   [[ var ]]  [% if %]
Spacing:              spacing.spacing.lg
Border Radius:        spacing.border_radius.md
Colors:               colors.primary[0]
Typography:           typography.body_font.fonts
Font Weight:          typography.font_weights.bold
Motion:               motion.default_spring.config.damping
FPS:                  const { fps } = useVideoConfig()
Font Size:            36 (hardcoded)

Layer Values:
  0  = Background
  5  = Content
  10 = Overlays

Time API:             start_time (seconds), duration (seconds)
Frame Conversion:     builder.seconds_to_frames(seconds)
Component Creation:   ComponentInstance(...)
Builder Return:       return builder
```

---

## Additional Resources

- [Token System Documentation](./token-system.md)
- [Theme System](../src/chuk_motion/themes/youtube_themes.py)
- [Remotion Documentation](https://www.remotion.dev/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Last Updated**: November 2025
**Version**: 1.0.0
