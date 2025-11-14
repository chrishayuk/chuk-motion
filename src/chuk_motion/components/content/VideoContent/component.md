# VideoContent

**Category:** Content
**Purpose:** Video player component for playing video files in compositions

## Overview

VideoContent provides a flexible video player that can display both local video files (via staticFile) and remote URLs. It supports volume control, playback speed adjustment, looping, and various fit modes for responsive video display. Perfect for adding video backgrounds, product demos, tutorials, or any video content to your layouts.

## How It Works

The component uses Remotion's Video component with additional features:
- **Static File Resolution**: Automatically resolves local video files using staticFile()
- **Fit Modes**: Control how video fills the container (contain, cover, fill)
- **Playback Control**: Adjust volume, speed, and starting frame
- **Looping**: Optionally loop videos continuously
- **Frame-based Timing**: Precise control over when video appears and for how long

## Parameters

- **src**: Video source URL or path to static file (required)
  - For local files: "video.mp4", "media/intro.mp4"
  - For remote URLs: "https://example.com/video.mp4"
- **volume**: Video volume from 0.0 (silent) to 1.0 (full volume) (default: 1.0)
- **playback_rate**: Playback speed multiplier (default: 1.0)
  - 0.5 = half speed (slow motion)
  - 1.0 = normal speed
  - 2.0 = double speed (fast forward)
- **fit**: How video fits in container (default: "cover")
  - "contain" = fit entire video, may show letterboxing
  - "cover" = fill container, may crop video
  - "fill" = stretch to fill, may distort aspect ratio
- **muted**: Whether video should be muted (default: false)
- **start_from**: Frame offset to start video playback from (default: 0)
- **loop**: Whether to loop the video continuously (default: false)
- **start_time**: When to show the video (seconds) (required)
- **duration**: Total duration to show (seconds) (default: 5.0)

## Design Token Integration

- **Colors:** Uses `background.dark` for container background
- **Layout:** Full width/height with responsive overflow handling

## Fit Mode Guide

- **contain**: Best for videos where you want to see the entire frame (presentations, tutorials)
- **cover**: Best for video backgrounds where you want to fill the space (hero sections, backgrounds)
- **fill**: Best when you need exact container fill and don't mind distortion (rare use case)

## Examples

```python
# Basic video from local file
{
    "type": "VideoContent",
    "config": {
        "src": "product_demo.mp4",
        "start_time": 0.0,
        "duration": 10.0
    }
}

# Video background with cover fit
{
    "type": "VideoContent",
    "config": {
        "src": "background.mp4",
        "fit": "cover",
        "muted": True,
        "loop": True,
        "start_time": 0.0,
        "duration": 30.0
    }
}

# Slow motion video clip
{
    "type": "VideoContent",
    "config": {
        "src": "action_scene.mp4",
        "playback_rate": 0.5,
        "volume": 0.8,
        "start_from": 120,
        "start_time": 5.0,
        "duration": 8.0
    }
}

# Tutorial video with full audio
{
    "type": "VideoContent",
    "config": {
        "src": "https://example.com/tutorial.mp4",
        "fit": "contain",
        "volume": 1.0,
        "start_time": 0.0,
        "duration": 60.0
    }
}

# Looping ambient video
{
    "type": "VideoContent",
    "config": {
        "src": "ambient_loop.mp4",
        "loop": True,
        "muted": True,
        "playback_rate": 0.7,
        "start_time": 0.0,
        "duration": 120.0
    }
}
```

## Best Practices

1. **File formats**: Use MP4 (H.264) for best compatibility across browsers
2. **Local files**: Place videos in `public/` directory and reference by name only
3. **Video size**: Keep video files optimized for web (compress with HandBrake, FFmpeg, etc.)
4. **Muted by default**: For autoplay backgrounds, always set `muted: True`
5. **Loop carefully**: Only loop short, seamless videos to avoid jarring transitions
6. **Playback rate**: Keep between 0.5-2.0 for natural-looking results
7. **start_from**: Use to skip intros or jump to specific sections

## Common Use Cases

- **Video backgrounds** for layouts and hero sections
- **Product demonstrations** and feature showcases
- **Tutorial content** with step-by-step instructions
- **Marketing video clips** for social media content
- **Presentation videos** embedded in slides
- **Ambient/looping visuals** for aesthetic appeal
- **Testimonial videos** from customers or users
- **Slow motion highlights** for action sequences

## Visual Feel

- **Immersive:** Full-screen video fills the space
- **Professional:** Smooth playback with precise timing control
- **Flexible:** Adapts to any container size with fit modes
- **Responsive:** Maintains aspect ratio while filling space
- **Dynamic:** Motion adds energy to static layouts

## Technical Notes

- Videos start playing based on `start_frame` timing
- When nested in layouts with `durationInFrames=0`, inherits parent timing
- Static files are resolved using Remotion's `staticFile()` helper
- Remote URLs load directly without static file resolution
- `start_from` allows precise frame-level control over video start point
