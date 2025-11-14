# LineChart

Animated line chart for data visualization with smooth drawing animation

## Overview

The `LineChart` component is a chart component in the chuk-motion library.

## Animations

### `draw`
Line draws from left to right

### `fade_in`
Chart fades in

### `scale_in`
Chart scales from center

### `points_sequence`
Points appear sequentially

## Properties

### `data`
- Type: `array`
- **Required**
- Array of data points [x, y] or {x, y, label}

### `title`
- Type: `string`
- *Optional* (default: ``)
- Chart title

### `xlabel`
- Type: `string`
- *Optional* (default: ``)
- X-axis label

### `ylabel`
- Type: `string`
- *Optional* (default: ``)
- Y-axis label

### `start_time`
- Type: `float`
- **Required**
- When to show (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `4.0`)
- How long to animate (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_linechart(
    data=[[0, 10], [1, 25], [2, 45], [3, 70], [4, 90]],
    title="User Growth",
    xlabel="Month",
    ylabel="Users (thousands)",
    start_time=8.0,
    duration=4.0,
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

- Keep data concise for readability on video
- Use contrasting colors for better visibility
- Consider animation duration based on data complexity
- Test at your target resolution (1080p, 4K)

## Related Components

Browse other chart components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*