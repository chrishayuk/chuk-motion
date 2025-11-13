# WavyText

**Category:** Text Animation
**Purpose:** Continuous wave motion animation on characters

## Overview

WavyText creates a playful, continuous wave motion effect where each character oscillates vertically with a phase offset, creating a smooth wave pattern across the text. Perfect for fun, energetic content like music videos, party themes, or any project that needs a dynamic, bouncy aesthetic.

## How It Works

The component applies a sinusoidal wave motion to each character:
- **Wave amplitude**: Controls the height of the vertical oscillation
- **Wave frequency**: Determines the spacing between wave peaks (how tight the wave is)
- **Wave speed**: Controls how fast the wave moves through the text
- **Phase offset**: Each character starts at a different point in the wave cycle, creating the continuous wave effect

## Parameters

- **text**: Text to animate with wave (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "4xl")
- **font_weight**: Font weight - normal, medium, semibold, bold, extrabold, black (default: "bold")
- **text_color**: Text color (uses on_dark color if not specified)
- **wave_amplitude**: Height of wave oscillation in pixels, 5-50 (default: 20.0)
- **wave_speed**: Speed of wave motion, 0.1-5.0 (default: 1.0)
- **wave_frequency**: Frequency of wave (spacing between peaks), 0.1-2.0 (default: 0.3)
- **position**: Vertical position - center, top, bottom (default: "center")
- **align**: Text alignment - left, center, right (default: "center")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['4xl']`, `font_weights.bold`, `primary_font`, `letter_spacing.wide`
- **Colors:** Uses `text.on_dark` by default
- **Spacing:** Uses `spacing.xl` and `spacing['4xl']`

## Wave Configuration Guide

### Amplitude
- **5-10px**: Subtle bounce, professional but playful
- **15-25px**: Moderate wave, clear motion (recommended)
- **30-40px**: Dramatic wave, very animated
- **45-50px**: Extreme wave, use sparingly for high energy

### Frequency
- **0.1-0.2**: Wide waves, gentle rolling motion
- **0.3-0.5**: Medium waves, balanced aesthetic (recommended)
- **0.6-1.0**: Tight waves, more peaks visible
- **1.5-2.0**: Very tight waves, rapid oscillation

### Speed
- **0.1-0.5**: Slow, smooth, calming
- **0.8-1.2**: Medium speed, energetic (recommended)
- **1.5-3.0**: Fast, exciting, high energy
- **3.5-5.0**: Very fast, frantic, use for impact

## Examples

```python
# Basic wave text
{
    "type": "WavyText",
    "config": {
        "text": "WAVE",
        "font_size": "4xl",
        "wave_amplitude": 20.0,
        "wave_frequency": 0.3,
        "wave_speed": 1.0,
        "duration": 3.0
    }
}

# Gentle rolling wave
{
    "type": "WavyText",
    "config": {
        "text": "Smooth Vibes",
        "font_size": "3xl",
        "wave_amplitude": 15.0,
        "wave_frequency": 0.2,
        "wave_speed": 0.5,
        "font_weight": "semibold"
    }
}

# High energy party text
{
    "type": "WavyText",
    "config": {
        "text": "LET'S GO!",
        "font_size": "4xl",
        "font_weight": "black",
        "wave_amplitude": 35.0,
        "wave_frequency": 0.4,
        "wave_speed": 2.0,
        "text_color": "#FF00FF"
    }
}

# Music video title
{
    "type": "WavyText",
    "config": {
        "text": "Summer Nights",
        "font_size": "4xl",
        "wave_amplitude": 25.0,
        "wave_frequency": 0.3,
        "wave_speed": 1.2,
        "position": "center",
        "text_color": "#00FFFF",
        "duration": 5.0
    }
}

# Subtle professional wave
{
    "type": "WavyText",
    "config": {
        "text": "Innovation",
        "font_size": "3xl",
        "font_weight": "medium",
        "wave_amplitude": 8.0,
        "wave_frequency": 0.25,
        "wave_speed": 0.8,
        "position": "top"
    }
}
```

## Best Practices

1. **Use wave_amplitude 15-25px** for most cases - visible but not overwhelming
2. **wave_frequency 0.3-0.5** creates the most natural wave pattern
3. **wave_speed 0.8-1.5** for energetic but not frantic motion
4. **Keep text short** (1-4 words) for best visual impact
5. **Bold fonts work best** - wave motion is more visible with heavier weights
6. **Bright colors** enhance the playful feel (#FF00FF, #00FFFF, #FFFF00)
7. **Use larger font sizes** (3xl, 4xl) to make wave motion more apparent

## Common Use Cases

- **Fun titles** for lighthearted or playful content
- **Music videos** for dance, pop, or energetic tracks
- **Creative content** for artistic or experimental projects
- **Playful effects** for children's content or entertainment
- **Party/celebration themes** for events, festivals, or celebrations
- **Product launches** with fun, approachable branding
- **Social media content** for attention-grabbing posts
- **Gaming content** for casual or arcade-style games

## Visual Feel

- **Playful:** Bouncy motion creates a fun, lighthearted atmosphere
- **Energetic:** Continuous movement adds dynamism and life
- **Rhythmic:** Wave pattern creates a sense of flow and rhythm
- **Attention-grabbing:** Motion naturally draws the eye
- **Youthful:** Feels fresh, modern, and approachable
- **Musical:** Wave motion evokes audio waveforms and music visualization
