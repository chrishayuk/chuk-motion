# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/colors.py
"""
Color tokens for Remotion video design system.

Organized by theme, optimized for video content and YouTube.
All colors are tested for readability and visual impact on screen.
"""

from typing import Any

COLOR_TOKENS: dict[str, Any] = {
    "tech": {
        "name": "Tech",
        "description": "Modern tech aesthetic with blue/cyan palette",
        "primary": ["#0066FF", "#0052CC", "#003D99"],  # Blue scale
        "accent": ["#00D9FF", "#00B8D4", "#0097A7"],  # Cyan scale
        "gradient": "linear-gradient(135deg, #0066FF 0%, #00D9FF 100%)",
        "background": {"dark": "#0A0E1A", "light": "#F5F7FA", "glass": "rgba(10, 14, 26, 0.85)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#1A1A1A", "muted": "#8B92A4"},
        "semantic": {
            "success": "#00C853",
            "warning": "#FFB300",
            "error": "#FF3D00",
            "info": "#00B8D4",
        },
    },
    "finance": {
        "name": "Finance",
        "description": "Professional finance theme with green/gold",
        "primary": ["#00C853", "#00A843", "#008833"],  # Green scale
        "accent": ["#FFD600", "#FFAB00", "#FF6F00"],  # Gold scale
        "gradient": "linear-gradient(135deg, #00C853 0%, #FFD600 100%)",
        "background": {"dark": "#0D1B0D", "light": "#F8FAF8", "glass": "rgba(13, 27, 13, 0.85)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#1A1A1A", "muted": "#7A8A7A"},
        "semantic": {
            "success": "#00C853",
            "warning": "#FFB300",
            "error": "#D32F2F",
            "info": "#1976D2",
        },
    },
    "education": {
        "name": "Education",
        "description": "Friendly education theme with purple/orange",
        "primary": ["#7C4DFF", "#651FFF", "#6200EA"],  # Purple scale
        "accent": ["#FF6E40", "#FF5722", "#F4511E"],  # Orange scale
        "gradient": "linear-gradient(135deg, #7C4DFF 0%, #FF6E40 100%)",
        "background": {"dark": "#1A0F2E", "light": "#FAF7FC", "glass": "rgba(26, 15, 46, 0.85)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#1A1A1A", "muted": "#9B8AA9"},
        "semantic": {
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336",
            "info": "#7C4DFF",
        },
    },
    "lifestyle": {
        "name": "Lifestyle",
        "description": "Warm lifestyle theme with coral/pink",
        "primary": ["#FF6B9D", "#E91E63", "#C2185B"],  # Pink scale
        "accent": ["#FFB74D", "#FFA726", "#FF9800"],  # Coral/orange scale
        "gradient": "linear-gradient(135deg, #FF6B9D 0%, #FFB74D 100%)",
        "background": {"dark": "#2E1A26", "light": "#FFF9FA", "glass": "rgba(46, 26, 38, 0.85)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#2E1A26", "muted": "#B39AA6"},
        "semantic": {
            "success": "#66BB6A",
            "warning": "#FFA726",
            "error": "#EF5350",
            "info": "#29B6F6",
        },
    },
    "gaming": {
        "name": "Gaming",
        "description": "High-energy gaming theme with neon accents",
        "primary": ["#00E676", "#00C853", "#00BFA5"],  # Neon green scale
        "accent": ["#E040FB", "#D500F9", "#AA00FF"],  # Neon purple scale
        "gradient": "linear-gradient(135deg, #00E676 0%, #E040FB 100%)",
        "background": {"dark": "#0F0F1A", "light": "#F0F0F5", "glass": "rgba(15, 15, 26, 0.9)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#1A1A1A", "muted": "#8B8BA0"},
        "semantic": {
            "success": "#00E676",
            "warning": "#FFD740",
            "error": "#FF1744",
            "info": "#00E5FF",
        },
    },
    "minimal": {
        "name": "Minimal",
        "description": "Clean minimal theme with monochrome palette",
        "primary": ["#212121", "#424242", "#616161"],  # Gray scale
        "accent": ["#FFFFFF", "#F5F5F5", "#EEEEEE"],  # Light scale
        "gradient": "linear-gradient(135deg, #212121 0%, #616161 100%)",
        "background": {"dark": "#000000", "light": "#FFFFFF", "glass": "rgba(0, 0, 0, 0.8)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#000000", "muted": "#757575"},
        "semantic": {
            "success": "#4CAF50",
            "warning": "#FFC107",
            "error": "#F44336",
            "info": "#2196F3",
        },
    },
    "business": {
        "name": "Business",
        "description": "Professional business theme with navy/teal",
        "primary": ["#1565C0", "#0D47A1", "#01579B"],  # Navy scale
        "accent": ["#00ACC1", "#0097A7", "#00838F"],  # Teal scale
        "gradient": "linear-gradient(135deg, #1565C0 0%, #00ACC1 100%)",
        "background": {"dark": "#0A1929", "light": "#F5F8FA", "glass": "rgba(10, 25, 41, 0.85)"},
        "text": {"on_dark": "#FFFFFF", "on_light": "#0A1929", "muted": "#718096"},
        "semantic": {
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
            "info": "#0EA5E9",
        },
    },
}
