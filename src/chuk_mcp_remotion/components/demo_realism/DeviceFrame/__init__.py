"""DeviceFrame component - Realistic device frames with auto-scaling and glare effects."""

from .schema import METADATA, DeviceFrameProps
from .tool import register_tool
from .builder import add_to_composition

__all__ = ["METADATA", "DeviceFrameProps", "register_tool", "add_to_composition"]
