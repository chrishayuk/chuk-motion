# ImageContent

**Category:** Content
**Purpose:** Image display component for showing images in compositions

## Overview

ImageContent provides a flexible image display that can show both local image files (via staticFile) and remote URLs. It supports opacity control, border radius, and various fit modes for responsive image display. Perfect for adding image backgrounds, product photos, logos, or any visual content to your layouts.

## How It Works

The component uses Remotion's Img component with additional features:
- **Static File Resolution**: Automatically resolves local image files using staticFile()
- **Fit Modes**: Control how image fills the container (contain, cover, fill)
- **Opacity Control**: Adjust image transparency from fully transparent to fully opaque
- **Border Radius**: Add rounded corners to images
- **Frame-based Timing**: Precise control over when image appears and for how long

## Parameters

- **src**: Image source URL or path to static file (required)
  - For local files: "image.png", "media/logo.png"
  - For remote URLs: "https://example.com/image.jpg"
- **fit**: How image fits in container (default: "cover")
  - "contain" = fit entire image, may show letterboxing
  - "cover" = fill container, may crop image
  - "fill" = stretch to fill, may distort aspect ratio
- **opacity**: Image opacity from 0.0 (transparent) to 1.0 (opaque) (default: 1.0)
- **border_radius**: Border radius in pixels for rounded corners (default: 0)
- **start_time**: When to show the image (seconds) (required)
- **duration**: Total duration to show (seconds) (default: 5.0)

## Design Token Integration

- **Colors:** Uses `background.dark` for container background
- **Layout:** Full width/height with responsive overflow handling

## Fit Mode Guide

- **contain**: Best for images where you want to see the entire frame (logos, product photos)
- **cover**: Best for image backgrounds where you want to fill the space (hero sections, backgrounds)
- **fill**: Best when you need exact container fill and don't mind distortion (rare use case)

## Examples

```python
# Basic image from local file
{
    "type": "ImageContent",
    "config": {
        "src": "product_photo.jpg",
        "start_time": 0.0,
        "duration": 10.0
    }
}

# Image background with cover fit
{
    "type": "ImageContent",
    "config": {
        "src": "background.jpg",
        "fit": "cover",
        "start_time": 0.0,
        "duration": 30.0
    }
}

# Semi-transparent overlay image
{
    "type": "ImageContent",
    "config": {
        "src": "watermark.png",
        "opacity": 0.3,
        "fit": "contain",
        "start_time": 0.0,
        "duration": 20.0
    }
}

# Rounded image
{
    "type": "ImageContent",
    "config": {
        "src": "profile.jpg",
        "border_radius": 20,
        "fit": "cover",
        "start_time": 5.0,
        "duration": 8.0
    }
}

# Logo display
{
    "type": "ImageContent",
    "config": {
        "src": "https://example.com/logo.png",
        "fit": "contain",
        "start_time": 0.0,
        "duration": 60.0
    }
}
```

## Best Practices

1. **File formats**: Use PNG for images with transparency, JPG for photos, SVG for logos/icons
2. **Local files**: Place images in `public/` directory and reference by name only
3. **Image size**: Optimize images for web (use appropriate resolution and compression)
4. **Transparency**: Use opacity for overlays and watermarks
5. **Border radius**: Use sparingly for design consistency
6. **Fit mode**: Choose based on whether content or aesthetics are more important
7. **Background images**: Use cover fit and ensure important content isn't near edges

## Common Use Cases

- **Image backgrounds** for layouts and hero sections
- **Product photos** and screenshots
- **Logo and branding** displays
- **Marketing visual content** for social media
- **Presentation images** and slides
- **Profile pictures** and avatars (with border radius)
- **Watermarks and overlays** (with opacity)
- **Before/after images** in comparisons

## Visual Feel

- **Clean:** Sharp images with precise rendering
- **Flexible:** Adapts to any container size with fit modes
- **Professional:** Maintains aspect ratio and quality
- **Responsive:** Scales appropriately to container
- **Customizable:** Opacity and border radius for creative control

## Technical Notes

- Images start appearing based on `start_frame` timing
- When nested in layouts with `durationInFrames=0`, inherits parent timing
- Static files are resolved using Remotion's `staticFile()` helper
- Remote URLs load directly without static file resolution
- Border radius is applied to the image element itself
- Opacity affects the entire image uniformly
