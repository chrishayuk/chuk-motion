# Remaining Layouts Specifications

This document provides detailed specifications for each remaining layout to be migrated.

## 1. Vertical Layout

### Description
9:16 optimized layout for Shorts/TikTok/Reels with multiple layout styles.

### Props
```python
top: Any | None  # Top content
bottom: Any | None  # Bottom content
layout_style: str = "top-bottom"  # Values: "top-bottom", "caption-content", "content-caption", "split-vertical"
top_ratio: float = 50  # For split styles (percentage)
gap: float = 20
padding: float = 40
```

### Template Notes
- Optimized for 9:16 aspect ratio
- Different arrangements based on `layout_style`:
  - `top-bottom`: Simple vertical stack
  - `caption-content`: Caption at top, content below
  - `content-caption`: Content at top, caption below
  - `split-vertical`: 50/50 split (or custom ratio)

### MCP Tool
`remotion_add_vertical`

---

## 2. DialogueFrame Layout

### Description
For conversation/dialogue scenes with two speakers.

### Props
```python
left_speaker: Any | None  # Left speaker content
right_speaker: Any | None  # Right speaker content
center_content: Any | None  # Optional center content (captions, etc.)
speaker_size: float = 40  # Speaker panel size (percentage)
gap: float = 20
padding: float = 40
```

### Template Notes
- Two side panels for speakers
- Optional center area for captions/shared content
- Typical layout: [Speaker 1] [Center] [Speaker 2]

### MCP Tool
`remotion_add_dialogue_frame`

---

## 3. Timeline Layout

### Description
Progress/timeline overlay with milestones and progress indicators.

### Props
```python
main_content: Any | None  # Background content
milestones: list[dict]  # List of milestone objects with {time, label, icon}
current_time: float = 0  # Current progress time
total_duration: float = 10  # Total timeline duration
position: str = "bottom"  # Values: "top", "bottom"
height: float = 100  # Timeline bar height (pixels)
```

### Template Notes
- Overlay timeline bar over main content
- Show milestones/markers along timeline
- Highlight current position
- Can be positioned at top or bottom

### MCP Tool
`remotion_add_timeline`

---

## 4. OverTheShoulder Layout

### Description
Looking over someone's shoulder perspective, typically for screen recordings.

### Props
```python
screen_content: Any | None  # Main screen content
shoulder_overlay: Any | None  # Person/shoulder overlay
overlay_position: str = "bottom-left"  # Position of shoulder overlay
overlay_size: float = 30  # Size of shoulder overlay (percentage)
angle: float = 0  # Optional rotation angle for perspective
gap: float = 20
padding: float = 40
```

### Template Notes
- Main content takes most of screen
- Shoulder/person overlay in corner (typically bottom-left or bottom-right)
- Optional perspective skew/rotation for "looking over shoulder" effect

### MCP Tool
`remotion_add_over_the_shoulder`

---

## 5. StackedReaction Layout

### Description
Reaction video style with stacked feeds (original content + reaction).

### Props
```python
original_content: Any | None  # Original video/content
reaction_content: Any | None  # Reaction video
layout: str = "vertical"  # Values: "vertical", "horizontal", "pip"
reaction_size: float = 40  # Reaction panel size (percentage)
gap: float = 20
padding: float = 40
```

### Template Notes
- `vertical`: Stacked vertically (reaction above or below)
- `horizontal`: Side by side (reaction left or right)
- `pip`: Reaction as small overlay
- Default: reaction at top, original below (vertical)

### MCP Tool
`remotion_add_stacked_reaction`

---

## 6. HUDStyle Layout

### Description
Heads-up display style with overlay elements (corners, edges, etc.).

### Props
```python
main_content: Any | None  # Main background
top_left: Any | None  # Top-left overlay
top_right: Any | None  # Top-right overlay
bottom_left: Any | None  # Bottom-left overlay
bottom_right: Any | None  # Bottom-right overlay
center: Any | None  # Center overlay
overlay_size: float = 15  # Corner overlay size (percentage)
gap: float = 20
padding: float = 40
```

### Template Notes
- Main content full screen
- Multiple overlay zones (corners + center)
- Overlays should not obscure main content
- Common for gaming, sports, tech demos

### MCP Tool
`remotion_add_hud_style`

---

## 7. PerformanceMultiCam Layout

### Description
Multi-camera performance view with primary + secondary cameras.

### Props
```python
primary_cam: Any | None  # Main camera feed
secondary_cams: list[Any] = []  # List of secondary camera feeds (up to 4)
layout: str = "primary-main"  # Values: "primary-main", "grid", "filmstrip"
gap: float = 20
padding: float = 40
```

### Template Notes
- `primary-main`: Large primary + small secondaries in filmstrip
- `grid`: Equal grid of all cameras
- `filmstrip`: Primary large, secondaries as horizontal strip
- Secondaries limited to 4 cameras

### MCP Tool
`remotion_add_performance_multi_cam`

---

## 8. FocusStrip Layout

### Description
Focused strip/banner layout for highlighting key content.

### Props
```python
main_content: Any | None  # Background/context content
focus_content: Any | None  # Focused strip content
position: str = "center"  # Values: "top", "center", "bottom"
strip_height: float = 30  # Strip height (percentage)
gap: float = 20
padding: float = 40
```

### Template Notes
- Horizontal strip/banner across screen
- Main content dimmed/blurred in background
- Focus strip is prominent
- Use for captions, quotes, code snippets

### MCP Tool
`remotion_add_focus_strip`

---

## 9. Mosaic Layout (COMPLEX)

### Description
Irregular collage with layered clips in various artistic arrangements.

### Props
```python
clips: list[dict]  # List of clip objects with {content, size, position}
style: str = "hero-corners"  # Values: "hero-corners", "stacked", "spotlight"
gap: float = 10
padding: float = 40
```

### Template Notes
- Most complex layout
- `hero-corners`: Large hero center, small clips in corners
- `stacked`: Overlapping cards/layers
- `spotlight`: One large + multiple small arranged around
- Each clip has custom size/position
- May need z-index management

### MCP Tool
`remotion_add_mosaic`

---

## Implementation Checklist

For each layout, create:

- [ ] `schema.py` with Pydantic models
- [ ] `builder.py` with composition method
- [ ] `tool.py` with MCP tool registration
- [ ] `template.tsx.j2` with React component
- [ ] `__init__.py` with exports
- [ ] Update `src/chuk_motion/components/layouts/__init__.py`
- [ ] Test with sample composition

## Testing

For each layout, test with:
1. Minimal props (all optional)
2. Full props
3. Different variants/styles
4. Edge cases (missing content, invalid values)

Refer to test files in `tests/templates/layouts/test_{layoutname}.py` for expected behavior.

## Priority Order

Recommended order to implement:

1. **Vertical** - Simple, high demand for Shorts/Reels
2. **DialogueFrame** - Simple, useful for interviews/conversations
3. **Timeline** - Medium complexity, very useful
4. **StackedReaction** - Popular format
5. **FocusStrip** - Simple, good for captions
6. **OverTheShoulder** - Medium complexity
7. **HUDStyle** - Multiple overlays, medium-high complexity
8. **PerformanceMultiCam** - Complex camera management
9. **Mosaic** - Most complex, save for last

Good luck! Each layout should take 30-60 minutes to implement following the existing patterns.
