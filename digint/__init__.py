"""
     `digint`

     A module focused on providing classes that allow for easy digitwise manipulation
     of integers of any base, just like they were `Collection`s.
"""

from .digint import PositionalBasedIntiger, ExtendedBasedIntiger, digitint
from .notation_format import NotationFormat

__version__ = "1.0.1.0"
__all__ = ["PositionalBasedIntiger", "ExtendedBasedIntiger", "digitint", "NotationFormat"]
