# Layout Animations

**Token-First Animation System for Layouts**

A comprehensive suite of layout animation components built with a **motion token-first approach**. These components add professional polish to any video with consistent timing, easing, and springs derived from the motion token system.

---

## 🎯 Core Philosophy

### Token-First Design

Every animation uses **motion tokens** for timing and easing:
- **Durations:** `fast` (0.2s), `normal` (0.35s), `medium` (0.5s), `slow` (0.7s)
- **Easings:** `ease_out_expo`, `ease_out_quint`, `ease_in_out_quart`, `ease_out_back`
- **Springs:** `smooth` (default), `bouncy` (playful), `snappy` (responsive)

This ensures:
✅ **Consistency** across all animations
✅ **Platform optimization** (TikTok sprint vs. cinematic slow)
✅ **Professional polish** without manual timing tweaks
✅ **Scalable** - change tokens globally, update all animations

---

## 🧩 Three Core Components

### 1. LayoutTransition

**Purpose:** Animated scene-to-scene layout transitions

**Variants:**
- `crossfade` – Smooth opacity blend (professional, subtle)
- `slide_horizontal` – Push left, slide right (sequential content)
- `slide_vertical` – Push up, slide from bottom (mobile-like)
- `cube_rotate` – 3D rotation (dramatic, attention-grabbing)
- `parallax_push` – Depth layers (cinematic, premium)

**Motion Tokens:**
- Duration: `medium` (0.5s), `slow` (0.7s)
- Easing: `ease_out_expo`, `ease_in_out_quart`, `ease_out_quint`

**Example:**
```python
remotion_add_layout_transition(
    first_content='{"type":"Grid","config":{"layout":"3x3","items":[...]}}',
    second_content='{"type":"Container","config":{...}}',
    transition_type="crossfade",
    transition_start=2.0,
    transition_duration=1.0
)
```

**Best for:** Scene changes, chapter transitions, before/after showcases

---

### 2. LayoutEntrance

**Purpose:** Universal entrance animation wrapper

**Variants:**
- `fade_in` – Simple fade (professional)
- `fade_slide_up` – Fade + slide up (modern, polished)
- `scale_in_soft` – Subtle scale 0.95→1.0 (elegant)
- `scale_in_pop` – Bounce scale (playful, energetic)
- `slide_in_left` / `slide_in_right` – Directional slides
- `blur_in` – Fade from blur (cinematic)
- `zoom_in` – Explosive zoom (hero entrance)

**Motion Tokens:**
- Duration: `normal` (0.35s), `medium` (0.5s), `slow` (0.7s)
- Easing: `ease_out`, `ease_out_expo`, `ease_out_back`
- Spring: `smooth` (for pop variant)

**Example:**
```python
remotion_add_layout_entrance(
    content='{"type":"Grid","config":{...}}',
    entrance_type="fade_slide_up",
    entrance_delay=0.2
)
```

**Best for:** Zero-config polish, consistent entrance patterns, rapid prototyping

---

### 3. PanelCascade

**Purpose:** Staggered panel entrance animations

**Variants:**
- `from_edges` – Slide from nearest edge (spatial, intelligent)
- `from_center` – Radial scale from center (focal)
- `bounce_in` – Spring bounce (playful)
- `sequential_left` – Left→right (reading order)
- `sequential_right` – Right→left (reverse)
- `sequential_top` – Top→bottom (vertical)
- `wave` – Diagonal wave (dynamic)

**Motion Tokens:**
- Duration: `fast` (0.2s), `medium` (0.5s)
- Easing: `ease_out_expo` (slides), `ease_out_back` (bounce)
- Spring: `bouncy` (for bounce_in)

**Stagger Delay Guidelines:**
- **0.05-0.08s:** Fast cascade (TikTok/Shorts, sprint tempo)
- **0.08-0.12s:** Balanced (YouTube, medium tempo)
- **0.12-0.2s:** Deliberate (presentations, slow tempo)

**Example:**
```python
remotion_add_panel_cascade(
    items='[{"type":"CodeBlock","config":{...}},{"type":"DemoBox","config":{}}]',
    cascade_type="from_edges",
    stagger_delay=0.08
)
```

**Best for:** Grid layouts, multi-panel showcases, photo galleries

---

## 🎨 Design System Integration

### How Motion Tokens Are Used

