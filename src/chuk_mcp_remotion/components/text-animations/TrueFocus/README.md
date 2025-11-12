# TrueFocus Text Animation Component

Dramatic text animation component inspired by [ReactBits TrueFocus](https://www.reactbits.dev/text-animations/true-focus), reimplemented for Remotion with full design system integration.

## Overview

TrueFocus creates a captivating word-by-word focus effect where:
- Text is split into individual words
- One word at a time receives focus (sharp) while others are blurred
- Animated corner brackets with glow effect highlight the focused word
- Smooth transitions cycle through all words

Perfect for: Taglines, key messages, dramatic reveals, call-to-action emphasis

## Design System Compliance

✅ **100% Design Token Compliant** - No hardcoded values

### Tokens Used

**Typography:**
- `typography.font_sizes[resolution].{xl|2xl|3xl|4xl}` - Text sizes
- `typography.font_weights.{bold|extrabold|black}` - Text weights
- `typography.primary_font.fonts` - Font family
- `typography.letter_spacing.tight` - Letter spacing
- `typography.line_heights.tight` - Line height

**Colors:**
- `colors.text.on_dark` - Default text color
- `colors.primary[0]` - Default frame/glow color

**Spacing:**
- `spacing.spacing.{sm|lg|xl|3xl}` - Padding and gaps
- `spacing.spacing.xs` - Glow spread
- `spacing.border_width.thick` - Frame borders
- `spacing.border_radius.xs` - Corner radius

**Motion:**
- `motion.default_spring.config.*` - Spring animation config

## Usage

### MCP Tool

```python
remotion_add_true_focus(
    text="Innovation Through Excellence",
    font_size="3xl",
    word_duration=1.5,
    position="center",
    duration=6.0
)
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | string | Required | Text to animate (will be split into words) |
| `font_size` | `xl\|2xl\|3xl\|4xl` | `"3xl"` | Size of text |
| `font_weight` | `bold\|extrabold\|black` | `"black"` | Weight of text |
| `text_color` | string | Theme color | Text color override |
| `frame_color` | string | Primary color | Corner bracket color |
| `glow_color` | string | Primary color | Glow effect color |
| `blur_amount` | number | `5.0` | Blur intensity for inactive words (px) |
| `word_duration` | number | `1.0` | Duration each word stays focused (seconds) |
| `position` | `center\|top\|bottom` | `"center"` | Vertical position |
| `duration` | number/string | `5.0` | Total duration |
| `track` | string | `"overlay"` | Track name |

## Examples

### Basic Center Position
```python
remotion_add_true_focus(
    text="Transform Your Vision",
    font_size="3xl",
    word_duration=1.5,
    position="center"
)
```

### Large Text with Fast Cycle
```python
remotion_add_true_focus(
    text="Think Different Act Bold",
    font_size="4xl",
    word_duration=0.8,  # Faster cycling
    blur_amount=7
)
```

### Custom Colors
```python
remotion_add_true_focus(
    text="The Future Is Now",
    font_size="3xl",
    text_color="#FFFFFF",
    frame_color="#00D9FF",
    glow_color="#00D9FF",
    blur_amount=6
)
```

### Top Position for Headers
```python
remotion_add_true_focus(
    text="Powered by Advanced Technology",
    font_size="2xl",
    position="top",
    word_duration=1.0
)
```

## Animation Details

### Word Cycling
- Words are automatically cycled based on `word_duration`
- Smooth spring-based transitions between words
- Frame opacity animates with spring physics

### Blur Effect
- Inactive words receive CSS `blur()` filter
- Smooth `0.3s ease` transition between focused/blurred states
- Configurable blur intensity (default: 5px)

### Corner Brackets
- Four animated corner brackets (top-left, top-right, bottom-left, bottom-right)
- Each corner shows two borders forming an "L" shape
- Drop shadow creates glow effect around brackets
- Opacity animates with spring physics for smooth appearance

### Positioning
- **Center:** Centered horizontally and vertically
- **Top:** Centered horizontally, top-aligned with padding
- **Bottom:** Centered horizontally, bottom-aligned with padding

## Technical Implementation

### Frame-Based Animation
Uses Remotion's `useCurrentFrame()` for precise timing:
```typescript
const cycleProgress = (relativeFrame / wordDuration) % wordCount;
const currentWordIndex = Math.floor(cycleProgress);
```

### Spring Physics
Smooth transitions using Remotion's `spring()`:
```typescript
const smoothTransition = spring({
  frame: transitionProgress * fps / 2,
  fps,
  config: {
    damping: motion.default_spring.config.damping,
    stiffness: motion.default_spring.config.stiffness,
    mass: motion.default_spring.config.mass,
  },
});
```

### Design Token Integration
All styling values resolve from design system:
```typescript
fontSize: parseInt(typography.font_sizes[resolution]['3xl'])
fontWeight: typography.font_weights.black
color: colors.text.on_dark
```

## Demo

Run the comprehensive demo:
```bash
python examples/true_focus_demo.py
cd remotion-projects/true_focus_demo
npm install && npm start
```

The demo showcases:
- Multiple font sizes (2xl, 3xl, 4xl)
- All three positions (center, top, bottom)
- Different cycle speeds (fast, normal, slow)
- Custom color configurations
- Combined with other components

## Comparison to Original

| Feature | ReactBits Original | Our Implementation |
|---------|-------------------|-------------------|
| Platform | React DOM | Remotion (video) |
| Animation | State + Framer Motion | Frame-based + Spring |
| Interaction | Hover-based | Time-based (automatic) |
| Styling | CSS + Custom props | Design tokens |
| Colors | Hardcoded | Token-based with overrides |
| Typography | Hardcoded | Token-based scaling |
| Blur | CSS filter | CSS filter |
| Corners | Framer Motion | CSS positioned divs |

## Best Practices

1. **Word Duration:** Aim for 1-2 seconds per word for readability
2. **Text Length:** Works best with 3-7 words
3. **Font Size:** Use larger sizes (3xl, 4xl) for impact
4. **Blur Amount:** 5-8px works well; higher values for more drama
5. **Position:** Center for maximum impact, top/bottom for overlays
6. **Colors:** Use high contrast for visibility

## Performance

- Lightweight: Only animates CSS properties (blur, opacity, position)
- No heavy computations per frame
- Efficient word splitting (memoized)
- Minimal re-renders

## Accessibility

- High contrast text by default
- Clear visual focus on active word
- Configurable blur for readability
- Works with all theme colors

## Credits

Original concept: [ReactBits TrueFocus](https://github.com/DavidHDev/react-bits) by David Huertas
Remotion adaptation: Reimplemented with design system tokens
