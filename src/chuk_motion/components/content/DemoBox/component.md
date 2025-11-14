# DemoBox

Simple colored box with label for demos and placeholders

## Overview

The `DemoBox` component is a content component in the chuk-motion library.

## Properties

### `label`
- Type: `string`
- **Required**
- Text label to display

### `color`
- Type: `enum`
- *Optional* (default: `primary`)
- Color theme
- Values: `primary`, `accent`, `secondary`

### `start_time`
- Type: `float`
- *Optional* (default: `None`)
- When to show (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `None`)
- How long to show (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_demobox(
    label="Demo Content",
    color="primary",
    start_time=0.0,
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

## Related Components

Browse other content components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*