# LayoutTransition

**Category:** Transition
**Purpose:** Animated scene-to-scene layout transitions with motion token integration

## Overview

LayoutTransition creates smooth, professional transitions between any two layouts or scenes. Built with a token-first approach, all timing and easing use the motion token system for consistency across your video.

## Transition Types

### crossfade
Smooth opacity blend between layouts.
- **Feel:** Subtle, professional, elegant
- **Use for:** Scene changes, subtle transitions, professional content
- **Motion tokens:** `ease_out_quint` easing

### slide_horizontal
Horizontal slide transition (push old layout left, slide new layout in from right).
- **Feel:** Sequential, familiar, directional
- **Use for:** Chapter transitions, slides, sequential content
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### slide_vertical
Vertical slide transition (push old layout up, slide new layout in from bottom).
- **Feel:** Vertical flow, mobile-like, modern
- **Use for:** Vertical/Shorts content, scrolling reveals
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### cube_rotate
3D cube rotation effect with perspective.
- **Feel:** Dramatic, 3D, attention-grabbing
- **Use for:** Major scene changes, dramatic reveals, showcase transitions
- **Motion tokens:** `ease_in_out_quart` easing (S-curve), `slow` duration

### parallax_push
Parallax depth effect (background moves slower than foreground).
- **Feel:** Depth, layered, cinematic
- **Use for:** Adding depth, layering, premium feel
- **Motion tokens:** `ease_out_expo` easing

## Parameters

- **first_content**: First layout/scene (any component)
- **second_content**: Second layout/scene (any component)
- **transition_type**: One of: `crossfade`, `slide_horizontal`, `slide_vertical`, `cube_rotate`, `parallax_push`
- **transition_start**: When to start transition (seconds) - default: 2.0
- **transition_duration**: Duration of transition (seconds) - default: 1.0
- **duration**: Total clip duration (seconds) - default: 5.0

## Motion Token Integration

All transitions use motion tokens for timing:
- **Durations:** `medium` (0.5s), `slow` (0.7s)
- **Easings:** `ease_out_expo`, `ease_in_out_quart`, `ease_out_quint`

## Examples

```python
# Crossfade between Grid and Container
{
    "type": "LayoutTransition",
    "config": {
        "first_content": {"type": "Grid", "config": {...}},
        "second_content": {"type": "Container", "config": {...}},
        "transition_type": "crossfade",
        "transition_start": 2.0,
        "transition_duration": 1.0
    }
}

# Slide horizontal for chapters
{
    "type": "LayoutTransition",
    "config": {
        "first_content": {"type": "TitleScene", "config": {"text": "Chapter 1"}},
        "second_content": {"type": "TitleScene", "config": {"text": "Chapter 2"}},
        "transition_type": "slide_horizontal",
        "transition_duration": 0.8
    }
}

# Dramatic cube rotate
{
    "type": "LayoutTransition",
    "config": {
        "first_content": {"type": "ThreeColumnLayout", "config": {...}},
        "second_content": {"type": "SplitScreen", "config": {...}},
        "transition_type": "cube_rotate",
        "transition_duration": 1.5
    }
}
```

## Best Practices

1. **Keep transition_duration between 0.5s-1.5s** for optimal viewing
2. **Use crossfade** for subtle, professional transitions
3. **Use slide_horizontal** for sequential content (slides, chapters)
4. **Use cube_rotate sparingly** - it's dramatic and attention-grabbing
5. **Use parallax_push** for depth and premium feel
6. **Match transition type to content:** formal = crossfade, playful = cube_rotate

## Common Use Cases

- **Scene changes** in narratives
- **Layout switches** (Grid → Container → Timeline)
- **Before/after showcases**
- **Chapter transitions**
- **Multi-part content flow**
- **Slideshow presentations**
