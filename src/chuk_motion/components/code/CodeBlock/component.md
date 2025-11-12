# CodeBlock

Syntax-highlighted code display with animated entrance

## Overview

The `CodeBlock` component is a code component in the chuk-motion library.

## Variants

### `minimal`
Clean code with subtle background

### `terminal`
Terminal/console styling

### `editor`
IDE/editor styling with line numbers

### `glass`
Glassmorphism effect

## Animations

### `fade_in`
Simple fade in

### `slide_up`
Slide from bottom

### `scale_in`
Scale from center

### `blur_in`
Blur to focus

## Properties

### `code`
- Type: `string`
- **Required**
- Code content to display

### `language`
- Type: `string`
- *Optional* (default: `javascript`)
- Programming language (for syntax highlighting)

### `title`
- Type: `string`
- *Optional* (default: ``)
- Optional title/filename

### `variant`
- Type: `enum`
- *Optional* (default: `editor`)
- Visual style
- Values: `minimal`, `terminal`, `editor`, `glass`

### `animation`
- Type: `enum`
- *Optional* (default: `fade_in`)
- Entrance animation
- Values: `fade_in`, `slide_up`, `scale_in`, `blur_in`

### `show_line_numbers`
- Type: `boolean`
- *Optional* (default: `True`)
- Show line numbers

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
remotion_add_codeblock(
    code="const greeting = 'Hello, World!';
console.log(greeting);",
    language="javascript",
    title="hello.js",
    variant="editor",
    animation="slide_up",
    show_line_numbers=True,
    start_time=3.0,
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

Browse other code components in the [component library](../../../README.md).

---

*Generated documentation for chuk-motion component library*