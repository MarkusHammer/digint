"""
     .. include:: ../README.md

     .. include:: ../SECURITY.md

     .. include:: ../LICENCE
"""

from .digint import PositionalBasedIntiger, ExtendedBasedIntiger, digitint
from .notation_format import NotationFormat

__version__ = "1.0.3.0"
__all__ = ["PositionalBasedIntiger", "ExtendedBasedIntiger", "digitint", "NotationFormat"]
