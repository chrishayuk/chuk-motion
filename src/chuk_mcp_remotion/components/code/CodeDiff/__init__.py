"""CodeDiff component - Code diff viewer with side-by-side or unified view."""

from .builder import add_to_composition
from .schema import METADATA, CodeDiffProps
from .tool import register_tool

__all__ = ["METADATA", "CodeDiffProps", "register_tool", "add_to_composition"]
