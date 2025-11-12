# Theme System

The theme system in `chuk-motion` provides complete, production-ready design systems optimized for YouTube video content. Each theme combines color palettes, typography, and motion design into a cohesive visual language.

## Overview

Themes are the highest-level abstraction in the design system hierarchy:

```
Design Tokens (Colors, Typography, Motion) → Themes → Components
```

Each theme includes:
- **Color Palette**: Primary, accent, background, text, and semantic colors
- **Typography**: Font families, sizes, and text styles
- **Motion Design**: Spring configurations, easing curves, and duration presets
- **Use Cases**: Recommended content types for the theme

## Available Themes

### Tech Theme

**Visual Identity**: Modern tech aesthetic with blue/cyan palette

**Color Palette**:
- Primary: Blue (#0066FF, #0052CC, #003D99)
- Accent: Cyan (#00D9FF, #00B8D4, #0097A7)
- Gradient: Blue to Cyan
- Background: Dark (#0A0E1A), Light (#F5F7FA)

**Typography**:
- Primary Font: Display (Inter, SF Pro Display)
- Body Font: Body (Inter, SF Pro Text)
- Code Font: Monospace (JetBrains Mono, Fira Code)
- Default Resolution: 1080p

**Motion Design**:
- Spring: Smooth (balanced, natural motion)
- Easing: Ease Out (starts fast, decelerates)
- Duration: Normal (0.667s / 20 frames)

**Best For**:
- Tech reviews and product demos
- Coding tutorials and programming content
- Software demonstrations
- Tech news and announcements
- Product launches

**Example Usage**:
```python
from chuk_motion.themes.youtube_themes import YOUTUBE_THEMES

tech_theme = YOUTUBE_THEMES["tech"]
primary_color = tech_theme["colors"]["primary"][0]  # #0066FF
```

---

### Finance Theme

**Visual Identity**: Professional finance with green/gold palette

**Color Palette**:
- Primary: Green (#00C853, #00A843, #008833)
- Accent: Gold (#FFD600, #FFAB00, #FF6F00)
- Gradient: Green to Gold
- Background: Dark (#0D1B0D), Light (#F8FAF8)

**Typography**:
- Primary Font: Display
- Body Font: Body
- Code Font: Monospace
- Default Resolution: 1080p

**Motion Design**:
- Spring: Snappy (quick, responsive motion)
- Easing: Ease In Out (slow start and end)
- Duration: Normal (0.667s / 20 frames)

**Best For**:
- Stock market analysis
- Investing and trading advice
- Business news and updates
- Financial education content
- Cryptocurrency analysis

---

### Education Theme

**Visual Identity**: Friendly education with purple/orange palette

**Color Palette**:
- Primary: Purple (#7C4DFF, #651FFF, #6200EA)
- Accent: Orange (#FF6E40, #FF5722, #F4511E)
- Gradient: Purple to Orange
- Background: Dark (#1A0F2E), Light (#FAF7FC)

**Typography**:
- Primary Font: Display
- Body Font: Body
- Code Font: Monospace
- Default Resolution: 1080p

**Motion Design**:
- Spring: Bouncy (playful spring with overshoot)
- Easing: Ease Out Back (overshoots then settles)
- Duration: Moderate (1.0s / 30 frames)

**Best For**:
- Educational content and tutorials
- Explainer videos
- Online course content
- Study guides and lessons
- Academic lectures

---

### Lifestyle Theme

**Visual Identity**: Warm lifestyle with coral/pink palette

**Color Palette**:
- Primary: Pink (#FF6B9D, #E91E63, #C2185B)
- Accent: Coral/Orange (#FFB74D, #FFA726, #FF9800)
- Gradient: Pink to Coral
- Background: Dark (#2E1A26), Light (#FFF9FA)

**Typography**:
- Primary Font: Decorative (Poppins, Montserrat)
- Body Font: Body
- Code Font: Body (no monospace for lifestyle)
- Default Resolution: 1080p

**Motion Design**:
- Spring: Gentle (soft, slow spring motion)
- Easing: Ease In Out (smooth transitions)
- Duration: Slow (1.5s / 45 frames)

**Best For**:
- Vlogs and personal content
- Lifestyle and wellness videos
- Travel vlogs
- Daily routines and habits
- Beauty and fashion content

---

### Gaming Theme

**Visual Identity**: High-energy gaming with neon accents

**Color Palette**:
- Primary: Neon Green (#00E676, #00C853, #00BFA5)
- Accent: Neon Purple (#E040FB, #D500F9, #AA00FF)
- Gradient: Neon Green to Neon Purple
- Background: Dark (#0F0F1A), Light (#F0F0F5)

**Typography**:
- Primary Font: Display
- Body Font: Display (bold for gaming)
- Code Font: Monospace
- Default Resolution: 1080p

**Motion Design**:
- Spring: Elastic (strong elastic overshoot)
- Easing: Ease Out Back (attention-grabbing)
- Duration: Fast (0.333s / 10 frames)

**Best For**:
- Gaming videos and let's plays
- Esports highlights and tournaments
- Stream overlays and alerts
- Gaming reviews and analysis
- Speedruns and walkthroughs

---

### Minimal Theme

**Visual Identity**: Clean minimal with monochrome palette

**Color Palette**:
- Primary: Gray (#212121, #424242, #616161)
- Accent: Light (#FFFFFF, #F5F5F5, #EEEEEE)
- Gradient: Dark Gray to Gray
- Background: Dark (#000000), Light (#FFFFFF)

**Typography**:
- Primary Font: Display
- Body Font: Body
- Code Font: Monospace
- Default Resolution: 1080p

**Motion Design**:
- Spring: Smooth (balanced motion)
- Easing: Ease In Out (smooth transitions)
- Duration: Normal (0.667s / 20 frames)

**Best For**:
- Professional content
- Corporate videos
- Documentaries
- Interviews and conversations
- Minimalist aesthetics

---

### Business Theme

**Visual Identity**: Professional business with navy/teal palette

**Color Palette**:
- Primary: Navy (#1565C0, #0D47A1, #01579B)
- Accent: Teal (#00ACC1, #0097A7, #00838F)
- Gradient: Navy to Teal
- Background: Dark (#0A1929), Light (#F5F8FA)

**Typography**:
- Primary Font: Display
- Body Font: Body
- Code Font: Monospace
- Default Resolution: 1080p

**Motion Design**:
- Spring: Snappy (quick, professional)
- Easing: Ease In Out (smooth transitions)
- Duration: Normal (0.667s / 20 frames)

**Best For**:
- Corporate videos and presentations
- Business presentations and pitches
- B2B content and marketing
- Company updates and announcements
- Professional training videos

---

## Theme Structure

Each theme is defined as a Python dictionary with the following structure:

```python
{
    "name": "Theme Name",
    "description": "Theme description",
    "colors": {
        # Color palette from COLOR_TOKENS
    },
    "typography": {
        "primary_font": {...},
        "body_font": {...},
        "code_font": {...},
        "default_resolution": "video_1080p"
    },
    "motion": {
        "default_spring": {...},
        "default_easing": {...},
        "default_duration": {...}
    },
    "use_cases": [
        # List of recommended use cases
    ]
}
```

## Using Themes

### Accessing Theme Data

```python
from chuk_motion.themes.youtube_themes import YOUTUBE_THEMES

# Get a specific theme
tech_theme = YOUTUBE_THEMES["tech"]

# Access theme properties
theme_name = tech_theme["name"]
primary_colors = tech_theme["colors"]["primary"]
default_spring = tech_theme["motion"]["default_spring"]
```

### Listing All Themes

```python
# Get all theme names
theme_names = list(YOUTUBE_THEMES.keys())
# ['tech', 'finance', 'education', 'lifestyle', 'gaming', 'minimal', 'business']

# Get theme metadata
for theme_key, theme in YOUTUBE_THEMES.items():
    print(f"{theme['name']}: {theme['description']}")
```

### Theme Selection Guide

Choose a theme based on your content type:

| Content Type | Recommended Theme | Alternative |
|--------------|------------------|-------------|
| Tech Reviews | Tech | Minimal |
| Financial Content | Finance | Business |
| Tutorials | Education | Tech |
| Vlogs | Lifestyle | Minimal |
| Gaming | Gaming | Tech |
| Corporate | Business | Minimal |
| Creative | Lifestyle | Education |

## Theme Manager

The `ThemeManager` class provides centralized theme management with advanced features like registration, validation, export/import, and custom theme creation.

### Creating a Theme Manager

```python
from chuk_motion.themes.theme_manager import ThemeManager

# Create manager (automatically loads built-in themes)
manager = ThemeManager()

# List all themes
themes = manager.list_themes()
# Returns: ['tech', 'finance', 'education', 'lifestyle', 'gaming', 'minimal', 'business']

# Get theme object
tech_theme = manager.get_theme("tech")

# Get detailed theme info
theme_info = manager.get_theme_info("tech")
```

### Theme Manager Features

#### Search Themes
```python
# Search by keyword
gaming_themes = manager.search_themes("gaming")
# Returns themes matching "gaming" in name, description, or use cases

# Get themes for content category
education_themes = manager.get_themes_by_category("education")
```

#### Compare Themes
```python
# Compare two themes side by side
comparison = manager.compare_themes("tech", "gaming")
# Returns detailed comparison of colors, motion, and use cases
```

#### Set Active Theme
```python
# Set current theme for session
manager.set_current_theme("tech")

# Get current theme
current = manager.get_current_theme()  # Returns "tech"
```

#### Create Custom Themes
```python
# Create custom theme based on existing theme
custom_key = manager.create_custom_theme(
    name="My Brand",
    description="Custom brand colors",
    base_theme="tech",
    color_overrides={
        "primary": ["#FF0000", "#CC0000", "#990000"],
        "accent": ["#00FF00", "#00CC00", "#009900"]
    }
)
```

#### Export/Import Themes
```python
# Export theme to JSON
file_path = manager.export_theme("tech", "my_tech_theme.json")

# Import theme from JSON
manager.import_theme("custom_theme.json", theme_key="custom")
```

#### Validate Themes
```python
# Validate theme data structure
theme_data = {...}  # Theme dictionary
validation = manager.validate_theme(theme_data)

if validation["valid"]:
    print("Theme is valid!")
else:
    print(f"Errors: {validation['errors']}")
```

## MCP Tools for Themes

The following MCP tools are available for theme management through Claude or other MCP clients:

### Discovery Tools

#### `remotion_list_themes()`
List all available themes with metadata.

```python
# Returns JSON with all themes
{
  "themes": [
    {
      "key": "tech",
      "name": "Tech",
      "description": "Modern tech aesthetic",
      "primary_color": "#0066FF",
      "accent_color": "#00D9FF",
      "use_cases": ["Tech reviews", "Coding tutorials", "Software demos"]
    },
    // ... more themes
  ]
}
```

#### `remotion_get_theme_info(theme_name: str)`
Get detailed information about a specific theme.

```python
# Example: Get tech theme info
remotion_get_theme_info(theme_name="tech")

# Returns complete theme with all tokens
{
  "name": "Tech",
  "description": "Modern tech aesthetic",
  "colors": {...},
  "typography": {...},
  "motion": {...},
  "use_cases": [...]
}
```

#### `remotion_search_themes(query: str)`
Search themes by keyword.

```python
# Example: Find professional themes
remotion_search_themes(query="professional")

# Returns matching themes
{
  "query": "professional",
  "matches": [
    {"key": "business", "name": "Business", ...},
    {"key": "minimal", "name": "Minimal", ...}
  ]
}
```

### Comparison Tools

#### `remotion_compare_themes(theme1: str, theme2: str)`
Compare two themes side by side.

```python
# Example: Compare tech vs gaming
remotion_compare_themes(theme1="tech", theme2="gaming")

# Returns detailed comparison
{
  "themes": ["tech", "gaming"],
  "comparison": {
    "primary_colors": [...],
    "accent_colors": [...],
    "motion_feel": ["Smooth", "Elastic"],
    "use_cases": [...]
  }
}
```

### Session Management

#### `remotion_set_current_theme(theme_name: str)`
Set the active theme for the session.

```python
# Example: Set gaming theme as default
remotion_set_current_theme(theme_name="gaming")
```

#### `remotion_get_current_theme()`
Get the currently active theme.

```python
# Returns current theme info
{
  "current_theme": "gaming",
  "info": {...}
}
```

### Custom Theme Tools

#### `remotion_create_custom_theme(...)`
Create a custom theme with overrides.

```python
# Example: Create branded theme
remotion_create_custom_theme(
    name="My Brand",
    description="Custom brand colors",
    base_theme="tech",
    primary_colors='["#FF0000", "#CC0000", "#990000"]',
    accent_colors='["#00FF00", "#00CC00", "#009900"]'
)
```

#### `remotion_export_theme(theme_name: str, file_path: str)`
Export theme to JSON file.

```python
# Example: Export tech theme
remotion_export_theme(
    theme_name="tech",
    file_path="my_tech_theme.json"
)
```

#### `remotion_import_theme(file_path: str, theme_key: str)`
Import theme from JSON file.

```python
# Example: Import custom theme
remotion_import_theme(
    file_path="custom_theme.json",
    theme_key="my_custom"
)
```

#### `remotion_validate_theme(theme_data: str)`
Validate theme JSON structure.

```python
# Example: Validate theme before import
remotion_validate_theme(theme_data='{"name": "Custom", ...}')
```

### Content-Based Selection

#### `remotion_get_theme_for_content(content_type: str)`
Get recommended themes for content type.

```python
# Example: Find themes for gaming content
remotion_get_theme_for_content(content_type="gaming")

# Returns recommendations
{
  "content_type": "gaming",
  "recommendations": [
    {"key": "gaming", "name": "Gaming", ...},
    {"key": "tech", "name": "Tech", ...}
  ]
}
```

## Customizing Themes

While themes provide sensible defaults, you can customize any aspect:

```python
# Method 1: Direct modification
custom_theme = YOUTUBE_THEMES["tech"].copy()
custom_theme["colors"]["primary"][0] = "#FF0000"
custom_theme["motion"]["default_spring"] = MOTION_TOKENS["spring_configs"]["bouncy"]

# Method 2: Using ThemeManager
manager = ThemeManager()
custom_key = manager.create_custom_theme(
    name="Custom Tech",
    description="Tech theme with custom colors",
    base_theme="tech",
    color_overrides={"primary": ["#FF0000", "#CC0000", "#990000"]}
)
```

## Theme Best Practices

### 1. Consistency
- Stick to one theme per video for visual consistency
- Use theme colors consistently across all components
- Follow theme typography recommendations

### 2. Accessibility
- All themes are designed with contrast ratios in mind
- Use `text.on_dark` for text on dark backgrounds
- Use `text.on_light` for text on light backgrounds

### 3. Performance
- Themes are optimized for 1080p by default
- Adjust font sizes for 720p or 4K using typography tokens
- Motion settings are tuned for smooth playback

### 4. Branding
- If you have brand colors, consider customizing a theme
- Start with the closest matching theme
- Override primary and accent colors while keeping structure

## Related Documentation

- [Token System](./token-system.md) - Deep dive into design tokens
- [Components](../README.md#component-catalog) - Using themes with components
- [Typography Tokens](./token-system.md#typography-tokens) - Font system details
- [Color Tokens](./token-system.md#color-tokens) - Color palette details
- [Motion Tokens](./token-system.md#motion-tokens) - Animation system details

## Source Files

Theme definitions: `src/chuk_motion/themes/youtube_themes.py`
