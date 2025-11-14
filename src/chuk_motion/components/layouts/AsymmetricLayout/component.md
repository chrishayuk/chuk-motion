# AsymmetricLayout

Main feed (2/3) + two demo panels (1/3 stacked) - perfect for tutorials

## Overview

The `AsymmetricLayout` component is a layout component in the chuk-motion library.

## Properties

### `main`
- Type: `component`
- *Optional* (default: `None`)
- Main content area

### `top_side`
- Type: `component`
- *Optional* (default: `None`)
- Top sidebar content

### `bottom_side`
- Type: `component`
- *Optional* (default: `None`)
- Bottom sidebar content

### `layout`
- Type: `enum`
- *Optional* (default: `main-left`)
- Layout variant
- Values: `main-left`, `main-right`

### `main_ratio`
- Type: `number`
- *Optional* (default: `66.67`)
- Main content width (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between panels (pixels)

### `padding`
- Type: `number`
- *Optional* (default: `40`)
- Padding around layout (pixels)

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

```python
remotion_add_asymmetriclayout(
    main={'type': 'CodeBlock', 'code': '// Main tutorial content'},
    top_side={'type': 'CodeBlock', 'code': '// Output'},
    bottom_side={'type': 'CodeBlock', 'code': '// Preview'},
    layout="main-left",
    main_ratio=66.67,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['Code tutorials with output/preview', 'Main content with supplementary panels', 'Demo videos with multi-view', 'Before/after comparisons'],
)
```

### TSX (Generated)

The component generates TypeScript/React code that integrates with Remotion.

## Design Tokens

This component uses the chuk-motion design token system for consistent styling:

- **Colors**: Theme-aware color palettes
- **Typography**: Video-optimized font scales
- **Motion**: Spring physics and easing curves
- **Spacing**: Consistent spacing and safe margins

## Tips & Best Practices

- Respect platform safe margins
- Test with actual content before finalizing
- Consider aspect ratio and target platform
- Balance content density with readability

## Related Components

Browse other layout components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*