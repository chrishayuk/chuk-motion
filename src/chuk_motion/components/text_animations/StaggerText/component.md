# StaggerText

**Category:** Text Animation
**Purpose:** Staggered reveal animation where characters or words appear one-by-one with spring physics

## Overview

StaggerText creates a smooth, professional reveal animation where text appears character-by-character or word-by-word with spring-based physics. Perfect for title reveals, bullet points, and impact statements that need a polished, dynamic entrance without being overwhelming.

## How It Works

The component reveals text progressively with configurable timing and animation styles:
- **Stagger units**: Choose between character-by-character or word-by-word reveals
- **Animation styles**: Fade, slide-up, slide-down, or scale animations
- **Spring physics**: Smooth, natural motion using spring-based animation curves
- **Customizable timing**: Control the delay between each unit's appearance

The spring physics create a professional, elastic feel that's more dynamic than linear animations but still refined and polished.

## Parameters

- **text**: Text to animate (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "3xl")
- **font_weight**: Font weight - normal, medium, semibold, bold, extrabold, black (default: "bold")
- **text_color**: Text color (uses on_dark color if not specified)
- **stagger_by**: Stagger by character or word - char, word (default: "char")
- **stagger_delay**: Delay in frames between units, 0.5-10.0 (default: 2.0)
- **animation_type**: Animation style - fade, slide-up, slide-down, scale (default: "fade")
- **position**: Vertical position - center, top, bottom (default: "center")
- **align**: Text alignment - left, center, right (default: "center")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['3xl']`, `font_weights.bold`, `primary_font`, `letter_spacing.wide`, `line_heights.relaxed`
- **Colors:** Uses `text.on_dark` by default
- **Spacing:** Uses `spacing.xl` and `spacing['4xl']`
- **Motion:** Uses `default_spring.damping`, `default_spring.stiffness`, `default_spring.mass` for smooth physics-based animations

## Stagger Delay Guide

- **0.5-1.0 frames**: Very fast, energetic reveals (may feel rushed)
- **1.5-2.5 frames**: Moderate pace, professional and polished (recommended)
- **3.0-5.0 frames**: Slower, dramatic reveals with emphasis
- **6.0-10.0 frames**: Very slow, intentional reveals (use sparingly)

## Animation Type Guide

- **fade**: Classic, subtle reveal - characters fade in from transparent to opaque
- **slide-up**: Dynamic, upward motion - characters slide up into position
- **slide-down**: Gravity-like effect - characters drop down into place
- **scale**: Zoom effect - characters scale up from small to full size

## Examples

```python
# Basic character-by-character fade reveal
{
    "type": "StaggerText",
    "config": {
        "text": "Welcome",
        "font_size": "4xl",
        "stagger_by": "char",
        "animation_type": "fade",
        "duration": 3.0
    }
}

# Word-by-word slide-up for bullet points
{
    "type": "StaggerText",
    "config": {
        "text": "Innovation • Excellence • Impact",
        "stagger_by": "word",
        "animation_type": "slide-up",
        "stagger_delay": 3.0,
        "align": "left",
        "position": "top"
    }
}

# Dramatic scale animation with custom styling
{
    "type": "StaggerText",
    "config": {
        "text": "BREAKTHROUGH",
        "font_size": "4xl",
        "font_weight": "black",
        "animation_type": "scale",
        "stagger_delay": 2.5,
        "text_color": "#FFD700",
        "duration": 4.0
    }
}

# Fast slide-down for energetic reveals
{
    "type": "StaggerText",
    "config": {
        "text": "Let's Go!",
        "animation_type": "slide-down",
        "stagger_delay": 1.5,
        "font_weight": "extrabold",
        "duration": 2.0
    }
}

# Slow, dramatic word-by-word reveal
{
    "type": "StaggerText",
    "config": {
        "text": "The Future Is Now",
        "stagger_by": "word",
        "animation_type": "slide-up",
        "stagger_delay": 4.0,
        "font_size": "3xl",
        "align": "center",
        "duration": 5.0
    }
}
```

## Best Practices

1. **Use stagger_by: char** for short text (1-2 words), **word** for longer phrases (3+ words)
2. **stagger_delay 1.5-2.5** creates the most professional, polished feel
3. **slide-up animation** is most versatile and works for almost any context
4. **Keep text concise** (1-5 words) for maximum impact
5. **Use word stagger for bullet points** to reveal one concept at a time
6. **Pair with bold font weights** (bold, extrabold, black) for emphasis
7. **Duration should accommodate all staggers** - ensure total duration allows all units to fully animate

## Common Use Cases

- **Title reveals** for video intros and section headers
- **Bullet point lists** in presentations and educational content
- **Professional presentations** for corporate and business videos
- **Step-by-step reveals** for tutorials and instructional content
- **Impact statements** for key messages and calls-to-action
- **Award announcements** for ceremonies and recognition videos
- **Product launches** for feature reveals and specifications
- **Video credits** for dynamic, engaging end credits

## Visual Feel

- **Professional:** Spring physics create polished, refined motion
- **Dynamic:** Progressive reveal keeps viewer attention engaged
- **Smooth:** Natural spring curves avoid jarring linear motion
- **Energetic:** Staggered timing creates rhythm and momentum
- **Modern:** Contemporary animation style fits current design trends
- **Controlled:** Predictable, intentional reveals maintain clarity
