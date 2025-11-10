"""DeviceFrame component - Realistic device frames with auto-scaling and glare effects."""

from .builder import add_to_composition
from .schema import METADATA, DeviceFrameProps
from .tool import register_tool

__all__ = ["METADATA", "DeviceFrameProps", "register_tool", "add_to_composition"]
