# Mosaic

Irregular collage with layered clips in various artistic arrangements

## Overview

The `Mosaic` component is a layout component in the chuk-motion library.

## Properties

### `clips`
- Type: `array`
- *Optional* (default: `None`)
- Clip objects with {content, size, position, z_index}

### `style`
- Type: `enum`
- *Optional* (default: `hero-corners`)
- Mosaic style
- Values: `hero-corners`, `stacked`, `spotlight`

### `gap`
- Type: `number`
- *Optional* (default: `10`)
- Gap (pixels)

### `padding`
- Type: `number`
- *Optional* (default: `40`)
- Padding (pixels)

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