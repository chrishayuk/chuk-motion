# ThreeColumnLayout

Sidebar + Main + Sidebar arrangements with configurable widths

## Overview

The `ThreeColumnLayout` component is a layout component in the chuk-motion library.

## Properties

### `left`
- Type: `component`
- *Optional* (default: `None`)
- Content for left column

### `center`
- Type: `component`
- *Optional* (default: `None`)
- Content for center column

### `right`
- Type: `component`
- *Optional* (default: `None`)
- Content for right column

### `left_width`
- Type: `number`
- *Optional* (default: `25`)
- Left column width (percentage, 0-100)

### `center_width`
- Type: `number`
- *Optional* (default: `50`)
- Center column width (percentage, 0-100)

### `right_width`
- Type: `number`
- *Optional* (default: `25`)
- Right column width (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between columns (pixels)

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
remotion_add_threecolumnlayout(
    left={'type': 'CodeBlock', 'code': '// Sidebar'},
    center={'type': 'CodeBlock', 'code': '// Main content'},
    right={'type': 'CodeBlock', 'code': '// Sidebar'},
    left_width=25,
    center_width=50,
    right_width=25,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['Dashboard with sidebars', 'Documentation with table of contents', 'App with navigation panels', 'Content with supplementary info'],
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