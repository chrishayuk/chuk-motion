# WebPage

Render real HTML content with CSS styling - perfect for showing actual web pages

## Overview

The `WebPage` component is a content component in the chuk-motion library.

## Properties

### `html`
- Type: `string`
- *Optional* (default: `<div style="padding: 40px; text-align: center;"><h1>Hello World</h1><p>This is a web page.</p></div>`)
- HTML content to render

### `css`
- Type: `string`
- *Optional* (default: ``)
- Custom CSS styles

### `base_styles`
- Type: `boolean`
- *Optional* (default: `True`)
- Include default styling for common HTML elements

### `scale`
- Type: `float`
- *Optional* (default: `1.0`)
- Zoom level (1.0 = 100%)

### `scroll_y`
- Type: `float`
- *Optional* (default: `0`)
- Vertical scroll position in pixels

### `animate_scroll`
- Type: `boolean`
- *Optional* (default: `False`)
- Animate scroll from 0 to scroll_y

### `scroll_duration`
- Type: `float`
- *Optional* (default: `60`)
- Duration of scroll animation in frames

### `theme`
- Type: `enum`
- *Optional* (default: `light`)
- Visual theme
- Values: `light`, `dark`

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
remotion_add_webpage(
    html="<div style="max-width: 1200px; margin: 0 auto;">
  <header style="text-align: center; padding: 60px 0;">
    <h1>Welcome to Our Product</h1>
    <p style="font-size: 20px; opacity: 0.8;">The best solution for your needs</p>
    <button>Get Started</button>
  </header>

  <section style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 40px;">
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature One</h3>
      <p>Amazing capability that solves your problem.</p>
    </div>
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature Two</h3>
      <p>Another incredible feature you'll love.</p>
    </div>
    <div style="padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
      <h3>Feature Three</h3>
      <p>The feature that ties it all together.</p>
    </div>
  </section>
</div>",
    css="h1 { color: #333; font-size: 48px; }
button { background: #0066ff; color: white; padding: 12px 24px; border-radius: 6px; }",
    base_styles=True,
    scale=1.0,
    scroll_y=0,
    animate_scroll=False,
    theme="light",
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