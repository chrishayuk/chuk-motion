# Component Design Principles

## Overview

This document describes the architectural patterns and design principles for all Remotion components in the chuk-motion generator system.

## Component Architecture

### Component Types

Components are organized into three categories:

1. **Overlays** (`overlays/`) - UI elements that appear on top of content
   - Title cards, lower thirds, text overlays
   - Examples: TitleScene, LowerThird

2. **Content** (`content/`) - Primary visual content elements
   - Code displays, charts, visualizations, demo boxes
   - Examples: CodeBlock, TypingCode, LineChart, DemoBox

3. **Layouts** (`layouts/`) - Container components that arrange children
   - Grid systems, split screens, multi-cam setups
   - Examples: Grid, ThreeByThreeGrid, AsymmetricLayout, PiPLayout

## Core Design Patterns

### 1. Timing Props (Required)

**Every component MUST accept these timing props:**

```typescript
interface ComponentProps {
  startFrame: number;          // When component becomes visible
  durationInFrames: number;    // How long component is visible
  // ... other props
}
```

**Visibility Check Pattern:**

```typescript
export const Component: React.FC<ComponentProps> = ({
  startFrame,
  durationInFrames,
  // ... other props
}) => {
  const frame = useCurrentFrame();

  // Don't render if outside the time range
  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  // Component implementation
};
```

**Why?** This enables precise frame-based timing control for video composition.

### 2. Props vs Template Variables

Components use a **two-phase rendering system**:

#### Phase 1: Template-Time (Jinja2)
- **Design tokens** injected from theme
- **Configuration values** from scene config
- Uses `[[ variable ]]` and `[% logic %]` syntax

```typescript
// Template variables (resolved at generation time)
const color = '[[ colors.primary[0] ]]';           // → '#0066FF'
const font = '[[ typography.primary_font.fonts ]]'; // → 'Inter'
const damping = [[ motion.default_spring.config.damping ]]; // → 200
```

#### Phase 2: Runtime (React/Remotion)
- **Content data** passed as props
- **Dynamic behavior** calculated per-frame
- Standard TypeScript/React props

```typescript
// Runtime props (resolved during video rendering)
interface ComponentProps {
  title: string;              // Content data
  variant?: string;           // Behavior control
  startFrame: number;         // Timing
  durationInFrames: number;   // Timing
}
```

### 3. Children Handling

#### Named Props Pattern (Preferred)
Use named props for components with specific, semantic children:

```typescript
interface LayoutProps {
  leftPanel?: React.ReactNode;
  rightPanel?: React.ReactNode;
  startFrame: number;
  durationInFrames: number;
}

export const SplitScreen: React.FC<LayoutProps> = ({
  leftPanel,
  rightPanel,
  // ...
}) => {
  return (
    <AbsoluteFill>
      <div style={{ flex: 1 }}>{leftPanel}</div>
      <div style={{ flex: 1 }}>{rightPanel}</div>
    </AbsoluteFill>
  );
};
```

**Use named props when:**
- Children have specific semantic meaning (left/right, main/pip, host/screen)
- Different children need different styling or positioning
- Component layout is not generic

#### Children Array Pattern
Use children array for generic, homogeneous layouts:

```typescript
interface GridProps {
  children: React.ReactNode[];
  startFrame: number;
  durationInFrames: number;
  // ...
}

export const Grid: React.FC<GridProps> = ({
  children,
  // ...
}) => {
  const gridChildren = Array.isArray(children) ? children : [children];

  return (
    <div style={{ display: 'grid' }}>
      {gridChildren.map((child, idx) => (
        <div key={idx}>{child}</div>
      ))}
    </div>
  );
};
```

**Use children array when:**
- All children are treated equally
- Number of children is variable
- Generic grid or list layouts

### 4. Styling Patterns

#### Absolute Positioning
Layout components should use `AbsoluteFill` for full-screen layouts:

```typescript
return (
  <AbsoluteFill style={{ pointerEvents: 'none' }}>
    {/* Layout content */}
  </AbsoluteFill>
);
```

#### Relative Positioning
Content within layouts should use relative positioning with flex or grid:

```typescript
<div
  style={{
    position: 'absolute',
    top: padding,
    left: padding,
    right: padding,
    bottom: padding,
    display: 'flex',
    gap: gap,
  }}
>
  {/* Content */}
</div>
```

### 5. Animation Patterns

#### Spring Animations (Entrances)
Use springs for smooth, natural entrances:

```typescript
const entranceProgress = spring({
  frame: relativeFrame,
  fps,
  config: {
    damping: [[ motion.default_spring.config.damping ]],
    stiffness: [[ motion.default_spring.config.stiffness ]]
  }
});

const scale = interpolate(entranceProgress, [0, 1], [0.8, 1]);
const opacity = entranceProgress;
```

#### Interpolate (Exits and Linear)
Use interpolate for exits and linear transitions:

```typescript
const exitDuration = 20;
const exitProgress = interpolate(
  relativeFrame,
  [durationInFrames - exitDuration, durationInFrames],
  [1, 0],
  {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  }
);

const finalOpacity = entranceOpacity * exitProgress;
```

