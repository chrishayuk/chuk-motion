# FuzzyText

**Category:** Text Animation
**Purpose:** Animated text with scanline distortion and glitch effects

## Overview

FuzzyText creates a VHS-style fuzzy text effect with scanline distortion, horizontal displacement, and RGB split. Perfect for retro aesthetics, glitch art, and cyberpunk themes that need that authentic analog degradation feel.

## How It Works

The component applies multiple visual effects to create the fuzzy VHS aesthetic:
- **Scanlines**: Horizontal lines that mimic CRT/VHS display artifacts
- **Glitch displacement**: Random horizontal offsets that create the "tracking error" look
- **RGB split**: Chromatic aberration effect separating color channels
- **Animation** (optional): Continuously changing glitch patterns for dynamic effect

## Parameters

- **text**: Text to display with fuzzy effect (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "3xl")
- **font_weight**: Font weight - normal, medium, semibold, bold, extrabold, black (default: "bold")
- **text_color**: Text color (uses on_dark color if not specified)
- **glitch_intensity**: Intensity of glitch displacement, 0-20 (default: 5.0)
- **scanline_height**: Height of scanlines in pixels (default: 2.0)
- **animate**: Whether to animate the glitch effect (default: true)
- **position**: Vertical position - center, top, bottom (default: "center")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['3xl']`, `font_weights.bold`, `primary_font`, `letter_spacing.wide`
- **Colors:** Uses `text.on_dark` by default
- **Spacing:** Uses `spacing.xl` and `spacing['4xl']`

## Glitch Intensity Guide

- **0-3**: Subtle VHS wear, barely noticeable
- **4-7**: Moderate VHS degradation, authentic retro feel (recommended)
- **8-12**: Heavy glitching, cyberpunk aesthetic
- **13-20**: Extreme distortion, barely readable (use sparingly for impact)

## Examples

```python
# Basic fuzzy text with animation
{
    "type": "FuzzyText",
    "config": {
        "text": "GLITCH EFFECT",
        "font_size": "4xl",
        "glitch_intensity": 8.0,
        "duration": 3.0
    }
}

# Static fuzzy text (no animation)
{
    "type": "FuzzyText",
    "config": {
        "text": "VHS Aesthetic",
        "animate": False,
        "glitch_intensity": 3.0,
        "scanline_height": 1.5
    }
}

# High-intensity cyberpunk glitch
{
    "type": "FuzzyText",
    "config": {
        "text": "SYSTEM ERROR",
        "glitch_intensity": 15.0,
        "font_weight": "extrabold",
        "position": "top",
        "text_color": "#FF00FF"
    }
}

# Subtle VHS title card
{
    "type": "FuzzyText",
    "config": {
        "text": "1987",
        "font_size": "4xl",
        "font_weight": "black",
        "glitch_intensity": 2.0,
        "scanline_height": 1.0,
        "animate": False
    }
}
```

## Best Practices

1. **Use glitch_intensity 5-8** for authentic VHS feel without being overbearing
2. **Static vs animated**: Set `animate: False` for title cards, `True` for dynamic scenes
3. **scanline_height 1.5-2.5** works best for most cases
4. **Pair with dark backgrounds** for maximum effect (scanlines show better)
5. **Use short text** (1-3 words) for best readability
6. **Magenta/cyan colors (#FF00FF, #00FFFF)** enhance the cyberpunk aesthetic

## Common Use Cases

- **Retro VHS aesthetics** for 80s/90s themed content
- **Glitch art effects** for experimental/artistic videos
- **Cyberpunk themes** for sci-fi or tech content
- **System error messages** for UI/technical demonstrations
- **80s/90s retro titles** for nostalgic content
- **Music videos** with retro or glitch aesthetics
- **Horror content** with found footage or analog horror themes

## Visual Feel

- **Nostalgic:** Evokes memories of VHS tapes and CRT TVs
- **Distorted:** Intentional degradation creates unique aesthetic
- **Retro-futuristic:** Combines 80s tech with modern cyberpunk
- **Glitchy:** Unpredictable movement feels dynamic and alive
- **Analog:** Warm, imperfect, human quality vs digital perfection
