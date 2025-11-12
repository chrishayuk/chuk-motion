# BarChart

Animated vertical bar chart for comparing categories

## Overview

The `BarChart` component is a chart component in the chuk-motion library.

## Animations

### `draw`
Chart draws with animation

### `fade_in`
Chart fades in

### `scale_in`
Chart scales from center

## Properties

### `data`
- Type: `array`
- **Required**
- List of objects with label, value, and optional color

### `title`
- Type: `string`
- *Optional* (default: ``)
- Optional chart title

### `xlabel`
- Type: `string`
- *Optional* (default: ``)
- Optional x-axis label

### `ylabel`
- Type: `string`
- *Optional* (default: ``)
- Optional y-axis label

### `start_time`
- Type: `float`
- **Required**
- When to show (seconds)

### `duration`
- Type: `float`
- **Required**
- How long to animate (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_barchart(
    data=[
        {
                "label": "Q1",
                "value": 45
        },
        {
                "label": "Q2",
                "value": 67
        }
],
    title="Example Chart",
    duration=4.0
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