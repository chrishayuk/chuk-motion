# TitleScene

Full-screen animated title card for video openings

## Overview

The `TitleScene` component is a overlay component in the chuk-motion library.

## Variants

### `minimal`
Clean, simple text on solid background

### `standard`
Text with gradient background

### `bold`
Large text with animated gradient and effects

### `kinetic`
Dynamic text with motion typography

## Animations

### `fade_zoom`
Fade in with subtle zoom

### `slide_up`
Slide up from bottom with blur

### `typewriter`
Character-by-character reveal

### `blur_in`
Blur to sharp focus

### `split`
Text splits from center

## Properties

### `text`
- Type: `string`
- **Required**
- Main title text

### `subtitle`
- Type: `string`
- *Optional* (default: `None`)
- Optional subtitle text

### `variant`
- Type: `enum`
- *Optional* (default: `standard`)
- Visual style variant
- Values: `minimal`, `standard`, `bold`, `kinetic`

### `animation`
- Type: `enum`
- *Optional* (default: `fade_zoom`)
- Animation style
- Values: `fade_zoom`, `slide_up`, `typewriter`, `blur_in`, `split`

### `duration_seconds`
- Type: `float`
- *Optional* (default: `3.0`)
- Duration in seconds

## Example Usage

### Python (MCP Tool)

```python
remotion_add_titlescene(
    text="The Future of AI",
    subtitle="Transforming Technology",
    variant="bold",
    animation="fade_zoom",
    duration_seconds=3.0,
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