| Component | Duration Tokens | Easing Tokens | Spring Tokens |
|-----------|----------------|---------------|---------------|
| LayoutTransition | `medium`, `slow` | `ease_out_expo`, `ease_in_out_quart`, `ease_out_quint` | — |
| LayoutEntrance | `normal`, `medium`, `slow` | `ease_out`, `ease_out_expo`, `ease_out_back` | `smooth` |
| PanelCascade | `fast`, `medium` | `ease_out_expo`, `ease_out_back` | `bouncy` |

### Token Hierarchy

```
motion.duration.medium (0.5s)
  → LayoutTransition slide animations
  → LayoutEntrance fade_slide_up
  → PanelCascade from_edges

motion.easing.ease_out_expo ([0.16, 1.0, 0.3, 1.0])
  → Used for snappy, responsive slides
  → All horizontal/vertical slides
  → PanelCascade slides

motion.spring_configs.bouncy (damping: 30, stiffness: 150)
  → PanelCascade bounce_in
  → Playful, energetic reveals
```

### Updating Tokens Globally

**Change one token, update all animations:**

```python
# In motion.py
motion.duration.medium = DurationConfig(
    ms=600,  # Was 500ms
    frames_30fps=18,  # Was 15
    seconds=0.6,
    css="0.6s",
    description="Medium motion (updated)"
)
```

Now **all** components using `medium` duration update automatically:
- LayoutTransition slides
- LayoutEntrance fade_slide_up
- PanelCascade from_edges

This is the power of **token-first design**.

---

## 📚 Common Patterns

### Pattern 1: Cascade → Transition

Combine PanelCascade with LayoutTransition for compound effects:

```python
# 1. Show Grid with cascading panels
remotion_add_panel_cascade(
    items=[...9 panels...],
    cascade_type="from_edges",
    stagger_delay=0.08,
    duration=3.0
)

# 2. Transition to different layout
remotion_add_layout_transition(
    first_content='{"type":"Grid","config":{...}}',
    second_content='{"type":"Timeline","config":{...}}',
    transition_type="crossfade",
    transition_start=2.5
)
```

### Pattern 2: Entrance Wrapper

Use LayoutEntrance to wrap **any** layout:

```python
# Add entrance to Grid
remotion_add_layout_entrance(
    content='{"type":"Grid","config":{...}}',
    entrance_type="fade_slide_up"
)

# Add entrance to Timeline
remotion_add_layout_entrance(
    content='{"type":"Timeline","config":{...}}',
    entrance_type="blur_in",
    entrance_delay=0.5
)
```

### Pattern 3: Platform-Optimized Cascade

Match stagger_delay to platform tempo:

```python
# TikTok/Shorts (sprint tempo)
remotion_add_panel_cascade(
    items=[...],
    cascade_type="from_edges",
    stagger_delay=0.05  # Fast cascade
)

# YouTube (medium tempo)
remotion_add_panel_cascade(
    items=[...],
    cascade_type="wave",
    stagger_delay=0.1  # Balanced
)

# Presentation (slow tempo)
remotion_add_panel_cascade(
    items=[...],
    cascade_type="from_center",
    stagger_delay=0.15  # Deliberate
)
```

---

## 🎬 Use Cases by Content Type

### Tech Tutorials (YouTube Long-Form)

```python
# Opening: Grid entrance with panels
remotion_add_layout_entrance(
    content='{"type":"Grid","config":{...}}',
    entrance_type="fade_slide_up"
)

# Sections: Transition between layouts
remotion_add_layout_transition(
    first_content='{"type":"Container","config":{...}}',
    second_content='{"type":"Timeline","config":{...}}',
    transition_type="slide_horizontal"
)
```

### Shorts/Reels (TikTok)

```python
# Fast cascade for retention
remotion_add_panel_cascade(
    items=[...],
    cascade_type="bounce_in",  # Energetic
    stagger_delay=0.06  # Sprint tempo
)

# Quick transitions
remotion_add_layout_transition(
    first_content=...,
    second_content=...,
    transition_type="slide_vertical",  # Mobile-like
    transition_duration=0.5  # Fast
)
```

### Presentations

```python
# Deliberate cascade
remotion_add_panel_cascade(
    items=[...],
    cascade_type="sequential_left",  # Reading order
    stagger_delay=0.15  # Slow tempo
)

# Professional transitions
remotion_add_layout_transition(
    first_content=...,
    second_content=...,
    transition_type="crossfade",  # Subtle
    transition_duration=1.2  # Slower
)
```

### Portfolio Showcase

```python
# Radial reveal from center
remotion_add_panel_cascade(
    items=[...9 portfolio items...],
    cascade_type="from_center",
    stagger_delay=0.1
)

# Transition to hero shot
remotion_add_layout_transition(
    first_content='{"type":"Grid","config":{...}}',
    second_content='{"type":"Container","config":{...}}',
    transition_type="parallax_push"  # Premium feel
)
```

