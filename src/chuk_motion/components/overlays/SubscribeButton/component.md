# SubscribeButton

Animated subscribe button overlay (YouTube-specific)

## Overview

The `SubscribeButton` component is a overlay component in the chuk-motion library.

## Animations

### `bounce`
Bouncy spring animation

### `glow`
Pulsing glow effect

### `pulse`
Scale pulse

### `slide`
Slide in from side

### `wiggle`
Attention-grabbing wiggle

## Properties

### `variant`
- Type: `enum`
- *Optional* (default: `standard`)
- Button style
- Values: `minimal`, `standard`, `animated`, `3d`

### `animation`
- Type: `enum`
- *Optional* (default: `bounce`)
- Animation style
- Values: `bounce`, `glow`, `pulse`, `slide`, `wiggle`

### `position`
- Type: `enum`
- *Optional* (default: `bottom_right`)
- Screen position
- Values: `bottom_right`, `bottom_center`, `center`, `top_right`

### `start_time`
- Type: `float`
- **Required**
- When to show (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `3.0`)
- How long to show (seconds)

### `custom_text`
- Type: `string`
- *Optional* (default: `SUBSCRIBE`)
- Custom button text

## Example Usage

### Python (MCP Tool)

```python
remotion_add_subscribebutton(
    variant="animated",
    animation="bounce",
    position="bottom_right",
    start_time=10.0,
    duration=3.0,
    custom_text="SUBSCRIBE",
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

- Keep text concise and readable
- Test animations at target frame rate
- Consider platform safe margins for social media
- Match animation style to overall video aesthetic

## Related Components

Browse other overlay components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*