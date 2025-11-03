# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/motion.py
"""
Motion design tokens for Remotion animations.

Spring configurations, easing curves, and duration presets
for creating smooth, professional animations.
"""

from typing import Any

MOTION_TOKENS: dict[str, Any] = {
    "spring_configs": {
        "gentle": {
            "name": "Gentle",
            "description": "Soft, slow spring motion",
            "config": {"damping": 100, "mass": 1.0, "stiffness": 100, "overshootClamping": False},
            "usage": "Subtle entrances, background elements",
        },
        "smooth": {
            "name": "Smooth",
            "description": "Balanced, natural motion",
            "config": {"damping": 200, "mass": 0.5, "stiffness": 200, "overshootClamping": False},
            "usage": "General purpose animations",
        },
        "bouncy": {
            "name": "Bouncy",
            "description": "Playful spring with overshoot",
            "config": {"damping": 15, "mass": 1.0, "stiffness": 300, "overshootClamping": False},
            "usage": "Attention-grabbing elements, playful UI",
        },
        "snappy": {
            "name": "Snappy",
            "description": "Quick, responsive motion",
            "config": {"damping": 300, "mass": 0.3, "stiffness": 400, "overshootClamping": True},
            "usage": "UI interactions, quick transitions",
        },
        "elastic": {
            "name": "Elastic",
            "description": "Strong elastic overshoot",
            "config": {"damping": 8, "mass": 1.5, "stiffness": 200, "overshootClamping": False},
            "usage": "Emphasis, call-to-action elements",
        },
    },
    "easing_curves": {
        "linear": {
            "name": "Linear",
            "curve": [0.0, 0.0, 1.0, 1.0],
            "css": "linear",
            "description": "Constant speed",
            "usage": "Progress bars, mechanical motion",
        },
        "ease_in": {
            "name": "Ease In",
            "curve": [0.42, 0.0, 1.0, 1.0],
            "css": "ease-in",
            "description": "Starts slow, accelerates",
            "usage": "Exits, disappearing elements",
        },
        "ease_out": {
            "name": "Ease Out",
            "curve": [0.0, 0.0, 0.58, 1.0],
            "css": "ease-out",
            "description": "Starts fast, decelerates",
            "usage": "Entrances, appearing elements",
        },
        "ease_in_out": {
            "name": "Ease In Out",
            "curve": [0.42, 0.0, 0.58, 1.0],
            "css": "ease-in-out",
            "description": "Slow start and end",
            "usage": "Transitions, transformations",
        },
        "ease_in_back": {
            "name": "Ease In Back",
            "curve": [0.6, -0.28, 0.735, 0.045],
            "css": "cubic-bezier(0.6, -0.28, 0.735, 0.045)",
            "description": "Pulls back before moving forward",
            "usage": "Dramatic exits",
        },
        "ease_out_back": {
            "name": "Ease Out Back",
            "curve": [0.175, 0.885, 0.32, 1.275],
            "css": "cubic-bezier(0.175, 0.885, 0.32, 1.275)",
            "description": "Overshoots then settles",
            "usage": "Attention-grabbing entrances",
        },
        "ease_in_out_back": {
            "name": "Ease In Out Back",
            "curve": [0.68, -0.55, 0.265, 1.55],
            "css": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
            "description": "Pulls back and overshoots",
            "usage": "Playful transitions",
        },
        "ease_out_expo": {
            "name": "Ease Out Exponential",
            "curve": [0.16, 1.0, 0.3, 1.0],
            "css": "cubic-bezier(0.16, 1, 0.3, 1)",
            "description": "Sharp deceleration",
            "usage": "Impactful entrances",
        },
    },
    "durations": {
        "instant": {
            "frames": 1,
            "seconds": 0.033,
            "description": "Instant (1 frame at 30fps)",
            "usage": "Cuts, instant changes",
        },
        "ultra_fast": {
            "frames": 5,
            "seconds": 0.167,
            "description": "Ultra fast",
            "usage": "Micro-interactions",
        },
        "fast": {
            "frames": 10,
            "seconds": 0.333,
            "description": "Fast",
            "usage": "Quick UI transitions",
        },
        "normal": {
            "frames": 20,
            "seconds": 0.667,
            "description": "Normal",
            "usage": "Standard animations",
        },
        "moderate": {
            "frames": 30,
            "seconds": 1.0,
            "description": "Moderate (1 second)",
            "usage": "Scene elements",
        },
        "slow": {
            "frames": 45,
            "seconds": 1.5,
            "description": "Slow",
            "usage": "Emphasis, important elements",
        },
        "very_slow": {
            "frames": 60,
            "seconds": 2.0,
            "description": "Very slow (2 seconds)",
            "usage": "Hero animations, cinematic",
        },
        "dramatic": {
            "frames": 90,
            "seconds": 3.0,
            "description": "Dramatic (3 seconds)",
            "usage": "Title reveals, special moments",
        },
    },
    "animation_presets": {
        "fade_in": {
            "name": "Fade In",
            "properties": ["opacity"],
            "from": {"opacity": 0},
            "to": {"opacity": 1},
            "easing": "ease_out",
            "duration": "normal",
        },
        "fade_out": {
            "name": "Fade Out",
            "properties": ["opacity"],
            "from": {"opacity": 1},
            "to": {"opacity": 0},
            "easing": "ease_in",
            "duration": "normal",
        },
        "slide_up": {
            "name": "Slide Up",
            "properties": ["transform"],
            "from": {"translateY": "100px"},
            "to": {"translateY": "0"},
            "easing": "ease_out_back",
            "duration": "normal",
        },
        "slide_down": {
            "name": "Slide Down",
            "properties": ["transform"],
            "from": {"translateY": "-100px"},
            "to": {"translateY": "0"},
            "easing": "ease_out_back",
            "duration": "normal",
        },
        "slide_left": {
            "name": "Slide Left",
            "properties": ["transform"],
            "from": {"translateX": "100px"},
            "to": {"translateX": "0"},
            "easing": "ease_out",
            "duration": "normal",
        },
        "slide_right": {
            "name": "Slide Right",
            "properties": ["transform"],
            "from": {"translateX": "-100px"},
            "to": {"translateX": "0"},
            "easing": "ease_out",
            "duration": "normal",
        },
        "scale_in": {
            "name": "Scale In",
            "properties": ["transform"],
            "from": {"scale": 0},
            "to": {"scale": 1},
            "easing": "ease_out_back",
            "duration": "normal",
        },
        "scale_out": {
            "name": "Scale Out",
            "properties": ["transform"],
            "from": {"scale": 1},
            "to": {"scale": 0},
            "easing": "ease_in",
            "duration": "fast",
        },
        "bounce_in": {
            "name": "Bounce In",
            "spring": "bouncy",
            "properties": ["transform"],
            "from": {"scale": 0},
            "to": {"scale": 1},
            "duration": "moderate",
        },
    },
    "youtube_optimizations": {
        "hook_timing": {
            "description": "First 3 seconds - must grab attention",
            "max_frames": 90,  # 3 seconds at 30fps
            "recommended_animations": ["bounce_in", "slide_up", "fade_in"],
            "tips": [
                "Use fast, attention-grabbing animations",
                "High contrast and bold text",
                "Immediate visual interest",
            ],
        },
        "pattern_interrupt": {
            "description": "Visual changes every 3-5 seconds to maintain attention",
            "interval_frames": [90, 150],  # 3-5 seconds at 30fps
            "recommended_animations": ["slide_left", "slide_right", "scale_in"],
            "tips": [
                "Vary animation direction",
                "Use color changes",
                "Add visual elements regularly",
            ],
        },
        "retention_timing": {
            "description": "Keep viewers engaged throughout",
            "scene_duration": {
                "min_frames": 90,  # 3 seconds minimum
                "max_frames": 300,  # 10 seconds maximum
                "optimal_frames": 150,  # 5 seconds optimal
            },
        },
    },
}
