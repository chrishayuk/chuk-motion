# ThreeByThreeGrid

Perfect 3x3 grid layout (9 cells)

## Overview

The `ThreeByThreeGrid` component is a layout component in the chuk-motion library.

## Properties

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between items (pixels)

### `padding`
- Type: `number`
- *Optional* (default: `40`)
- Padding around grid (pixels)

### `items`
- Type: `array`
- **Required**
- Array of up to 9 components to display

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
remotion_add_threebythreegrid(
    gap=20,
    padding=40,
    items=[{'type': 'CodeBlock', 'code': 'Python'}, {'type': 'CodeBlock', 'code': 'JavaScript'}, {'type': 'CodeBlock', 'code': 'Rust'}, {'type': 'CodeBlock', 'code': 'Go'}, {'type': 'CodeBlock', 'code': 'TypeScript'}, {'type': 'CodeBlock', 'code': 'Swift'}, {'type': 'CodeBlock', 'code': 'Kotlin'}, {'type': 'CodeBlock', 'code': 'Ruby'}, {'type': 'CodeBlock', 'code': 'C++'}],
    start_time=0.0,
    duration=10.0,
    use_cases=['Portfolio showcase (9 projects)', 'Language comparison', 'Instagram-style grid', 'Feature showcase', 'Social media style display'],
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