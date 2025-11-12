# Counter

Animated number counter for statistics and metrics

## Overview

The `Counter` component is a animation component in the chuk-motion library.

## Animations

### `count_up`
Count from start to end value

### `flip`
Digit flip animation

### `slot_machine`
Slot machine roll effect

### `digital`
Digital display style

## Properties

### `start_value`
- Type: `number`
- *Optional* (default: `0`)
- Starting number

### `end_value`
- Type: `number`
- **Required**
- Ending number

### `prefix`
- Type: `string`
- *Optional* (default: ``)
- Text before number (e.g., '$')

### `suffix`
- Type: `string`
- *Optional* (default: ``)
- Text after number (e.g., 'M', '%')

### `decimals`
- Type: `integer`
- *Optional* (default: `0`)
- Number of decimal places

### `animation`
- Type: `enum`
- *Optional* (default: `count_up`)
- Animation style
- Values: `count_up`, `flip`, `slot_machine`, `digital`

### `start_time`
- Type: `float`
- **Required**
- When to start (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `2.0`)
- Animation duration (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_counter(
    start_value=0,
    end_value=1000000,
    prefix="",
    suffix="+ users",
    decimals=0,
    animation="count_up",
    start_time=5.0,
    duration=2.0,
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

## Related Components

Browse other animation components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*