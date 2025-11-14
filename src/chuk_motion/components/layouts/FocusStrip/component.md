# FocusStrip

Focused strip/banner layout for highlighting key content

## Overview

The `FocusStrip` component is a layout component in the chuk-motion library.

## Properties

### `main_content`
- Type: `component`
- *Optional* (default: `None`)
- Background/context content

### `focus_content`
- Type: `component`
- *Optional* (default: `None`)
- Focused strip content

### `position`
- Type: `enum`
- *Optional* (default: `center`)
- Strip position
- Values: `top`, `center`, `bottom`

### `strip_height`
- Type: `number`
- *Optional* (default: `30`)
- Strip height (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap (pixels)

### `padding`
- Type: `number`
- *Optional* (default: `40`)
- Padding around layout (pixels)

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
remotion_add_focusstrip(
    main_content={'type': 'CodeBlock', 'code': '// Background'},
    focus_content={'type': 'CodeBlock', 'code': '// Key message'},
    position="center",
    strip_height=30,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['Caption overlays', 'Quote highlights', 'Code snippets', 'Key message banners'],
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

- Respect platform safe margins
- Test with actual content before finalizing
- Consider aspect ratio and target platform
- Balance content density with readability

## Related Components

Browse other layout components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*