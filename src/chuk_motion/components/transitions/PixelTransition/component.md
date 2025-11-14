# PixelTransition

**Category:** Transition
**Purpose:** Pixelated dissolve transition effect between two pieces of content

## Overview

PixelTransition creates a retro-style pixelated dissolve effect between any two pieces of content. Pixels animate in with random stagger to cover the first content, then animate out to reveal the second content. Perfect for adding a unique, attention-grabbing transition style to your videos.

## How It Works

The transition happens in three phases:

1. **Phase 1 - Pixels Fade In:** Square pixels randomly stagger in to cover the first content
2. **Phase 2 - Content Switch:** While pixels are fully visible, content switches from first to second
3. **Phase 3 - Pixels Fade Out:** Pixels randomly stagger out to reveal the second content

## Parameters

- **first_content**: First content component (shown initially)
- **second_content**: Second content component (revealed after transition)
- **grid_size**: Number of pixels per row/column (default: 10 = 10x10 = 100 pixels)
- **pixel_color**: Color of transition pixels (uses primary color if not specified)
- **transition_start**: When to start transition in seconds (default: 2.0)
- **transition_duration**: Duration of transition animation in seconds (default: 1.0)
- **duration**: Total clip duration in seconds (default: 5.0)

## Design Token Integration

- **Colors:** Uses `primary[0]` color by default for pixels
- **Timing:** Random stagger creates organic, unpredictable animation feel

## Grid Size Guide

- **grid_size: 5-8** - Large pixels, dramatic, retro 8-bit feel
- **grid_size: 10-12** - Medium pixels, balanced, modern retro
- **grid_size: 15-20** - Small pixels, subtle, refined dissolve

## Examples

```python
# Basic pixel transition between title cards
{
    "type": "PixelTransition",
    "config": {
        "first_content": {"type": "TitleScene", "config": {"text": "Before", "variant": "bold"}},
        "second_content": {"type": "TitleScene", "config": {"text": "After", "variant": "glass"}},
        "grid_size": 12,
        "transition_start": 2.0,
        "transition_duration": 1.0,
        "duration": 5.0
    }
}

# Transition between chart and text with custom color
{
    "type": "PixelTransition",
    "config": {
        "first_content": {"type": "BarChart", "config": {"data": [...], "title": "Sales Data"}},
        "second_content": {"type": "TextOverlay", "config": {"text": "Record Growth", "size": "large"}},
        "grid_size": 15,
        "pixel_color": "#00D9FF"
    }
}

# Retro 8-bit style transition
{
    "type": "PixelTransition",
    "config": {
        "first_content": {"type": "CodeBlock", "config": {...}},
        "second_content": {"type": "Grid", "config": {...}},
        "grid_size": 6,
        "pixel_color": "#FF00FF",
        "transition_duration": 1.5
    }
}
```

## Best Practices

1. **Use grid_size 10-12** for most transitions (balanced, professional)
2. **Lower grid_size (5-8)** for retro, playful, dramatic effect
3. **Higher grid_size (15-20)** for subtle, refined transitions
4. **Match pixel_color to theme** - use brand colors or accent colors
5. **Keep transition_duration 0.8-1.5s** for optimal viewing
6. **Use for scene transitions** where you want to add personality and style

## Common Use Cases

- **Scene transitions** with personality
- **Content reveals** with impact
- **Before/after showcases**
- **Dramatic content switches**
- **Retro-style transitions**
- **Gaming or tech content** (8-bit feel)
- **Creative transitions** for social media

## Visual Feel

- **Retro:** Reminiscent of 8-bit games and early digital graphics
- **Playful:** Random stagger creates organic, unpredictable movement
- **Attention-grabbing:** Unique effect that stands out from standard transitions
- **Flexible:** Works with any content type (layouts, scenes, components)
