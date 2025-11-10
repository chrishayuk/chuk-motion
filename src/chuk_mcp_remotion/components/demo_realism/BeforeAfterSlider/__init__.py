"""BeforeAfterSlider component - Interactive before/after comparison slider."""

from .builder import add_to_composition
from .schema import METADATA, BeforeAfterSliderProps
from .tool import register_tool

__all__ = ["METADATA", "BeforeAfterSliderProps", "register_tool", "add_to_composition"]
