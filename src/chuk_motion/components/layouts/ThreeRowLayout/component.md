# ThreeRowLayout

Header + Main + Footer arrangements with configurable heights

## Overview

The `ThreeRowLayout` component is a layout component in the chuk-motion library.

## Properties

### `top`
- Type: `component`
- *Optional* (default: `None`)
- Content for top row

### `middle`
- Type: `component`
- *Optional* (default: `None`)
- Content for middle row

### `bottom`
- Type: `component`
- *Optional* (default: `None`)
- Content for bottom row

### `top_height`
- Type: `number`
- *Optional* (default: `25`)
- Top row height (percentage, 0-100)

### `middle_height`
- Type: `number`
- *Optional* (default: `50`)
- Middle row height (percentage, 0-100)

### `bottom_height`
- Type: `number`
- *Optional* (default: `25`)
- Bottom row height (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between rows (pixels)

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
remotion_add_threerowlayout(
    top={'type': 'CodeBlock', 'code': '// Header'},
    middle={'type': 'CodeBlock', 'code': '// Main content'},
    bottom={'type': 'CodeBlock', 'code': '// Footer'},
    top_height=25,
    middle_height=50,
    bottom_height=25,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['App with header and footer', 'Dashboard with title bar', 'Slides with header/footer', 'Content with navigation bars'],
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