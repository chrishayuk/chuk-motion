#!/usr/bin/env python3
"""
LayoutTransition Examples

Demonstrates all 5 transition types:
- crossfade: Smooth opacity blend
- slide_horizontal: Horizontal slide
- slide_vertical: Vertical slide
- cube_rotate: 3D cube rotation
- parallax_push: Parallax depth effect

Each example shows transitioning between different layout types.
"""

# Example 1: Crossfade between Grid and Container
CROSSFADE_EXAMPLE = {
    "type": "LayoutTransition",
    "config": {
        "first_content": {
            "type": "Grid",
            "config": {
                "layout": "3x3",
                "items": [
                    {"type": "CodeBlock", "config": {"code": f"Item {i}"}}
                    for i in range(1, 10)
                ],
            },
        },
        "second_content": {
            "type": "Container",
            "config": {
                "position": "center",
                "content": {
                    "type": "TitleScene",
                    "config": {"text": "Crossfade Complete", "variant": "bold"},
                },
            },
        },
        "transition_type": "crossfade",
        "transition_start": 2.0,
        "transition_duration": 1.0,
        "duration": 5.0,
    },
}

# Example 2: Slide Horizontal - Chapter transitions
SLIDE_HORIZONTAL_EXAMPLE = {
    "type": "LayoutTransition",
    "config": {
        "first_content": {
            "type": "TitleScene",
            "config": {"text": "Chapter 1: Introduction", "variant": "gradient"},
        },
        "second_content": {
            "type": "TitleScene",
            "config": {"text": "Chapter 2: Deep Dive", "variant": "neon"},
        },
        "transition_type": "slide_horizontal",
        "transition_start": 2.5,
        "transition_duration": 0.8,
        "duration": 6.0,
    },
}

# Example 3: Slide Vertical - Vertical content flow
SLIDE_VERTICAL_EXAMPLE = {
    "type": "LayoutTransition",
    "config": {
        "first_content": {
            "type": "Vertical",
            "config": {
                "content": {"type": "CodeBlock", "config": {"code": "Vertical Layout 1"}},
                "caption": "Swipe up to continue",
            },
        },
        "second_content": {
            "type": "Vertical",
            "config": {
                "content": {"type": "CodeBlock", "config": {"code": "Vertical Layout 2"}},
                "caption": "Next section",
            },
        },
        "transition_type": "slide_vertical",
        "transition_start": 2.0,
        "transition_duration": 1.0,
        "duration": 5.0,
    },
}

# Example 4: Cube Rotate - Dramatic 3D transition
CUBE_ROTATE_EXAMPLE = {
    "type": "LayoutTransition",
    "config": {
        "first_content": {
            "type": "ThreeColumnLayout",
            "config": {
                "left": {"type": "CodeBlock", "config": {"code": "Left"}},
                "center": {"type": "CodeBlock", "config": {"code": "Center"}},
                "right": {"type": "CodeBlock", "config": {"code": "Right"}},
            },
        },
        "second_content": {
            "type": "SplitScreen",
            "config": {
                "left": {"type": "CodeBlock", "config": {"code": "Split Left"}},
                "right": {"type": "CodeBlock", "config": {"code": "Split Right"}},
                "split_position": 50,
            },
        },
        "transition_type": "cube_rotate",
        "transition_start": 2.0,
        "transition_duration": 1.5,
        "duration": 6.0,
    },
}

# Example 5: Parallax Push - Depth and layers
PARALLAX_PUSH_EXAMPLE = {
    "type": "LayoutTransition",
    "config": {
        "first_content": {
            "type": "Grid",
            "config": {
                "layout": "2x2",
                "items": [
                    {"type": "DemoBox", "config": {}},
                    {"type": "DemoBox", "config": {}},
                    {"type": "DemoBox", "config": {}},
                    {"type": "DemoBox", "config": {}},
                ],
            },
        },
        "second_content": {
            "type": "Mosaic",
            "config": {
                "items": [
                    {"type": "CodeBlock", "config": {"code": "Mosaic 1"}},
                    {"type": "CodeBlock", "config": {"code": "Mosaic 2"}},
                    {"type": "CodeBlock", "config": {"code": "Mosaic 3"}},
                ],
            },
        },
        "transition_type": "parallax_push",
        "transition_start": 2.0,
        "transition_duration": 1.2,
        "duration": 5.5,
    },
}

# Motion Token Usage Summary
MOTION_TOKENS_USED = """
LayoutTransition Motion Token Usage:

Durations:
- medium: Used for general transition timing (0.5s)
- slow: Used for more deliberate transitions (0.7s)

Easings:
- ease_out_expo: Fast start, smooth deceleration (slides)
- ease_in_out_quart: Strong S-curve (cube rotate)
- ease_out_quint: Elegant deceleration (crossfade, parallax)

Best Practices:
- Keep transition_duration between 0.5s-1.5s
- Use crossfade for subtle, professional transitions
- Use slide_horizontal for sequential content
- Use cube_rotate sparingly for dramatic moments
- Use parallax_push for depth and layering
"""

print(MOTION_TOKENS_USED)
