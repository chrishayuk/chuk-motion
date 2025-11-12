# Timeline

Progress/timeline overlay with milestones and progress indicators

## Overview

The `Timeline` component is a layout component in the chuk-motion library.

## Properties

### `main_content`
- Type: `component`
- *Optional* (default: `None`)
- Background content

### `milestones`
- Type: `array`
- *Optional* (default: `None`)
- Milestone objects

### `current_time`
- Type: `number`
- *Optional* (default: `0`)
- Current progress time

### `total_duration`
- Type: `number`
- *Optional* (default: `10`)
- Total duration

### `position`
- Type: `enum`
- *Optional* (default: `bottom`)
- Position
- Values: `top`, `bottom`

### `height`
- Type: `number`
- *Optional* (default: `100`)
- Timeline height (pixels)

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