# TextOverlay

Animated text overlay for emphasis and captions

## Overview

The `TextOverlay` component is a overlay component in the chuk-motion library.

## Animations

### `blur_in`
Blur to focus

### `slide_up`
Slide from bottom

### `fade`
Simple fade in/out

### `typewriter`
Character reveal

### `scale_in`
Scale from center

## Properties

### `text`
- Type: `string`
- **Required**
- Text content

### `style`
- Type: `enum`
- *Optional* (default: `emphasis`)
- Text style
- Values: `emphasis`, `caption`, `callout`, `subtitle`, `quote`

### `animation`
- Type: `enum`
- *Optional* (default: `blur_in`)
- Animation style
- Values: `blur_in`, `slide_up`, `fade`, `typewriter`, `scale_in`

### `start_time`
- Type: `float`
- **Required**
- When to show (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `3.0`)
- How long to show (seconds)

### `position`
- Type: `string`
- *Optional* (default: `center`)
- Position (center, top, bottom, custom)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_textoverlay(
    text="Mind. Blown. ??",
    style="emphasis",
    animation="scale_in",
    start_time=5.0,
    duration=2.0,
    position="center",
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