### 6. Variant System

Components should support multiple visual variants:

```typescript
interface ComponentProps {
  variant?: string;  // 'minimal' | 'standard' | 'bold' | 'glass'
  // ...
}

const variants = {
  minimal: { /* styles */ },
  standard: { /* styles */ },
  bold: { /* styles */ },
  glass: { /* styles */ }
};

const variantStyle = variants[variant as keyof typeof variants] || variants.standard;
```

### 7. Design Token Integration

Always use design tokens for theming:

```typescript
// ✅ CORRECT - Uses theme tokens
const color = '[[ colors.primary[0] ]]';
const font = '[[ typography.primary_font.fonts ]]';
const background = '[[ colors.background.dark ]]';

// ❌ WRONG - Hardcoded values
const color = '#0066FF';
const font = 'Inter';
const background = '#0A0E1A';
```

## Component Structure Template

Every component should follow this structure:

```typescript
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

interface ComponentNameProps {
  // Content props
  title?: string;

  // Timing props (REQUIRED)
  startFrame: number;
  durationInFrames: number;

  // Styling props
  variant?: string;
  animation?: string;

  // Configuration props
  padding?: number;
  gap?: number;
}

/**
 * ComponentName - Brief description
 *
 * Perfect for:
 * - Use case 1
 * - Use case 2
 *
 * Features:
 * - Feature 1
 * - Feature 2
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  title = 'Default Title',
  startFrame,
  durationInFrames,
  variant = 'standard',
  animation = 'fade_in',
  padding = 40,
  gap = 20
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const relativeFrame = frame - startFrame;

  // Visibility check
  if (frame < startFrame || frame >= startFrame + durationInFrames) {
    return null;
  }

  // Animation logic
  const entranceProgress = spring({
    frame: relativeFrame,
    fps,
    config: { damping: [[ motion.default_spring.config.damping ]] }
  });

  // Variant styles
  const variants = {
    standard: { /* ... */ },
    bold: { /* ... */ }
  };
  const variantStyle = variants[variant as keyof typeof variants] || variants.standard;

  // Render
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* Component implementation */}
    </AbsoluteFill>
  );
};
```

## Best Practices

### DO ✅

1. **Always include timing props** (startFrame, durationInFrames)
2. **Always include visibility check** at the start of the component
3. **Use design tokens** for colors, fonts, and motion
4. **Provide default values** for all optional props
5. **Use semantic prop names** (hostView, screenContent, not just child1, child2)
6. **Include JSDoc comments** describing the component's purpose
7. **Support multiple variants** for flexibility
8. **Use spring animations** for entrances
9. **Use interpolate** for exits and linear animations
10. **Test with multiple themes** to ensure token system works

### DON'T ❌

1. **Don't hardcode colors or fonts** - use theme tokens
2. **Don't skip visibility checks** - components should respect timing
3. **Don't use generic prop names** like "content" when semantic names fit
4. **Don't forget exit animations** - fade out at end of duration
5. **Don't use state** unless absolutely necessary (prefer frame calculations)
6. **Don't rely on external data** during render (pre-load everything)
7. **Don't nest layouts deeply** - keep component hierarchy flat
8. **Don't use percentages** without calc() for gaps/padding
9. **Don't forget TypeScript interfaces** - type all props
10. **Don't skip tests** - every component should have comprehensive tests

## Testing Requirements

Every component must have tests covering:

1. **Basic generation** - Component renders without errors
2. **Timing props** - startFrame and durationInFrames are present
3. **Visibility check** - Component respects frame timing
4. **TypeScript validity** - No unresolved template variables
5. **Interface definition** - Proper TypeScript interface exists
6. **Variants** (if applicable) - All variants generate correctly
7. **Design tokens** - Theme colors/fonts/motion are injected
8. **Props** - All props are properly used

See `tests/templates/README_TEMPLATE_TESTS.md` for testing guidelines.

## File Organization

```
src/chuk_motion/generator/templates/
├── overlays/          # UI overlay components
│   ├── TitleScene.tsx.j2
│   └── LowerThird.tsx.j2
├── content/           # Content display components
│   ├── CodeBlock.tsx.j2
│   ├── TypingCode.tsx.j2
│   ├── LineChart.tsx.j2
│   └── DemoBox.tsx.j2
└── layouts/           # Container layout components
    ├── Grid.tsx.j2
    ├── ThreeByThreeGrid.tsx.j2
    ├── AsymmetricLayout.tsx.j2
    └── ... (more layouts)
```

## Documentation Structure

Each component should have its own documentation file:

```
docs/components/
├── COMPONENT_DESIGN.md       # This file
├── overlays/
│   ├── TitleScene.md
│   └── LowerThird.md
├── content/
│   ├── CodeBlock.md
│   ├── TypingCode.md
│   ├── LineChart.md
│   └── DemoBox.md
└── layouts/
    ├── Grid.md
    ├── ThreeByThreeGrid.md
    └── ... (one per layout)
```

See individual component documentation for detailed usage examples and configuration options.
