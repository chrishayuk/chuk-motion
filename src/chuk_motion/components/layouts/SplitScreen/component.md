# SplitScreen

Layout component for side-by-side content

## Overview

The `SplitScreen` component is a layout component in the chuk-motion library.

## Properties

### `orientation`
- Type: `enum`
- *Optional* (default: `horizontal`)
- Split direction
- Values: `horizontal`, `vertical`

### `layout`
- Type: `enum`
- *Optional* (default: `50-50`)
- Size ratio
- Values: `50-50`, `60-40`, `40-60`, `70-30`, `30-70`

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between panels (pixels)

### `left_content`
- Type: `component`
- **Required**
- Component for left/top panel

### `right_content`
- Type: `component`
- **Required**
- Component for right/bottom panel

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
remotion_add_splitscreen(
    orientation="horizontal",
    layout="50-50",
    gap=20,
    left_content={'type': 'CodeBlock', 'code': '...'},
    right_content={'type': 'Terminal', 'output': '...'},
    start_time=0.0,
    duration=10.0,
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