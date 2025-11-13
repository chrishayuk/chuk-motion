# LayoutEntrance

**Category:** Animation
**Purpose:** Universal entrance animation wrapper for any layout

## Overview

LayoutEntrance is a zero-config way to add polish to any layout or component. It wraps any content and animates it in using motion token-driven animations. Works with Grid, Container, Timeline, or any other component.

## Entrance Types

### none
No animation (instant appearance).
- **Use for:** When you need instant visibility

### fade_in
Simple fade from 0 to 1 opacity.
- **Feel:** Subtle, professional, clean
- **Use for:** Text, overlays, subtle entrances
- **Motion tokens:** `ease_out` easing, `normal` duration (0.35s)

### fade_slide_up
Fade in while sliding up 30px.
- **Feel:** Content rising, modern, polished
- **Use for:** Content blocks, cards, sections
- **Motion tokens:** `ease_out_expo` easing, `medium` duration (0.5s)

### scale_in_soft
Subtle scale from 0.95 to 1.0 with fade.
- **Feel:** Elegant, refined, gentle
- **Use for:** Professional content, subtle emphasis
- **Motion tokens:** `ease_out` easing, `medium` duration

### scale_in_pop
Pop scale from 0.9 → 1.05 → 1.0 with spring bounce.
- **Feel:** Playful, energetic, fun
- **Use for:** Creator content, playful reveals, notifications
- **Motion tokens:** `smooth` spring (default)

### slide_in_left
Slide from left with fade.
- **Feel:** Directional, spatial, modern
- **Use for:** Side panels, nav menus, sequential reveals
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### slide_in_right
Slide from right with fade.
- **Feel:** Reverse flow, alternative direction
- **Use for:** Side panels, alternate reveals
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### blur_in
Fade from 20px blur to sharp.
- **Feel:** Dramatic, cinematic, hero entrance
- **Use for:** Hero images, backgrounds, dramatic moments
- **Motion tokens:** `ease_out` easing, `slow` duration (0.7s)

### zoom_in
Zoom from 0 to 100% scale.
- **Feel:** Explosive, dramatic, attention-grabbing
- **Use for:** Hero elements, dramatic entrances, focus moments
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

## Parameters

- **content**: Layout or component to animate in (any component)
- **entrance_type**: One of the 9 entrance types above
- **entrance_delay**: Delay before entrance starts (seconds) - default: 0.0
- **duration**: Total clip duration (seconds) - default: 5.0

## Motion Token Integration

Token-first design with consistent timing:
- **Durations:** `normal` (0.35s), `medium` (0.5s), `slow` (0.7s)
- **Easings:** `ease_out`, `ease_out_expo`, `ease_out_back`
- **Springs:** `smooth` spring for pop effects

## Examples

```python
# Fade-slide entrance for Grid
{
    "type": "LayoutEntrance",
    "config": {
        "content": {"type": "Grid", "config": {"layout": "3x3", "items": [...]}},
        "entrance_type": "fade_slide_up",
        "entrance_delay": 0.2
    }
}

# Pop entrance for Container
{
    "type": "LayoutEntrance",
    "config": {
        "content": {"type": "Container", "config": {...}},
        "entrance_type": "scale_in_pop"
    }
}

# Dramatic blur entrance for Timeline
{
    "type": "LayoutEntrance",
    "config": {
        "content": {"type": "Timeline", "config": {...}},
        "entrance_type": "blur_in",
        "entrance_delay": 0.5
    }
}
```

## Best Practices

1. **Use fade_in as default** - subtle and professional
2. **Use fade_slide_up for cards/blocks** - familiar motion pattern
3. **Use scale_in_pop sparingly** - it's energetic and playful
4. **Use blur_in for hero moments** - dramatic and cinematic
5. **Add entrance_delay (0.1-0.5s)** to prevent instant pop-in
6. **Match entrance to content tone:** formal = fade_in, playful = scale_in_pop

## Common Use Cases

- **Adding polish to layouts** without custom animation
- **Consistent entrance patterns** across all layouts
- **Zero-config animation** for rapid prototyping
- **Professional transitions** with minimal setup
- **Platform-optimized timing** via motion tokens
