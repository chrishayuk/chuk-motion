"""CodeDiff component - Code diff viewer with side-by-side or unified view."""

from .schema import METADATA, CodeDiffProps
from .tool import register_tool
from .builder import add_to_composition

__all__ = ["METADATA", "CodeDiffProps", "register_tool", "add_to_composition"]
