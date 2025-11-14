# TypewriterText

**Category:** Text Animation
**Purpose:** Classic typewriter animation with cursor

## Overview

TypewriterText creates an authentic typewriter effect where characters appear one-by-one as if being typed in real-time. Complete with an optional blinking cursor, this animation is perfect for adding a human touch to text reveals, mimicking the feel of live typing or terminal output.

## How It Works

The component progressively reveals characters at a configurable speed, creating the illusion of someone typing:
- **Sequential reveal**: Characters appear left-to-right, one at a time
- **Blinking cursor**: Optional cursor that follows the text as it types
- **Configurable speed**: Control typing pace with characters per second
- **Multiline support**: Handles multiline text with `\n` line breaks

## Parameters

- **text**: Text to type out, supports multiline with \n (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "3xl")
- **font_weight**: Font weight - normal, medium, semibold, bold (default: "medium")
- **text_color**: Text color (uses on_dark color if not specified)
- **cursor_color**: Cursor color (uses text color if not specified)
- **show_cursor**: Whether to show blinking cursor (default: true)
- **type_speed**: Characters per second, 0.1-20.0 (default: 2.0)
- **position**: Screen position - center, top, bottom, left (default: "center")
- **align**: Text alignment - left, center, right (default: "left")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['3xl']`, `font_weights.medium`, `primary_font`, `letter_spacing.normal`
- **Colors:** Uses `text.on_dark` by default
- **Spacing:** Uses `spacing.xs`, `spacing['2xl']`, `spacing['4xl']`

## Typing Speed Guide

- **0.5-1.5**: Very slow, contemplative, emphasizes each word
- **2.0-4.0**: Natural typing pace, readable and engaging (recommended)
- **5.0-8.0**: Fast typing, energetic, skilled typist feel
- **9.0-20.0**: Very fast, machine-like, terminal/CLI aesthetic

## Examples

```python
# Basic typewriter with cursor
{
    "type": "TypewriterText",
    "config": {
        "text": "Hello, World!",
        "font_size": "4xl",
        "type_speed": 3.0,
        "duration": 5.0
    }
}

# Terminal/CLI style output
{
    "type": "TypewriterText",
    "config": {
        "text": "$ npm install success\n> Build complete",
        "font_weight": "normal",
        "text_color": "#00FF00",
        "cursor_color": "#00FF00",
        "type_speed": 8.0,
        "align": "left",
        "position": "left"
    }
}

# Storytelling narrative
{
    "type": "TypewriterText",
    "config": {
        "text": "Once upon a time...",
        "font_size": "2xl",
        "font_weight": "normal",
        "type_speed": 1.5,
        "show_cursor": false,
        "align": "center"
    }
}

# Code demonstration
{
    "type": "TypewriterText",
    "config": {
        "text": "def hello_world():\n    print('Hello!')",
        "font_size": "xl",
        "font_weight": "medium",
        "type_speed": 4.0,
        "position": "left",
        "align": "left"
    }
}

# Dialogue/caption style
{
    "type": "TypewriterText",
    "config": {
        "text": "And that's how it works.",
        "font_size": "3xl",
        "type_speed": 2.5,
        "position": "bottom",
        "align": "center",
        "show_cursor": false
    }
}
```

## Best Practices

1. **Use type_speed 2.0-4.0** for most readable, natural typing feel
2. **Show cursor for live typing feel**, hide it for finished text or captions
3. **Align left for code/terminal**, center for titles/dialogue
4. **Keep text concise** (under 100 characters) for best impact
5. **Green text (#00FF00)** with left alignment creates classic terminal aesthetic
6. **Duration should match text length**: Ensure duration is long enough for all text to type out
7. **Use multiline sparingly** - works best with 1-3 lines of text

## Common Use Cases

- **Code demonstrations** showing code being written live
- **Dialogue and captions** for video narration or subtitles
- **Storytelling sequences** for narrative-driven content
- **Terminal/CLI effects** for technical demonstrations
- **Step-by-step instructions** that appear progressively
- **Programming tutorials** showing code snippets
- **Live chat simulations** for UI demonstrations
- **Documentary-style captions** for informative content

## Visual Feel

- **Human:** Mimics human typing, feels personal and authentic
- **Progressive:** Text appears gradually, building anticipation
- **Focused:** Draws attention to each word as it appears
- **Nostalgic:** Evokes old typewriters and early computers
- **Engaging:** More dynamic than instant text appearance
- **Technical:** Perfect for code, terminal, and CLI aesthetics
