#!/usr/bin/env python3
"""
PanelCascade Examples

Demonstrates all 7 cascade types with different grid configurations:
- from_edges: Spatial animation from nearest edge
- from_center: Radial animation from center
- bounce_in: Playful bounce with overshoot
- sequential_left: Left-to-right reading order
- sequential_right: Right-to-left reverse flow
- sequential_top: Top-to-bottom vertical flow
- wave: Diagonal wave pattern

Perfect for Grid, multi-panel layouts, and photo galleries.
"""

# Example 1: From Edges - 3x3 Grid (9 panels)
FROM_EDGES_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "CodeBlock", "config": {"code": f"Panel {i}", "language": "python"}}
            for i in range(1, 10)
        ],
        "cascade_type": "from_edges",
        "stagger_delay": 0.08,
        "duration": 10.0,
    },
}

# Example 2: From Center - 3x3 Grid (radial reveal)
FROM_CENTER_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "DemoBox", "config": {}} for _ in range(9)
        ],
        "cascade_type": "from_center",
        "stagger_delay": 0.1,
        "duration": 10.0,
    },
}

# Example 3: Bounce In - 3x2 Grid (playful energy)
BOUNCE_IN_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {
                "type": "Counter",
                "config": {
                    "start_value": 0,
                    "end_value": (i + 1) * 1000,
                    "suffix": " users",
                    "animation": "count_up",
                },
            }
            for i in range(6)
        ],
        "cascade_type": "bounce_in",
        "stagger_delay": 0.12,
        "duration": 10.0,
    },
}

# Example 4: Sequential Left - 4-panel row (reading order)
SEQUENTIAL_LEFT_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {
                "type": "TitleScene",
                "config": {"text": f"Step {i}", "variant": "minimal"},
            }
            for i in range(1, 5)
        ],
        "cascade_type": "sequential_left",
        "stagger_delay": 0.15,
        "duration": 8.0,
    },
}

# Example 5: Sequential Right - 4-panel row (reverse flow)
SEQUENTIAL_RIGHT_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {
                "type": "CodeBlock",
                "config": {"code": f"Feature {i}", "language": "typescript"},
            }
            for i in range(1, 5)
        ],
        "cascade_type": "sequential_right",
        "stagger_delay": 0.1,
        "duration": 8.0,
    },
}

# Example 6: Sequential Top - 2x3 Grid (vertical flow)
SEQUENTIAL_TOP_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "DemoBox", "config": {}} for _ in range(6)
        ],
        "cascade_type": "sequential_top",
        "stagger_delay": 0.1,
        "duration": 10.0,
    },
}

# Example 7: Wave - 3x3 Grid (diagonal wave)
WAVE_EXAMPLE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {
                "type": "CodeBlock",
                "config": {
                    "code": f"Panel {i}",
                    "language": ["python", "javascript", "rust", "go"][i % 4],
                },
            }
            for i in range(1, 10)
        ],
        "cascade_type": "wave",
        "stagger_delay": 0.08,
        "duration": 12.0,
    },
}

# Real-world use case: Portfolio showcase
PORTFOLIO_SHOWCASE = {
    "type": "PanelCascade",
    "config": {
        "items": [
            {"type": "WebPage", "config": {"url": f"https://example.com/project-{i}"}}
            for i in range(1, 10)
        ],
        "cascade_type": "from_edges",
        "stagger_delay": 0.1,
        "duration": 15.0,
    },
}

# Motion Token Usage Summary
MOTION_TOKENS_USED = """
PanelCascade Motion Token Usage:

Durations:
- fast: Used for quick sequential animations (0.2s)
- medium: Used for balanced cascade timing (0.5s)

Easings:
- ease_out_expo: Snappy deceleration for slides
- ease_out_back: Slight overshoot for bounce_in

Springs:
- bouncy: Used for bounce_in cascade (playful, energetic)

Recommended Stagger Delays:
- 0.05s-0.08s: Fast cascade (sprint tempo)
- 0.08s-0.12s: Balanced cascade (medium tempo)
- 0.12s-0.2s: Deliberate cascade (slow tempo)

Best Practices:
- Use from_edges for professional, spatial reveals
- Use from_center for attention-grabbing radial effects
- Use bounce_in for playful, energetic content
- Use sequential_left for reading-order familiarity
- Use wave for dynamic, flowing reveals
- Match stagger_delay to content tempo/platform
"""

print(MOTION_TOKENS_USED)
