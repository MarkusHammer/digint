""" 
`typings`

Hold the imported types used for type checking and inheriting
"""

# pylint: disable=unused-import, ungrouped-imports, deprecated-class
try:
    from typing import SupportsInt
except ImportError:
    from typing_extensions import SupportsInt

try:
    from typing import SupportsFloat
except ImportError:
    from typing_extensions import SupportsFloat

try:
    from typing import SupportsAbs
except ImportError:
    from typing_extensions import SupportsAbs

try:
    from typing import SupportsBytes
except ImportError:
    from typing_extensions import SupportsBytes

try:
    from typing import SupportsComplex
except ImportError:
    from typing_extensions import SupportsComplex

try:
    from typing import SupportsIndex
except ImportError:
    from typing_extensions import SupportsIndex

try:
    from typing import SupportsRound
except ImportError:
    from typing_extensions import SupportsRound

try:
    from typing import Callable
except ImportError:
    from typing_extensions import Callable

try:
    from typing import override #type:ignore
except ImportError:
    try:
        from typing_extensions import override #type:ignore
    except ImportError:
        def override(func:Callable) -> Callable: #pylint:disable=missing-function-docstring
            return func

try:
    from typing import Any
except ImportError:
    from typing_extensions import Any

try:
    from typing import Type
except ImportError:
    from typing_extensions import Type

try:
    from typing import overload
except ImportError:
    from typing_extensions import overload

try:
    from typing import LiteralString
except ImportError:
    from typing_extensions import LiteralString

try:
    from typing import Union
except ImportError:
    from typing_extensions import Union

try:
    from typing import Sized
except ImportError:
    from typing_extensions import Sized

try:
    from typing import Optional
except ImportError:
    from typing_extensions import Optional

try:
    from typing import Tuple
except ImportError:
    from typing_extensions import Tuple

try:
    from typing import List
except ImportError:
    from typing_extensions import List

try:
    from typing import Sequence
except ImportError:
    from typing_extensions import Sequence

from collections.abc import Sequence as SequenceABC

try:
    from typing import Hashable
except ImportError:
    from typing_extensions import Hashable

from collections.abc import Hashable as HashableABC

try:
    from typing import Iterable
except ImportError:
    from typing_extensions import Iterable

try:
    from typing import Iterator
except ImportError:
    from typing_extensions import Iterator

from collections.abc import MutableSequence as MutableSequenceABC

try:
    from typing import MutableSequence
except ImportError:
    from typing_extensions import MutableSequence

try:
    from typing import cast
except ImportError:
    from typing_extensions import cast
