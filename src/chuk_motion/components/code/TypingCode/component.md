# TypingCode

Animated typing code effect with cursor

## Overview

The `TypingCode` component is a code component in the chuk-motion library.

## Variants

### `minimal`
Clean typing effect

### `terminal`
Terminal-style with cursor

### `editor`
IDE-style typing

### `hacker`
Matrix/hacker style

## Properties

### `code`
- Type: `string`
- **Required**
- Code to type out

### `language`
- Type: `string`
- *Optional* (default: `javascript`)
- Programming language

### `title`
- Type: `string`
- *Optional* (default: ``)
- Optional title/filename

### `variant`
- Type: `enum`
- *Optional* (default: `editor`)
- Visual style
- Values: `minimal`, `terminal`, `editor`, `hacker`

### `cursor_style`
- Type: `enum`
- *Optional* (default: `line`)
- Cursor appearance
- Values: `block`, `line`, `underline`, `none`

### `typing_speed`
- Type: `enum`
- *Optional* (default: `normal`)
- Typing animation speed
- Values: `slow`, `normal`, `fast`, `instant`

### `show_line_numbers`
- Type: `boolean`
- *Optional* (default: `True`)
- Show line numbers

### `start_time`
- Type: `float`
- **Required**
- When to start (seconds)

### `duration`
- Type: `float`
- *Optional* (default: `10.0`)
- How long to type (seconds)

## Example Usage

### Python (MCP Tool)

```python
remotion_add_typingcode(
    code="function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n-1) + fibonacci(n-2);
}",
    language="javascript",
    title="fibonacci.js",
    variant="editor",
    cursor_style="line",
    typing_speed="normal",
    show_line_numbers=True,
    start_time=2.0,
    duration=8.0,
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