# PiP

Picture-in-Picture webcam overlay with customizable positions

## Overview

The `PiP` component is a layout component in the chuk-motion library.

## Properties

### `main_content`
- Type: `component`
- *Optional* (default: `None`)
- Main background content

### `pip_content`
- Type: `component`
- *Optional* (default: `None`)
- Picture-in-picture overlay content

### `position`
- Type: `enum`
- *Optional* (default: `bottom-right`)
- Overlay position
- Values: `bottom-right`, `bottom-left`, `top-right`, `top-left`

### `overlay_size`
- Type: `number`
- *Optional* (default: `20`)
- Overlay size (percentage of screen, 0-100)

### `margin`
- Type: `number`
- *Optional* (default: `40`)
- Margin from edges (pixels)

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
remotion_add_pip(
    main_content={'type': 'CodeBlock', 'code': '// Main content'},
    pip_content={'type': 'CodeBlock', 'code': '// Webcam'},
    position="bottom-right",
    overlay_size=20,
    margin=40,
    start_time=0.0,
    duration=10.0,
    use_cases=['Tutorial with webcam overlay', 'Screen recording with presenter', 'Reaction videos', 'Live commentary over content'],
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