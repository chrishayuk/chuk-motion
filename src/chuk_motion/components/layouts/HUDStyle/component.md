# HUDStyle

Heads-up display style with overlay elements

## Overview

The `HUDStyle` component is a layout component in the chuk-motion library.

## Properties

### `main_content`
- Type: `component`
- *Optional* (default: `None`)
- Main background content

### `top_left`
- Type: `component`
- *Optional* (default: `None`)
- Top-left overlay

### `top_right`
- Type: `component`
- *Optional* (default: `None`)
- Top-right overlay

### `bottom_left`
- Type: `component`
- *Optional* (default: `None`)
- Bottom-left overlay

### `bottom_right`
- Type: `component`
- *Optional* (default: `None`)
- Bottom-right overlay

### `center`
- Type: `component`
- *Optional* (default: `None`)
- Center overlay

### `overlay_size`
- Type: `number`
- *Optional* (default: `15`)
- Corner overlay size (%)

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