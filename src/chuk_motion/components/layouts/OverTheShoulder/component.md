# OverTheShoulder

Looking over someone's shoulder perspective for screen recordings

## Overview

The `OverTheShoulder` component is a layout component in the chuk-motion library.

## Properties

### `screen_content`
- Type: `component`
- *Optional* (default: `None`)
- Main screen content

### `shoulder_overlay`
- Type: `component`
- *Optional* (default: `None`)
- Person/shoulder overlay

### `overlay_position`
- Type: `enum`
- *Optional* (default: `bottom-left`)
- Overlay position
- Values: `bottom-left`, `bottom-right`, `top-left`, `top-right`

### `overlay_size`
- Type: `number`
- *Optional* (default: `30`)
- Overlay size (percentage)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
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
remotion_add_overtheshoulder(
    screen_content={'type': 'CodeBlock', 'code': '// Screen'},
    shoulder_overlay={'type': 'CodeBlock', 'code': '// Person'},
    overlay_position="bottom-left",
    overlay_size=30,
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