---

## 🔧 Technical Details

### Grid Calculation (PanelCascade)

PanelCascade automatically calculates grid positions:

```typescript
// Calculate grid dimensions
const cols = Math.ceil(Math.sqrt(panelCount))
const rows = Math.ceil(panelCount / cols)

// For 9 panels: 3x3 grid
// For 6 panels: 3x2 grid
// For 4 panels: 2x2 grid
```

**Distance calculations:**
- `from_edges`: `min(distLeft, distRight, distTop, distBottom)`
- `from_center`: `√((row - centerRow)² + (col - centerCol)²)`
- `wave`: `row + col` (diagonal)

### Motion Token Access

Templates access tokens via Jinja2:

```tsx
const DURATION_MEDIUM = [[ motion.duration.medium.frames_30fps ]];
const easeOutExpo = [[ motion.easing.ease_out_expo.curve ]];

const opacity = interpolate(
  relativeFrame,
  [0, DURATION_MEDIUM],
  [0, 1],
  {
    easing: Easing.bezier(...easeOutExpo)
  }
);
```

---

## 📖 Complete Examples

See `examples/` directory:
- `layout_animations_showcase.py` – Full showcase of all three components
- `layout_transition_examples.py` – All 5 transition types
- `panel_cascade_examples.py` – All 7 cascade types

---

## 🚀 Next Steps

### Future Animation Patterns

From the original roadmap (not yet implemented):

4. **FocusSwap** – Animate focus between panels (FocusStrip, PiP, Mosaic)
5. **VerticalReveal** – Platform-specific Shorts/Reels animations
6. **DialogueChoreography** – Speaker-driven panel animations
7. **GridMorph** – Morph between grid configurations
8. **OverTheShoulderMotion** – Camera-like motion simulation
9. **HUDPulse** – Micro-interactions for HUD overlays
10. **TimelineScroll** – Animated timeline reveals

All would follow the same **token-first** architecture.

---

## 💡 Best Practices Summary

### 1. Choose the Right Component

- **LayoutTransition** → Scene-to-scene changes
- **LayoutEntrance** → Add polish to any layout
- **PanelCascade** → Multi-panel reveals

### 2. Match Animation to Content Tone

| Tone | LayoutTransition | LayoutEntrance | PanelCascade |
|------|-----------------|----------------|--------------|
| Professional | `crossfade` | `fade_in` | `from_edges` |
| Playful | `cube_rotate` | `scale_in_pop` | `bounce_in` |
| Cinematic | `parallax_push` | `blur_in` | `from_center` |
| Modern | `slide_horizontal` | `fade_slide_up` | `wave` |

### 3. Respect Motion Token Guidelines

- **Don't hardcode durations** – use motion tokens
- **Don't hardcode easings** – reference token easings
- **Match tempo to platform** – use tempo tokens for guidance

### 4. Transition Duration Guidelines

- **0.5-0.8s:** Snappy (Shorts, social)
- **0.8-1.2s:** Balanced (YouTube, general)
- **1.2-2.0s:** Deliberate (presentations, cinematic)

### 5. Stagger Delay Guidelines

- **Fast (0.05-0.08s):** High retention, sprint tempo
- **Medium (0.08-0.12s):** Balanced pacing
- **Slow (0.12-0.2s):** Deliberate, clear

---

## 📐 Architecture

```
src/chuk_motion/components/
├── transitions/
│   ├── LayoutTransition/
│   │   ├── __init__.py          (METADATA export)
│   │   ├── tool.py              (MCP tool registration)
│   │   ├── template.tsx.j2      (React/Remotion component)
│   │   ├── component.md         (Documentation)
│   │   └── METADATA.json        (Component metadata)
│   └── PixelTransition/
├── animations/
│   ├── LayoutEntrance/
│   │   ├── __init__.py
│   │   ├── schema.py            (Pydantic models, MCP_SCHEMA)
│   │   ├── builder.py           (Composition builder)
│   │   ├── tool.py
│   │   ├── template.tsx.j2
│   │   └── component.md
│   ├── PanelCascade/
│   │   └── (same structure)
│   └── Counter/

tokens/motion.py                  (Motion token definitions)
themes/models.py                  (ThemeMotion model)
```

Auto-discovery via `components/__init__.py:discover_components()`

---

**Built with ❤️ using motion-token-first architecture**
