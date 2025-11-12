# Container

Flexible positioning container for components

## Overview

The `Container` component is a layout component in the chuk-motion library.

## Properties

### `position`
- Type: `enum`
- *Optional* (default: `center`)
- Position on screen
- Values: `center`, `top-left`, `top-center`, `top-right`, `middle-left`, `middle-right`, `bottom-left`, `bottom-center`, `bottom-right`

### `width`
- Type: `string`
- *Optional* (default: `auto`)
- Width (px, %, or auto)

### `height`
- Type: `string`
- *Optional* (default: `auto`)
- Height (px, %, or auto)

### `padding`
- Type: `number`
- *Optional* (default: `40`)
- Internal padding (pixels)

### `content`
- Type: `component`
- **Required**
- Component to position

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
remotion_add_container(
    position="top-right",
    width="400px",
    height="auto",
    padding=20,
    content={'type': 'CodeBlock', 'code': '...'},
    start_time=0.0,
    duration=5.0,
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