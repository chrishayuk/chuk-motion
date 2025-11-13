"""LayoutTransition component for animated scene-to-scene layout transitions."""

from .tool import register_tool

# METADATA for auto-discovery
from chuk_motion.components.base import ComponentMetadata

METADATA = ComponentMetadata(
    name="LayoutTransition",
    description="Animated scene-to-scene layout transitions with motion token integration",
    category="transition",
)

__all__ = ["METADATA", "register_tool"]
