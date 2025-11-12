# EndScreen

YouTube end screen with CTAs and video suggestions

## Overview

The `EndScreen` component is a overlay component in the chuk-motion library.

## Variants

### `standard`
Simple layout with video thumbnail and subscribe

### `split`
Split screen with multiple CTAs

### `carousel`
Sliding carousel of videos

### `minimal`
Clean single CTA

## Properties

### `cta_text`
- Type: `string`
- **Required**
- Call-to-action text

### `thumbnail_url`
- Type: `string`
- *Optional* (default: `None`)
- Video thumbnail URL

### `variant`
- Type: `enum`
- *Optional* (default: `standard`)
- Layout variant
- Values: `standard`, `split`, `carousel`, `minimal`

### `duration_seconds`
- Type: `float`
- *Optional* (default: `10.0`)
- Duration (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_endscreen(
    cta_text="Watch Next",
    thumbnail_url="https://example.com/thumb.jpg",
    variant="split",
    duration_seconds=10.0,
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