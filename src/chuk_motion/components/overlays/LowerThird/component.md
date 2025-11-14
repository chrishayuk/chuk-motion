# LowerThird

Name plate overlay with title and subtitle (like TV graphics)

## Overview

The `LowerThird` component is a overlay component in the chuk-motion library.

## Variants

### `minimal`
Simple text on subtle background

### `standard`
Text with clean bar background

### `glass`
Glassmorphism effect with blur

### `bold`
High contrast with accent colors

### `animated`
Dynamic sliding animation

## Properties

### `name`
- Type: `string`
- **Required**
- Main name/text (larger)

### `title`
- Type: `string`
- *Optional* (default: `None`)
- Subtitle/title (smaller, below name)

### `variant`
- Type: `enum`
- *Optional* (default: `glass`)
- Visual style
- Values: `minimal`, `standard`, `glass`, `bold`, `animated`

### `position`
- Type: `enum`
- *Optional* (default: `bottom_left`)
- Screen position
- Values: `bottom_left`, `bottom_center`, `bottom_right`, `top_left`, `top_center`

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
remotion_add_lowerthird(
    name="Dr. Sarah Chen",
    title="AI Researcher, Stanford",
    variant="glass",
    position="bottom_left",
    start_time=2.0,
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

- Keep text concise and readable
- Test animations at target frame rate
- Consider platform safe margins for social media
- Match animation style to overall video aesthetic

## Related Components

Browse other overlay components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*