"""LayoutTransition component for animated scene-to-scene layout transitions."""

# METADATA for auto-discovery
from chuk_motion.components.base import ComponentMetadata

from .builder import add_to_composition
from .tool import register_tool

METADATA = ComponentMetadata(
    name="LayoutTransition",
    description="Animated scene-to-scene layout transitions with motion token integration",
    category="transition",
)

__all__ = ["METADATA", "register_tool", "add_to_composition"]
