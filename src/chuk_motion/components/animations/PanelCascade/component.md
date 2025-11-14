# PanelCascade

**Category:** Animation
**Purpose:** Staggered panel entrance animations for multi-panel layouts

## Overview

PanelCascade creates beautiful staggered animations for multi-panel layouts. Each panel animates in with a short delay, creating a cascading reveal effect. Perfect for Grid, ThreeColumn, Mosaic, and other layouts with multiple distinct regions.

## Cascade Types

### from_edges
Panels slide in from their nearest screen edge (top, bottom, left, or right).
- **Feel:** Spatial, professional, intelligent
- **Use for:** Grid layouts, professional showcases, photo galleries
- **How it works:** Calculates distance from each edge, animates from closest
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### from_center
Panels scale out radially from the center.
- **Feel:** Radial, attention-grabbing, focal
- **Use for:** Hero grids, focal reveals, center-emphasis content
- **How it works:** Calculates distance from center, staggers outward
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

### bounce_in
Panels bounce in with spring overshoot.
- **Feel:** Playful, energetic, fun
- **Use for:** Creator content, playful reveals, informal showcases
- **How it works:** Uses bouncy spring for each panel
- **Motion tokens:** `bouncy` spring (30 damping, 150 stiffness)

### sequential_left
Left-to-right sequential reveal.
- **Feel:** Familiar, reading-order, structured
- **Use for:** Lists, sequential content, step-by-step reveals
- **How it works:** Simple index-based stagger
- **Motion tokens:** `ease_out_expo` easing, `fast` duration

### sequential_right
Right-to-left sequential reveal (reverse).
- **Feel:** Reverse flow, alternative direction
- **Use for:** RTL content, reverse reveals, variety
- **How it works:** Reverse index-based stagger
- **Motion tokens:** `ease_out_expo` easing, `fast` duration

### sequential_top
Top-to-bottom sequential reveal.
- **Feel:** Vertical flow, natural reading
- **Use for:** Vertical lists, dropdown content, timelines
- **How it works:** Index-based vertical stagger
- **Motion tokens:** `ease_out_expo` easing, `fast` duration

### wave
Diagonal wave pattern across panels.
- **Feel:** Dynamic, flowing, rhythmic
- **Use for:** Dynamic reveals, flowing content, creative showcases
- **How it works:** Diagonal (row + col) stagger with combined scale + translateY
- **Motion tokens:** `ease_out_expo` easing, `medium` duration

## Parameters

- **items**: Array of panel components to animate (required)
- **cascade_type**: One of the 7 cascade types above - default: `from_edges`
- **stagger_delay**: Delay between each panel in seconds - default: 0.08
- **duration**: Total clip duration (seconds) - default: 5.0

## Motion Token Integration

All cascade animations use motion tokens:
- **Durations:** `fast` (0.2s), `medium` (0.5s)
- **Easings:** `ease_out_expo` (snappy deceleration), `ease_out_back` (overshoot)
- **Springs:** `bouncy` spring for bounce_in variant

### Stagger Delay Guidelines

Based on tempo tokens:
- **0.05s-0.08s:** Fast cascade (sprint tempo) - TikTok/Shorts
- **0.08s-0.12s:** Balanced cascade (medium tempo) - YouTube
- **0.12s-0.2s:** Deliberate cascade (slow tempo) - Presentations

## Examples

```python
# From edges - 3x3 grid (professional)
{
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "CodeBlock", "config": {"code": f"Panel {i}"}}
            for i in range(1, 10)
        ],
        "cascade_type": "from_edges",
        "stagger_delay": 0.08
    }
}

# From center - radial reveal
{
    "type": "PanelCascade",
    "config": {
        "items": [{"type": "DemoBox", "config": {}} for _ in range(9)],
        "cascade_type": "from_center",
        "stagger_delay": 0.1
    }
}

# Bounce in - playful energy
{
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "Counter", "config": {
                "start_value": 0,
                "end_value": (i + 1) * 1000,
                "suffix": " users"
            }}
            for i in range(6)
        ],
        "cascade_type": "bounce_in",
        "stagger_delay": 0.12
    }
}

# Wave pattern - dynamic flow
{
    "type": "PanelCascade",
    "config": {
        "items": [...],
        "cascade_type": "wave",
        "stagger_delay": 0.08
    }
}
```

## Best Practices

1. **Use from_edges for professional content** - intelligent and spatial
2. **Use from_center for focal reveals** - draws eye to center
3. **Use bounce_in for playful content** - energetic and fun
4. **Use sequential_left for familiar flow** - reading order
5. **Use wave for dynamic reveals** - flowing and creative
6. **Match stagger_delay to platform:**
   - TikTok/Shorts: 0.05-0.08s (sprint tempo)
   - YouTube: 0.08-0.12s (medium tempo)
   - Presentations: 0.12-0.2s (slow tempo)
7. **Grid layouts automatically calculated** - component handles positioning

## Grid Calculation

PanelCascade automatically:
- Calculates optimal grid dimensions (√n columns)
- Determines panel positions (row, col)
- Calculates distances (from edges, from center)
- Applies intelligent stagger based on cascade_type

## Common Use Cases

- **Portfolio showcases** (9-panel grid with from_edges)
- **Feature grids** (6-panel with sequential_left)
- **Photo galleries** (from_center radial reveal)
- **Stats dashboards** (bounce_in for energy)
- **Timeline milestones** (sequential_top vertical flow)
- **Multi-panel comparisons** (wave for dynamic flow)

## Combining with Other Components

```python
# PanelCascade → LayoutTransition
# First show panels with cascade, then transition to different layout

# LayoutEntrance(PanelCascade)
# Wrap entire cascade in entrance for compound effect
```
