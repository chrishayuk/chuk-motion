"""BeforeAfterSlider component - Interactive before/after comparison slider."""

from .schema import METADATA, BeforeAfterSliderProps
from .tool import register_tool
from .builder import add_to_composition

__all__ = ["METADATA", "BeforeAfterSliderProps", "register_tool", "add_to_composition"]
