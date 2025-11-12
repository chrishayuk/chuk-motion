# StylizedWebPage

Stylized webpage mockup with header, sidebar, content blocks, and footer

## Overview

The `StylizedWebPage` component is a content component in the chuk-motion library.

## Properties

### `title`
- Type: `string`
- *Optional* (default: `Website Title`)
- Page title displayed in header

### `subtitle`
- Type: `string`
- *Optional* (default: `Tagline or description`)
- Hero section subtitle

### `show_header`
- Type: `boolean`
- *Optional* (default: `True`)
- Show header/navbar

### `show_sidebar`
- Type: `boolean`
- *Optional* (default: `False`)
- Show sidebar navigation

### `show_footer`
- Type: `boolean`
- *Optional* (default: `False`)
- Show footer

### `header_text`
- Type: `string`
- *Optional* (default: `Navigation`)
- Text in header nav area

### `sidebar_items`
- Type: `array`
- *Optional* (default: `['Dashboard', 'Analytics', 'Settings']`)
- List of sidebar navigation items

### `content_lines`
- Type: `array`
- *Optional* (default: `['Welcome to our site', 'Explore our features', 'Get started today']`)
- Main content block text lines

### `footer_text`
- Type: `string`
- *Optional* (default: `© 2024 Company`)
- Footer text

### `theme`
- Type: `enum`
- *Optional* (default: `light`)
- Visual theme
- Values: `light`, `dark`

### `accent_color`
- Type: `enum`
- *Optional* (default: `primary`)
- Accent color theme
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
remotion_add_stylizedwebpage(
    title="My Amazing App",
    subtitle="Build something incredible",
    show_header=True,
    show_sidebar=True,
    show_footer=True,
    header_text="Home • About • Contact",
    sidebar_items=['Dashboard', 'Analytics', 'Settings', 'Profile'],
    content_lines=['Welcome to our platform', 'Discover powerful features', 'Get started in minutes'],
    footer_text="© 2024 My Company",
    theme="light",
    accent_color="primary",
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