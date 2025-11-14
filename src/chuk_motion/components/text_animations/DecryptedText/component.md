# DecryptedText

**Category:** Text Animation
**Purpose:** Animated text reveal with character scrambling effect

## Overview

DecryptedText creates a dramatic text reveal animation where characters progressively "decrypt" from random scrambled characters to reveal the final text. Perfect for adding impact and intrigue to text reveals, especially for technical, hacker-themed, or mystery content.

## How It Works

Characters start as random scrambled symbols and progressively reveal the actual text based on the reveal direction:
- **start**: Reveals from left to right
- **end**: Reveals from right to left
- **center**: Reveals outward from the center

The scrambling effect creates a Matrix-like, decryption aesthetic that's attention-grabbing and dynamic.

## Parameters

- **text**: Text to animate (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "3xl")
- **font_weight**: Font weight - normal, medium, semibold, bold, extrabold, black (default: "bold")
- **text_color**: Text color (uses on_dark color if not specified)
- **reveal_direction**: Direction of reveal - start, end, center (default: "start")
- **scramble_speed**: Speed of character scrambling, higher = faster (default: 3.0)
- **position**: Vertical position - center, top, bottom (default: "center")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['3xl']`, `font_weights.bold`, `primary_font`, `letter_spacing.wide`
- **Colors:** Uses `text.on_dark` by default
- **Spacing:** Uses `spacing.xl` and `spacing['4xl']`

## Reveal Direction Guide

- **start (left-to-right)**: Most natural reading order, professional
- **end (right-to-left)**: Unusual, attention-grabbing, mysterious
- **center (outward)**: Dramatic, focuses attention on center text

## Examples

```python
# Basic decrypted text reveal
{
    "type": "DecryptedText",
    "config": {
        "text": "Access Granted",
        "font_size": "4xl",
        "reveal_direction": "start",
        "duration": 3.0
    }
}

# Center-out reveal with custom styling
{
    "type": "DecryptedText",
    "config": {
        "text": "System Initialized",
        "reveal_direction": "center",
        "font_weight": "extrabold",
        "scramble_speed": 5.0,
        "duration": 4.0
    }
}

# End-to-start reveal (right to left)
{
    "type": "DecryptedText",
    "config": {
        "text": "Decoding Complete",
        "reveal_direction": "end",
        "position": "top",
        "text_color": "#00FF00",
        "scramble_speed": 4.0
    }
}

# Slow dramatic reveal
{
    "type": "DecryptedText",
    "config": {
        "text": "CLASSIFIED",
        "font_size": "3xl",
        "font_weight": "black",
        "scramble_speed": 2.0,
        "reveal_direction": "center",
        "duration": 5.0
    }
}
```

## Best Practices

1. **Use font_size 3xl or 4xl** for maximum impact and readability
2. **Keep text short** (1-4 words) for best effect - longer text can feel cluttered
3. **scramble_speed 3.0-5.0** for most cases (slower = more dramatic, faster = more energetic)
4. **Use reveal_direction: center** for the most dramatic, attention-grabbing effect
5. **Green text (#00FF00)** creates classic hacker/Matrix aesthetic
6. **Duration 3-5 seconds** gives enough time to appreciate the animation

## Common Use Cases

- **Dramatic text reveals** for key messages or titles
- **Code/hacker aesthetics** for technical or cybersecurity content
- **Mystery unveilings** for suspenseful reveals
- **System messages** for UI/UX demonstrations
- **Access granted screens** for authentication flows
- **Tech product launches** for futuristic, cutting-edge feel
- **Gaming content** for achievement unlocks or level completions

## Visual Feel

- **Dramatic:** Creates suspense and anticipation as text reveals
- **Technical:** Matrix-like scrambling feels code-y and technical
- **Attention-grabbing:** Unusual animation captures viewer focus
- **Modern:** Futuristic, digital aesthetic
- **Mysterious:** Reveals text progressively, creating intrigue
