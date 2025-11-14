# TrueFocus

**Category:** Text Animation
**Purpose:** Dramatic text animation with word-by-word focus cycling

## Overview

TrueFocus creates a captivating text animation that cycles through each word in a phrase, highlighting one word at a time while blurring the others. Each focused word is framed by animated corner brackets with a subtle glow effect, drawing the viewer's attention in a controlled, dramatic fashion. Perfect for emphasizing key messages, brand statements, and calls-to-action.

## How It Works

The component splits the input text into individual words and cycles through them sequentially:
- **Word cycling**: Each word becomes the focus for a specified duration
- **Blur effect**: Inactive words are blurred to reduce visual noise
- **Corner brackets**: Animated brackets appear around the focused word
- **Glow effect**: Subtle glow enhances the focused word's prominence
- **Smooth transitions**: Spring-based animations create fluid focus shifts

## Parameters

- **text**: Text to animate (will be split into words) (required)
- **font_size**: Font size - xl, 2xl, 3xl, 4xl (default: "3xl")
- **font_weight**: Font weight - bold, extrabold, black (default: "black")
- **text_color**: Text color (uses theme text color if not specified)
- **frame_color**: Color of corner brackets (uses primary color if not specified)
- **glow_color**: Glow effect color (uses primary color if not specified)
- **blur_amount**: Blur intensity for inactive words in pixels, 0-20 (default: 5.0)
- **word_duration**: Duration each word stays focused in seconds, 0.1-10 (default: 1.0)
- **position**: Vertical position - center, top, bottom (default: "center")
- **duration**: Total duration in seconds (default: 3.0)

## Design Token Integration

- **Typography:** Uses `font_sizes['3xl']`, `font_weights.black`, `primary_font`, `letter_spacing.tight`, `line_heights.tight`
- **Colors:** Uses `text.on_dark` and `primary[0]` by default
- **Spacing:** Uses `spacing.sm`, `spacing.lg`, `spacing.xl`, `spacing.xs`, `spacing['3xl']`, `border_width.thick`, `border_radius.xs`
- **Motion:** Uses `default_spring.config.damping`, `default_spring.config.stiffness`, `default_spring.config.mass`

## Blur Amount Guide

- **0-2**: Minimal blur, words remain mostly legible
- **3-7**: Medium blur, clear distinction between focused and inactive words (recommended)
- **8-12**: Heavy blur, strong emphasis on focused word
- **13-20**: Extreme blur, inactive words nearly invisible (use for maximum drama)

## Word Duration Guide

- **0.3-0.7**: Fast cycling, energetic feel (good for short phrases)
- **0.8-1.5**: Medium pace, balanced readability (recommended for most uses)
- **1.6-3.0**: Slow cycling, contemplative feel (good for important messages)
- **3.0+**: Very slow, cinematic emphasis (use sparingly for maximum impact)

## Examples

```json
{
    "type": "TrueFocus",
    "config": {
        "text": "Innovation Through Excellence",
        "font_size": "3xl",
        "word_duration": 1.5,
        "position": "center",
        "duration": 6.0
    }
}
```

```json
{
    "type": "TrueFocus",
    "config": {
        "text": "Dream Big Create Bold",
        "font_size": "4xl",
        "font_weight": "black",
        "blur_amount": 8.0,
        "word_duration": 1.2,
        "position": "center"
    }
}
```

```json
{
    "type": "TrueFocus",
    "config": {
        "text": "Unlock Your Potential",
        "font_size": "2xl",
        "blur_amount": 4.0,
        "word_duration": 1.0,
        "text_color": "#FFFFFF",
        "frame_color": "#FFD700",
        "glow_color": "#FFD700"
    }
}
```

```json
{
    "type": "TrueFocus",
    "config": {
        "text": "Quality Speed Reliability",
        "font_size": "3xl",
        "font_weight": "extrabold",
        "blur_amount": 10.0,
        "word_duration": 2.0,
        "position": "bottom",
        "frame_color": "#00FFFF"
    }
}
```

```json
{
    "type": "TrueFocus",
    "config": {
        "text": "Transform Connect Inspire",
        "font_size": "4xl",
        "blur_amount": 6.0,
        "word_duration": 0.8,
        "position": "top",
        "text_color": "#F0F0F0",
        "glow_color": "#FF6B6B"
    }
}
```

## Best Practices

1. **Keep text short** (3-6 words) for optimal impact and readability
2. **Match word_duration to phrase length**: Longer phrases need faster cycling, shorter phrases can be slower
3. **Use blur_amount 4-8** for the best balance between emphasis and context
4. **Choose impactful words**: Every word gets focus, so make each one count
5. **Consider color contrast**: Ensure frame_color and glow_color complement your background
6. **Position strategically**: Center for impact, top/bottom for integration with other content
7. **Calculate duration**: Set total duration to approximately (word_count × word_duration) for full cycle

## Common Use Cases

- **Dramatic tagline reveals** for brand introductions
- **Key message emphasis** in product launches
- **Brand statement animations** for marketing videos
- **Call-to-action highlights** in promotional content
- **Mission/vision statements** for corporate presentations
- **Feature highlights** cycling through product benefits
- **Motivational messages** for inspirational content
- **Title sequences** for video intros

## Visual Feel

- **Dramatic:** Strong focus shifts create cinematic impact
- **Purposeful:** Controlled attention guidance feels intentional and designed
- **Modern:** Clean brackets and blur effect feel contemporary
- **Premium:** Glow and smooth animations convey quality and polish
- **Focused:** Clear hierarchy directs viewer attention exactly where you want it
- **Dynamic:** Movement keeps viewers engaged throughout the animation
- **Professional:** Refined execution suitable for corporate and brand content

## Timing Considerations

When planning your animation:
- **Full cycle time** = number of words × word_duration
- **Example**: "Innovation Through Excellence" (3 words) with word_duration 1.5s = 4.5s minimum duration
- **Best practice**: Add 0.5-1.0s padding to allow the animation to settle at the end
- **For looping**: Ensure duration allows at least one complete cycle

## Color Customization Tips

- **Monochromatic**: Use same color for frame and glow, different from text (clean, minimal)
- **Complementary**: Use complementary colors for frame vs text (vibrant, energetic)
- **Brand alignment**: Match frame_color to your primary brand color
- **Subtle emphasis**: Keep glow_color close to frame_color but slightly more saturated
- **High contrast**: White/light text with bright colored frames works well on dark backgrounds
