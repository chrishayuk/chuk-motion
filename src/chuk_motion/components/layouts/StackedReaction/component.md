# StackedReaction

Reaction video style with stacked feeds

## Overview

The `StackedReaction` component is a layout component in the chuk-motion library.

## Properties

### `original_content`
- Type: `component`
- *Optional* (default: `None`)
- Original video/content

### `reaction_content`
- Type: `component`
- *Optional* (default: `None`)
- Reaction video

### `layout`
- Type: `enum`
- *Optional* (default: `vertical`)
- Layout style
- Values: `vertical`, `horizontal`, `pip`

### `reaction_size`
- Type: `number`
- *Optional* (default: `40`)
- Reaction panel size (percentage, 0-100)

### `gap`
- Type: `number`
- *Optional* (default: `20`)
- Gap between panels (pixels)

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
remotion_add_stackedreaction(
    original_content={'type': 'CodeBlock', 'code': '// Original video'},
    reaction_content={'type': 'CodeBlock', 'code': '// Reaction'},
    layout="vertical",
    reaction_size=40,
    gap=20,
    padding=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['Reaction videos', 'Commentary videos', 'Analysis content', 'Review videos'],
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