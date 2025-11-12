# Design Token System

**Version 2.0** - Production-Ready Token System for MCP-Driven Video Generation

## Overview

The chuk-motion design token system provides a comprehensive, structured approach to video styling, motion, layout, and brand customization. This system ensures consistency across all generated videos while enabling platform-specific optimizations and client-specific white-labeling.

Design tokens are the atomic building blocks of the design system:

```
Tokens → Themes → Components → Compositions → Videos
```

### Token Philosophy

Design tokens provide several benefits:

- **Consistency**: Single source of truth for design decisions
- **Reusability**: Tokens can be combined and reused across components
- **Maintainability**: Update tokens once, changes propagate everywhere
- **Scalability**: Easy to add new themes and variants
- **LLM-Friendly**: Structured, discoverable design options

### Token Hierarchy

```
Base Tokens (primitives)
    ↓
Semantic Tokens (meaningful names)
    ↓
Component Tokens (component-specific)
    ↓
Theme Tokens (complete system)
```

---

## Table of Contents

1. [Typography Tokens](#typography-tokens)
2. [Color Tokens](#color-tokens)
3. [Motion Tokens](#motion-tokens)
4. [Spacing & Safe Areas](#spacing--safe-areas)
5. [Brand Packs](#brand-packs)
6. [Caption Styles](#caption-styles)
7. [Usage Guide](#usage-guide)
8. [MCP Tools](#mcp-tools)

---

## Typography Tokens

**Location**: `src/chuk_motion/tokens/typography.py`

Typography tokens define the text system optimized for video content at various resolutions.

### Font Families

Four font categories for different content types:

```python
from chuk_motion.tokens.typography import TYPOGRAPHY_TOKENS

font_families = TYPOGRAPHY_TOKENS.font_families
```

#### Display Fonts
- **Fonts**: Inter, SF Pro Display, system-ui, sans-serif
- **Usage**: Large headings and titles
- **Characteristics**: Bold, attention-grabbing

#### Body Fonts
- **Fonts**: Inter, SF Pro Text, system-ui, sans-serif
- **Usage**: Body text, captions, descriptions
- **Characteristics**: Readable, clean

#### Monospace Fonts
- **Fonts**: JetBrains Mono, Fira Code, Monaco, monospace
- **Usage**: Code blocks, technical content
- **Characteristics**: Fixed-width, developer-friendly

#### Decorative Fonts
- **Fonts**: Poppins, Montserrat, Raleway, sans-serif
- **Usage**: Special emphasis, stylized text
- **Characteristics**: Unique, expressive

### Font Sizes

Font sizes optimized for three video resolutions:

```python
# 1080p (Full HD) - Most common
sizes_1080p = TYPOGRAPHY_TOKENS.font_sizes.video_1080p
# xs: 24px, sm: 32px, base: 40px, lg: 48px
# xl: 64px, 2xl: 80px, 3xl: 96px, 4xl: 120px

# 4K (Ultra HD)
sizes_4k = TYPOGRAPHY_TOKENS.font_sizes.video_4k
# xs: 48px, sm: 64px, base: 80px, lg: 96px
# xl: 128px, 2xl: 160px, 3xl: 192px, 4xl: 240px

# 720p (HD)
sizes_720p = TYPOGRAPHY_TOKENS.font_sizes.video_720p
# xs: 18px, sm: 24px, base: 30px, lg: 36px
# xl: 48px, 2xl: 60px, 3xl: 72px, 4xl: 90px
```

### Font Size Scale

| Size | 1080p | 4K | 720p | Usage |
|------|-------|-----|------|-------|
| xs | 24px | 48px | 18px | Small captions |
| sm | 32px | 64px | 24px | Regular captions |
| base | 40px | 80px | 30px | Body text |
| lg | 48px | 96px | 36px | Subheadings |
| xl | 64px | 128px | 48px | Headings |
| 2xl | 80px | 160px | 60px | Large headings |
| 3xl | 96px | 192px | 72px | Title cards |
| 4xl | 120px | 240px | 90px | Hero titles |

### Font Weights

Standard font weight scale:

```python
weights = TYPOGRAPHY_TOKENS.font_weights
# thin: 100, extralight: 200, light: 300
# regular: 400, medium: 500, semibold: 600
# bold: 700, extrabold: 800, black: 900
```

### Line Heights

Optimized for readability:

```python
line_heights = TYPOGRAPHY_TOKENS.line_heights
# tight: 1.1    - Large headings
# snug: 1.25    - Headings
# normal: 1.5   - Body text
# relaxed: 1.75 - Captions
# loose: 2.0    - Special cases
```

### Text Styles

Pre-configured text styles combining multiple properties:

```python
text_styles = TYPOGRAPHY_TOKENS.text_styles

# Hero Title - Largest, boldest text
hero_title = text_styles.hero_title
# fontSize: 4xl, fontWeight: black, lineHeight: tight

# Title - Large section titles
title = text_styles.title
# fontSize: 3xl, fontWeight: bold, lineHeight: tight

# Heading - Standard headings
heading = text_styles.heading
# fontSize: 2xl, fontWeight: semibold, lineHeight: snug

# Body - Regular content
body = text_styles.body
# fontSize: base, fontWeight: regular, lineHeight: normal

# Caption - Small descriptive text
caption = text_styles.caption
# fontSize: sm, fontWeight: medium, lineHeight: relaxed
```

---

## Color Tokens

**Location**: `src/chuk_motion/tokens/colors.py`

Color tokens define the visual palette for each theme. All colors are tested for readability and visual impact on screen.

### Structure

Each color theme includes:

- **Primary Colors**: Main brand colors (3-scale progression)
- **Accent Colors**: Secondary colors for emphasis (3-scale)
- **Gradient**: Linear gradient combining primary and accent
- **Background Colors**: Dark, light, and glass variants
- **Text Colors**: Optimized for readability on backgrounds
- **Semantic Colors**: Success, warning, error, and info states

### Using Color Tokens

```python
from chuk_motion.tokens.colors import COLOR_TOKENS

# Access specific color
tech_primary = COLOR_TOKENS["tech"]["primary"][0]  # #0066FF

# Get gradient
tech_gradient = COLOR_TOKENS["tech"]["gradient"]

# Text colors for contrast
text_on_dark = COLOR_TOKENS["tech"]["text"]["on_dark"]  # #FFFFFF

# Semantic colors
success_color = COLOR_TOKENS["tech"]["semantic"]["success"]
```

### Color Scale

Each primary and accent color has a 3-step scale:

1. **Base (index 0)**: Default color, most commonly used
2. **Dark (index 1)**: Darker variant for hover states or depth
3. **Darker (index 2)**: Darkest variant for active states

```python
# Example: Tech theme blue scale
primary_base = COLOR_TOKENS["tech"]["primary"][0]    # #0066FF
primary_dark = COLOR_TOKENS["tech"]["primary"][1]    # #0052CC
primary_darker = COLOR_TOKENS["tech"]["primary"][2]  # #003D99
```

### Available Color Themes

| Theme | Primary | Accent | Description |
|-------|---------|--------|-------------|
| Tech | Blue | Cyan | Modern tech aesthetic |
| Finance | Green | Gold | Professional finance |
| Education | Purple | Orange | Friendly education |
| Lifestyle | Pink | Coral | Warm lifestyle |
| Gaming | Neon Green | Neon Purple | High-energy gaming |
| Minimal | Gray | Light | Clean monochrome |
| Business | Navy | Teal | Professional business |

---

## Motion Tokens

**Location**: `src/chuk_motion/tokens/motion.py`

Motion tokens standardize animation timing, easing, and choreography across all video content. All motion tokens are now Pydantic models for type safety and validation.

### Duration Tokens

Standardized timing values for consistent animation speed.

```python
from chuk_motion.tokens.motion import MOTION_TOKENS

# Access as Pydantic model attributes
MOTION_TOKENS.duration.instant         # 0ms (0 frames)
MOTION_TOKENS.duration.ultra_fast      # 100ms (3 frames @ 30fps)
MOTION_TOKENS.duration.fast            # 200ms (6 frames)
MOTION_TOKENS.duration.normal          # 350ms (11 frames)
MOTION_TOKENS.duration.medium          # 500ms (15 frames)
MOTION_TOKENS.duration.slow            # 700ms (21 frames)
MOTION_TOKENS.duration.slower          # 1000ms (30 frames)
MOTION_TOKENS.duration.ultra_slow      # 1500ms (45 frames)
```

**Each includes**:
- `ms`: Milliseconds
- `frames_30fps`: Frame count at 30fps
- `frames_60fps`: Frame count at 60fps
- `seconds`: Duration in seconds
- `css`: CSS duration string
- `description`: Human-readable description

### Easing Curves

15 predefined timing functions for animation interpolation.

```python
# Access easing curves
MOTION_TOKENS.easing.linear
MOTION_TOKENS.easing.ease_in_out

# Ease In (slow start, accelerate)
MOTION_TOKENS.easing.ease_in
MOTION_TOKENS.easing.ease_in_cubic

# Ease Out (fast start, decelerate)
MOTION_TOKENS.easing.ease_out
MOTION_TOKENS.easing.ease_out_cubic
MOTION_TOKENS.easing.ease_out_expo
MOTION_TOKENS.easing.ease_out_back

# Ease In Out (slow start and end)
MOTION_TOKENS.easing.ease_in_out_quart
MOTION_TOKENS.easing.ease_in_out_back

# Special curves
MOTION_TOKENS.easing.bounce
MOTION_TOKENS.easing.elastic
MOTION_TOKENS.easing.anticipate
```

**Each includes**:
- `curve`: Cubic bezier values [x1, y1, x2, y2]
- `css`: CSS timing function string
- `description`: Animation characteristic
- `usage`: Best use cases

### Spring Configurations

Physics-based spring animations for natural motion.

```python
MOTION_TOKENS.spring_configs.gentle    # Soft, floaty (damping: 100, stiffness: 100)
MOTION_TOKENS.spring_configs.smooth    # Balanced, natural (damping: 50, stiffness: 120)
MOTION_TOKENS.spring_configs.bouncy    # Playful overshoot (damping: 15, stiffness: 300)
MOTION_TOKENS.spring_configs.snappy    # Quick, responsive (damping: 30, stiffness: 200)
MOTION_TOKENS.spring_configs.stiff     # Rigid, precise (damping: 20, stiffness: 300)
```

**Each includes**:
- `config`: `{damping, mass, stiffness}`
- `feel`: Animation personality
- `usage`: Recommended use cases

### Enter Transitions

10 predefined entrance animations.

```python
MOTION_TOKENS.enter.fade_in            # Simple opacity fade
MOTION_TOKENS.enter.fade_up            # Fade + slide up
MOTION_TOKENS.enter.fade_down          # Fade + slide down
MOTION_TOKENS.enter.slide_in_left      # Slide from left
MOTION_TOKENS.enter.slide_in_right     # Slide from right
MOTION_TOKENS.enter.scale_in           # Zoom in with overshoot
MOTION_TOKENS.enter.zoom_in            # Dramatic zoom
MOTION_TOKENS.enter.bounce_in          # Bouncy spring entrance
MOTION_TOKENS.enter.rotate_in          # Rotate + scale
MOTION_TOKENS.enter.blur_in            # Fade in from blurred
```

### Exit Transitions

8 predefined exit animations.

```python
MOTION_TOKENS.exit.fade_out            # Simple fade out
MOTION_TOKENS.exit.fade_out_down       # Fade + slide down
MOTION_TOKENS.exit.fade_out_up         # Fade + slide up
MOTION_TOKENS.exit.slide_out_left      # Slide to left
MOTION_TOKENS.exit.slide_out_right     # Slide to right
MOTION_TOKENS.exit.scale_out           # Shrink + fade
MOTION_TOKENS.exit.zoom_out            # Dramatic zoom out
MOTION_TOKENS.exit.pull_back           # Pull away with perspective
```

### Tempo / Narrative Rhythm

Control pacing for different content types.

```python
MOTION_TOKENS.tempo.sprint             # 1.0s beats - TikTok style
MOTION_TOKENS.tempo.fast               # 1.5s beats - Social media
MOTION_TOKENS.tempo.medium             # 2.2s beats - Standard explainer
MOTION_TOKENS.tempo.slow               # 3.5s beats - Technical content
MOTION_TOKENS.tempo.cinematic          # 4.5s beats - Documentary style
```

**Each includes**:
- `beat_duration`: Seconds between visual beats
- `frames_30fps`: Frames per beat
- `caption_duration`: How long to show captions
- `scene_duration_range`: Min/max scene lengths
- `feel`: Content personality

### Platform Timing

Optimized timing for each platform's algorithm.

```python
MOTION_TOKENS.platform_timing.youtube_long_form
MOTION_TOKENS.platform_timing.youtube_shorts
MOTION_TOKENS.platform_timing.tiktok
MOTION_TOKENS.platform_timing.instagram_reel
MOTION_TOKENS.platform_timing.linkedin
MOTION_TOKENS.platform_timing.presentation
```

**Each includes**:
- `hook_duration`: Seconds to grab attention
- `scene_change_interval`: Pattern interrupt timing
- `caption_display_duration`: Caption hold duration
- `cta_timing`: Call-to-action timing
- `attention_span`: "ultra_short" | "short" | "medium" | "long"
- `recommended_tempo`: Which tempo to use

---

## Spacing & Safe Areas

**Location**: `src/chuk_motion/tokens/spacing.py`

Comprehensive spacing system with platform-specific safe zones.

### Spacing Scale

```python
from chuk_motion.tokens.spacing import SPACING_TOKENS

SPACING_TOKENS.spacing.none   # 0
SPACING_TOKENS.spacing.xxs    # 4px
SPACING_TOKENS.spacing.xs     # 8px
SPACING_TOKENS.spacing.sm     # 12px
SPACING_TOKENS.spacing.md     # 16px (base unit)
SPACING_TOKENS.spacing.lg     # 24px
SPACING_TOKENS.spacing.xl     # 32px
SPACING_TOKENS.spacing.xxl    # 48px
SPACING_TOKENS.spacing.xxxl   # 64px
SPACING_TOKENS.spacing.xxxxl  # 80px
SPACING_TOKENS.spacing.xxxxxl # 120px
```

### Safe Areas (Platform-Specific)

Critical for avoiding UI overlay collisions.

```python
SPACING_TOKENS.safe_area.desktop                 # 16:9 general
SPACING_TOKENS.safe_area.mobile                  # 9:16 general
SPACING_TOKENS.safe_area.youtube_long_form       # YouTube desktop player
SPACING_TOKENS.safe_area.youtube_shorts          # YouTube Shorts
SPACING_TOKENS.safe_area.tiktok                  # TikTok
SPACING_TOKENS.safe_area.instagram_reel          # Instagram Reels
SPACING_TOKENS.safe_area.instagram_story         # Instagram Stories
SPACING_TOKENS.safe_area.linkedin                # LinkedIn feed
SPACING_TOKENS.safe_area.twitter                 # Twitter/X
SPACING_TOKENS.safe_area.presentation            # Slides/presentations
SPACING_TOKENS.safe_area.square                  # 1:1 format
SPACING_TOKENS.safe_area.ultrawide               # 21:9 cinematic
```

**Each includes**:
- `top, bottom, left, right`: Safe margins in pixels
- `critical_zones`: Specific UI overlay zones
- `aspect_ratio`: Target aspect ratio
- `ui_overlays`: What UI elements to avoid
- `description`, `usage`, `notes`

#### Example: TikTok Safe Area

```python
{
    "top": 100,           # Top bar
    "bottom": 180,        # Bottom controls
    "left": 24,
    "right": 80,          # Side buttons
    "critical_zones": {
        "top_bar": {"top": 0, "height": 100},
        "side_controls": {"right": 0, "width": 80, "top": 200, "bottom": 300},
        "bottom_info": {"bottom": 0, "height": 180},
        "caption_zone": {"bottom": 180, "height": 100, "left": 24, "right": 80},
    },
    "aspect_ratio": "9:16",
    "ui_overlays": [
        "top info (100px)",
        "right controls (80px)",
        "bottom caption + CTA (180px)",
    ],
}
```

### Border Tokens

```python
SPACING_TOKENS.border_radius.none      # 0
SPACING_TOKENS.border_radius.xs        # 2px
SPACING_TOKENS.border_radius.sm        # 4px
SPACING_TOKENS.border_radius.md        # 8px
SPACING_TOKENS.border_radius.lg        # 12px
SPACING_TOKENS.border_radius.xl        # 16px
SPACING_TOKENS.border_radius.xxl       # 24px
SPACING_TOKENS.border_radius.xxxl      # 32px
SPACING_TOKENS.border_radius.full      # 9999px (pills)

SPACING_TOKENS.border_width.none       # 0
SPACING_TOKENS.border_width.thin       # 1px
SPACING_TOKENS.border_width.base       # 2px
SPACING_TOKENS.border_width.thick      # 4px
SPACING_TOKENS.border_width.heavy      # 8px
SPACING_TOKENS.border_width.ultra      # 12px
```

---

## Brand Packs

**Location**: `src/chuk_motion/tokens/brand.py`

White-labeling and client-specific customization system.

### Available Brand Packs

```python
from chuk_motion.tokens.brand import BRAND_PACKS

BRAND_PACKS.default             # Clean, professional default
BRAND_PACKS.tech_startup        # Modern, energetic tech
BRAND_PACKS.enterprise          # Professional, corporate
BRAND_PACKS.creator             # Vibrant, personality-driven
BRAND_PACKS.education           # Clear, approachable
```

### Using Brand Packs

```python
from chuk_motion.tokens.brand import get_brand_pack, merge_brand_pack

# Get a brand pack
brand = get_brand_pack("tech_startup")

# Merge custom overrides
custom_brand = merge_brand_pack("tech_startup", {
    "logo": {"url": "client-logo.png"},
    "colors": {"primary": ["#custom-color"]},
})

# List all available packs
from chuk_motion.tokens.brand import list_brand_packs
packs = list_brand_packs()
```

---

## Caption Styles

**Location**: `src/chuk_motion/tokens/captions.py`

Platform-specific caption styling presets.

### Available Caption Styles

```python
from chuk_motion.tokens.captions import CAPTION_STYLES

CAPTION_STYLES.burst          # MrBeast / Ali Abdaal style
CAPTION_STYLES.precise        # Kurzgesagt style
CAPTION_STYLES.headline       # LinkedIn headline blocks
CAPTION_STYLES.minimal        # Clean professional
CAPTION_STYLES.neon           # Gaming / tech high energy
CAPTION_STYLES.classic        # Documentary style
```

### Display Modes

- **word_by_word**: One or more words at a time (MrBeast style)
- **phrase_by_phrase**: 4-6 words per caption (Kurzgesagt style)
- **line_by_line**: Full lines (LinkedIn style)
- **full_sentence**: Complete sentences (documentary style)

### Using Caption Styles

```python
from chuk_motion.tokens.captions import get_caption_style, get_style_for_platform

# Get a caption style
style = get_caption_style("burst")

# Get recommended style for platform
recommended = get_style_for_platform("tiktok")  # Returns "burst"

# List all styles
from chuk_motion.tokens.captions import list_caption_styles
styles = list_caption_styles()
```

---

## Usage Guide

### For Component Development

```python
# Import tokens
from chuk_motion.tokens.motion import MOTION_TOKENS
from chuk_motion.tokens.spacing import SPACING_TOKENS

# Use in component - convert Pydantic model to dict
entrance = spring({
    "frame": relativeFrame,
    "fps": fps,
    "config": MOTION_TOKENS.spring_configs.smooth.config.model_dump(),
})

# Apply safe area
safe_area = SPACING_TOKENS.safe_area.tiktok.model_dump()
margin_top = safe_area["top"]
```

### For MCP Server Integration

```python
from chuk_motion.tokens.brand import get_brand_pack
from chuk_motion.tokens.captions import get_style_for_platform
from chuk_motion.tokens.spacing import SPACING_TOKENS

# Get platform-specific settings
platform = "tiktok"
brand = get_brand_pack("tech_startup")
caption_style = get_style_for_platform(platform)
safe_area = SPACING_TOKENS.safe_area[platform].model_dump()

# Generate video with these settings
video = generate_video(
    brand_pack=brand,
    caption_style=caption_style,
    safe_area=safe_area,
)
```

### Token Manager for Import/Export

```python
from chuk_motion.tokens.token_manager import TokenManager
from chuk_virtual_fs import AsyncVirtualFileSystem

# Initialize
vfs = AsyncVirtualFileSystem()
manager = TokenManager(vfs)

# Export tokens
await manager.export_typography_tokens("my_typography.json")
await manager.export_color_tokens("my_colors.json")
await manager.export_motion_tokens("my_motion.json")
await manager.export_spacing_tokens("my_spacing.json")

# Export all tokens at once
await manager.export_all_tokens("my_tokens_dir")

# Import tokens
await manager.import_typography_tokens("custom_typography.json")
await manager.import_color_tokens("custom_colors.json", merge=True)

# Get custom tokens
custom_font = manager.get_typography_token("font_families", "custom_font")
custom_color = manager.get_color_token("custom_theme", "primary")
```

---

## MCP Tools

### Typography Token Tools

- `remotion_list_typography_tokens()` - List all typography tokens
- `remotion_get_font_families()` - Get available font family definitions
- `remotion_get_font_sizes(resolution)` - Get font sizes for specific resolution
- `remotion_get_text_style(style_name)` - Get specific text style preset

### Color Token Tools

- `remotion_list_color_tokens()` - List all color tokens for all themes
- `remotion_get_theme_colors(theme_name)` - Get colors for specific theme
- `remotion_get_color_value(theme_name, color_type, index)` - Get specific color value

### Motion Token Tools

- `remotion_list_motion_tokens()` - List all motion design tokens
- `remotion_get_spring_configs()` - Get all spring animation configurations
- `remotion_get_spring_config(spring_name)` - Get specific spring configuration
- `remotion_get_easing_curves()` - Get all easing curve definitions
- `remotion_get_easing_curve(easing_name)` - Get specific easing curve
- `remotion_get_durations()` - Get all duration presets
- `remotion_get_duration(duration_name)` - Get specific duration preset
- `remotion_get_animation_presets()` - Get all animation presets
- `remotion_get_youtube_optimizations()` - Get YouTube optimization guidelines

### Token Management Tools

- `remotion_export_typography_tokens(file_path)` - Export typography tokens
- `remotion_import_typography_tokens(file_path)` - Import typography tokens
- `remotion_export_color_tokens(file_path, theme_name)` - Export color tokens
- `remotion_import_color_tokens(file_path)` - Import color tokens
- `remotion_export_motion_tokens(file_path)` - Export motion tokens
- `remotion_import_motion_tokens(file_path)` - Import motion tokens
- `remotion_export_all_tokens(output_dir)` - Export all token types

---

## Best Practices

1. **Always use tokens** instead of hardcoded values
2. **Use Pydantic models** - Access tokens as attributes (e.g., `MOTION_TOKENS.duration.normal`)
3. **Convert to dicts when needed** - Use `.model_dump()` for JSON serialization
4. **Resolution-aware typography** - Choose font sizes based on video resolution
5. **Consistent motion** - Use motion tokens for consistent animation feel
6. **Platform-specific safe areas** - Always apply safe areas for target platform
7. **Theme consistency** - Stick to one theme's tokens throughout a video

### Pydantic Model Usage

```python
# Access tokens as Pydantic model attributes
duration = MOTION_TOKENS.duration.normal

# Access nested properties
damping = MOTION_TOKENS.spring_configs.smooth.config.damping

# Convert to dict for JSON serialization
duration_dict = MOTION_TOKENS.duration.normal.model_dump()

# Convert entire model to dict
all_motion = MOTION_TOKENS.model_dump()
```

---

## Token Quick Reference

```
Typography:
  TYPOGRAPHY_TOKENS.font_families.[display|body|monospace|decorative]
  TYPOGRAPHY_TOKENS.font_sizes.[video_1080p|video_4k|video_720p].[xs|sm|base|lg|xl|2xl|3xl|4xl]
  TYPOGRAPHY_TOKENS.font_weights.[thin|regular|medium|semibold|bold|extrabold|black]
  TYPOGRAPHY_TOKENS.text_styles.[hero_title|title|heading|body|caption]

Color:
  COLOR_TOKENS[theme_name]["primary"|"accent"|"gradient"|"background"|"text"|"semantic"]

Motion:
  MOTION_TOKENS.duration.[instant|ultra_fast|fast|normal|medium|slow|slower|ultra_slow]
  MOTION_TOKENS.easing.[linear|ease|ease_in|ease_out|ease_in_out|bounce|elastic|...]
  MOTION_TOKENS.spring_configs.[gentle|smooth|bouncy|snappy|stiff]
  MOTION_TOKENS.enter.[fade_in|fade_up|slide_in_left|scale_in|zoom_in|bounce_in|...]
  MOTION_TOKENS.exit.[fade_out|slide_out_left|scale_out|zoom_out|pull_back|...]
  MOTION_TOKENS.tempo.[sprint|fast|medium|slow|cinematic]
  MOTION_TOKENS.platform_timing.[youtube_long_form|tiktok|instagram_reel|...]

Spacing:
  SPACING_TOKENS.spacing.[none|xxs|xs|sm|md|lg|xl|xxl|xxxl|...]
  SPACING_TOKENS.safe_area.[desktop|mobile|youtube_shorts|tiktok|instagram_reel|...]
  SPACING_TOKENS.border_radius.[none|xs|sm|md|lg|xl|xxl|xxxl|full]

Brand:
  BRAND_PACKS.[default|tech_startup|enterprise|creator|education]

Captions:
  CAPTION_STYLES.[burst|precise|headline|minimal|neon|classic]
```

---

## Source Files

- Typography tokens: `src/chuk_motion/tokens/typography.py`
- Color tokens: `src/chuk_motion/tokens/colors.py`
- Motion tokens: `src/chuk_motion/tokens/motion.py`
- Spacing tokens: `src/chuk_motion/tokens/spacing.py`
- Brand packs: `src/chuk_motion/tokens/brand.py`
- Caption styles: `src/chuk_motion/tokens/captions.py`
- Token manager: `src/chuk_motion/tokens/token_manager.py`

---

**Last Updated**: November 2025
**Version**: 2.0.0
**Status**: Production Ready
