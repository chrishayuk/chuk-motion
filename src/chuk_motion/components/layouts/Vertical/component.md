# Vertical

9:16 optimized for Shorts/TikTok/Reels with multiple layout styles

## Overview

The `Vertical` component is a layout component in the chuk-motion library.

## Properties

### `top`
- Type: `component`
- *Optional* (default: `None`)
- Top content

### `bottom`
- Type: `component`
- *Optional* (default: `None`)
- Bottom content

### `layout_style`
- Type: `enum`
- *Optional* (default: `top-bottom`)
- Layout style
- Values: `top-bottom`, `caption-content`, `content-caption`, `split-vertical`

### `top_ratio`
- Type: `number`
- *Optional* (default: `50`)
- Top section ratio (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between sections (pixels)

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
remotion_add_vertical(
    top={'type': 'CodeBlock', 'code': '// Content'},
    bottom={'type': 'CodeBlock', 'code': '// Caption'},
    layout_style="content-caption",
    top_ratio=70,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['YouTube Shorts', 'TikTok videos', 'Instagram Reels', 'Mobile-first content'],
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