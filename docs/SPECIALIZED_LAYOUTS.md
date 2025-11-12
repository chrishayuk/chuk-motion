# Specialized YouTube Layouts

This guide covers 6 additional specialized layouts for narrative, reaction, gaming, and creative content.

---

## 🎭 Narrative / Storytelling Layouts

### 1. OverTheShoulderLayout
**Template**: `layouts/OverTheShoulderLayout.tsx.j2`

**Purpose**: Show both the host and their screen content side-by-side, creating an immersive tutorial experience.

**Perfect for**:
- Coding walkthroughs and tutorials
- Editing demos (video, photo, audio)
- Creative process videos
- Screen-based educational content

**Configuration**:
```python
{
    "type": "OverTheShoulderLayout",
    "config": {
        "host_position": "left",  # "left" | "right"
        "host_size": 35,  # Host view width percentage
        "gap": 20,
        "border_width": 2,
        "border_color": colors.text.muted,
        "padding": 40
    },
    "hostView": {...},  # Your host/presenter component
    "screenContent": {...},  # Screen share/content component
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Configurable host position (left or right)
- Adjustable size ratio between host and screen
- Clean borders and professional styling
- Maintains focus on screen content while showing presenter

**Use Cases**:
- "Let me show you how to..." tutorials
- Design process walkthroughs
- Code-along sessions
- Software demonstrations

---

### 2. DialogueFrameLayout
**Template**: `layouts/DialogueFrameLayout.tsx.j2`

**Purpose**: Split screen for conversations, debates, or character-based content.

**Perfect for**:
- Comedy skits and sketches
- Interview formats
- AI conversation visualizations
- Role-play content
- Debate videos

**Configuration**:
```python
{
    "type": "DialogueFrameLayout",
    "config": {
        "character_a_label": "Alex",
        "character_b_label": "Jamie",
        "gap": 20,
        "border_width": 2,
        "border_color": colors.text.muted,
        "label_background": colors.background.glass,
        "label_border": colors.primary[0],
        "padding": 40
    },
    "characterA": {...},  # Left character
    "characterB": {...},  # Right character
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Equal split for balanced dialogue
- Optional character name labels with glass-morphism
- Configurable styling per character
- Perfect 50/50 screen division

**Use Cases**:
- "Person A vs Person B" format videos
- Conversational storytelling
- Reaction comparisons
- Split perspective narratives

---

## 🎬 Reaction / Commentary Layouts

### 3. StackedReactionLayout
**Template**: `layouts/StackedReactionLayout.tsx.j2`

**Purpose**: Vertical stack showing original content and reactor simultaneously.

**Perfect for**:
- Music/video reactions
- Commentary content
- YouTube Shorts/TikTok reactions
- Meme reactions

**Configuration**:
```python
{
    "type": "StackedReactionLayout",
    "config": {
        "clip_ratio": 65,  # Original clip height percentage
        "gap": 20,
        "show_labels": True,  # Show "ORIGINAL" and "REACTION" badges
        "border_width": 2,
        "border_color": colors.text.muted,
        "reactor_border_color": colors.primary[0],
        "label_background": colors.background.glass,
        "padding": 40
    },
    "originalClip": {...},  # Content being reacted to
    "reactorFace": {...},  # Reactor's webcam
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Configurable ratio (default 65/35 split)
- Auto-labels for "ORIGINAL" and "REACTION"
- Different border colors to distinguish content
- Optimized for vertical mobile formats

**Use Cases**:
- Music video reactions
- "First time watching..." content
- Commentary on viral clips
- Educational analysis videos

---

## 🎮 Gaming / Performance Layouts

### 4. HUDStyleLayout
**Template**: `layouts/HUDStyleLayout.tsx.j2`

**Purpose**: Full-screen gameplay with overlaid webcam and chat HUD elements.

**Perfect for**:
- Livestreams and gaming content
- Let's Plays and speedruns
- Esports and competitive gaming
- Tutorial streams with viewer interaction

**Configuration**:
```python
{
    "type": "HUDStyleLayout",
    "config": {
        "webcam_position": "top-left",  # "top-left" | "top-right" | "bottom-left" | "bottom-right"
        "webcam_size": 15,  # Webcam width percentage
        "show_chat": True,
        "chat_width": 25,  # Chat panel width percentage
        "webcam_border_color": colors.primary[0],
        "chat_background": colors.background.glass
    },
    "gameplay": {...},  # Main gameplay content
    "webcam": {...},  # Streamer webcam
    "chatOverlay": {...},  # Live chat component
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Fullscreen gameplay with minimal obstruction
- Floating webcam overlay (4 position options)
- Optional live chat panel with glass-morphism
- Professional streaming HUD aesthetic

**Use Cases**:
- Twitch/YouTube Gaming streams
- Walkthrough and tutorial content
- Competitive gaming highlights
- Stream replays and VODs

---

### 5. PerformanceMultiCamLayout
**Template**: `layouts/PerformanceMultiCamLayout.tsx.j2`

**Purpose**: 2x2 grid showing multiple camera angles simultaneously.

**Perfect for**:
- Music performances and covers
- Cooking shows and recipes
- Art creation timelapses
- DIY and craft tutorials
- Sports technique analysis

**Configuration**:
```python
{
    "type": "PerformanceMultiCamLayout",
    "config": {
        "labels": {
            "front": "FRONT VIEW",
            "overhead": "OVERHEAD",
            "hand": "HAND CAM",
            "detail": "DETAIL"
        },
        "gap": 20,
        "show_labels": True,
        "border_width": 2,
        "border_radius": 8,
        "label_background": colors.background.glass,
        "padding": 40
    },
    "frontCam": {...},  # Main front-facing camera
    "overheadCam": {...},  # Top-down view
    "handCam": {...},  # Close-up of hands/action
    "detailCam": {...},  # Detail/foot pedal/other angle
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Perfect 2x2 grid layout
- Customizable camera labels
- Color-coded borders (accent color for main, primary for others)
- Professional multi-angle production look

**Use Cases**:
- Music instrument tutorials
- Cooking demonstrations with overhead shot
- Art/drawing process videos
- Woodworking and crafts
- Dance and movement tutorials

---

## 🎨 Hybrid / Creative Layouts

### 6. FocusStripLayout
**Template**: `layouts/FocusStripLayout.tsx.j2`

**Purpose**: Centered host bar over blurred B-roll background - trendy modern aesthetic.

**Perfect for**:
- Documentary-style narration (Vox, Nebula style)
- Essay videos with visual backgrounds
- News and analysis content
- Modern commentary format

**Configuration**:
```python
{
    "type": "FocusStripLayout",
    "config": {
        "strip_height": 30,  # Host strip height percentage
        "strip_position": "center",  # "center" | "top" | "bottom"
        "background_blur": 5,  # Blur amount for background
        "strip_background": colors.background.dark,
        "border_width": 2,
        "border_color": colors.primary[0],
        "strip_shadow": True  # Add shadow to strip
    },
    "hostStrip": {...},  # Focused host/narrator component
    "backgroundContent": {...},  # B-roll or visual content
    "startFrame": 0,
    "durationInFrames": 300
}
```

**Key Features**:
- Blurred background for visual interest without distraction
- Focused horizontal strip for host
- Configurable positioning (center, top, or bottom)
- Modern editorial aesthetic
- Optional shadow for depth

**Use Cases**:
- Video essays and analysis
- News commentary and explainers
- Documentary-style content
- Educational content with B-roll
- Professional journalism format

---

## 📊 Layout Summary Table

| Layout | Category | Best For | Complexity | Mobile-Friendly |
|--------|----------|----------|------------|-----------------|
| OverTheShoulder | Narrative | Tutorials | Medium | ✅ Yes |
| DialogueFrame | Narrative | Conversations | Low | ✅ Yes |
| StackedReaction | Reaction | Reactions | Low | ⭐ Excellent |
| HUDStyle | Gaming | Livestreams | High | ⚠️ Desktop only |
| PerformanceMultiCam | Creative | Multi-angle | High | ⚠️ Desktop only |
| FocusStrip | Hybrid | Essays | Medium | ✅ Yes |

---

## 🎯 Choosing the Right Layout

### For Tutorial Content:
1. **Code/Software**: OverTheShoulderLayout
2. **Creative Process**: PerformanceMultiCamLayout
3. **Narrated Lessons**: FocusStripLayout

### For Entertainment:
1. **Reactions**: StackedReactionLayout
2. **Skits/Comedy**: DialogueFrameLayout
3. **Gaming**: HUDStyleLayout

### For Professional Content:
1. **Interviews**: DialogueFrameLayout
2. **Analysis/Essays**: FocusStripLayout
3. **Demonstrations**: PerformanceMultiCamLayout

---

## 🔧 Implementation Example

```python
from chuk_motion.generator.composition_builder import CompositionBuilder

# Example: Creating a coding tutorial with Over-the-Shoulder layout
tutorial_scene = {
    "type": "OverTheShoulderLayout",
    "config": {
        "host_position": "left",
        "host_size": 35,
        "gap": 20,
        "border_width": 2,
        "padding": 40
    },
    "hostView": {
        "type": "PersonSpeaking",
        "config": {
            "name": "Sarah",
            "title": "Senior Developer"
        }
    },
    "screenContent": {
        "type": "CodeBlock",
        "config": {
            "code": "function example() {\\n  return 'Hello World';\\n}",
            "language": "javascript"
        }
    },
    "startFrame": 0,
    "durationInFrames": 300
}
```

---

## 📝 Notes

- All layouts support **design token integration**
- All layouts are **time-based** with `startFrame` and `durationInFrames`
- All layouts support **custom padding** and **border styling**
- Check individual layout docs for specific configuration options

For complete examples, see:
- `examples/specialized_layouts.py` (coming soon)
- `docs/YOUTUBE_LAYOUTS.md` for basic layouts
- `docs/ALL_YOUTUBE_LAYOUTS.md` for complete coverage
