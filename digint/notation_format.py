""" 
notation_format

Defines the `NotationFromat` type, a dataclass that holds key information about notating numbers.
Also provides a pre defined `DEFAULT_FORMAT`, a common notation formating.
"""

from dataclasses import FrozenInstanceError, dataclass, asdict
from string import digits, ascii_uppercase, ascii_lowercase
from .typings import * #pylint:disable=unused-wildcard-import, wildcard-import

@dataclass(init=False)
class NotationFormat(SequenceABC, HashableABC):
    """
    `NotationFormat`

    A dataclass that holds common notation formating information.
    """

    value_symbols:Tuple[str, ...] = tuple()
    undefined_symbol:Optional[str] = None
    positive_symbol:Optional[str] = None
    negative_symbol:Optional[str] = None
    radix_point_symbol:Optional[str] = None
    implicit_positive:bool = False
    implicit_negative:bool = False

    def __init__(self,
                 *value_symbols:str,
                 undefined_symbol:Optional[str] = None,
                 positive_symbol:Optional[str] = None,
                 negative_symbol:Optional[str] = None,
                 radix_point_symbol:Optional[str] = None,
                 implicit_positive:bool = False,
                 implicit_negative:bool = False
                ):
        self.__frozen:bool = False

        self.value_symbols:Tuple[str, ...] = value_symbols
        self.undefined_symbol:Optional[str] = undefined_symbol
        self.negative_symbol:Optional[str] = negative_symbol
        self.positive_symbol:Optional[str] = positive_symbol
        self.radix_point_symbol:Optional[str] = radix_point_symbol
        self.implicit_positive:bool = implicit_positive
        self.implicit_negative:bool = implicit_negative

        self.__frozen = True

    def __setattribute__(self, name: str, value: Any):
        if self.__frozen:
            raise FrozenInstanceError(value, name, self)
        return super().__setattr__(name, value)

    @property
    def unity(self) -> Optional[str]:
        """
        `unity`

        Returns:
            The 'unity' symbol (the symbol associated with the value of 1),
            if defined, from the `value_symbols`. If not defined, returns `None`.
        """
        return self.value_symbols[1] if len(self.value_symbols) >= 1 else None

    @property
    def naught(self) -> Optional[str]:
        """
        `naught`

        Returns:
            The 'naught' symbol (the symbol associated with the value of 0),
            if defined, from the `value_symbols`. If not defined, returns `None`.
        """
        return self.value_symbols[0] if len(self.value_symbols) >= 0 else None

    def get_value(self, symbol:str) -> Optional[int]:
        """
        `get_value`

        Looks for the first instance of the given symbol in the `value_symbols`.

        Arguments:
            `symbol` -- The symbol to look up.

        Returns:
            The index (and therefroe the value) of the symbol in `value_symbols`
            if possible, otherwise returns `None`.
        """
        return None if symbol not in self.value_symbols else self.value_symbols.index(symbol)

    @overload
    def __getitem__(self, index:int) -> str: ...
    @overload
    def __getitem__(self, index:slice) -> Tuple[str, ...]: ...
    def __getitem__(self, index:Union[int, slice]) -> Union[str, Tuple[str, ...]]:
        return self.value_symbols[index]

    def get_digit(self, index:int) -> Optional[str]:
        """
        `get_digit`

        Looks for the symbol for the given value, if possible`.

        Arguments:
            `index` -- The index (the digit's value) to find the symbol of.

        Returns:
            The symbol of the given value from `value_symbols`
            if possible, otherwise returns `None`.
        """
        if index < 0 or index >= len(self.value_symbols):
            return self.undefined_symbol
        else:
            return self.value_symbols[index]

    def __len__(self):
        return len(self.value_symbols)

    def __iter__(self) -> Iterator[str]:
        return iter(self.value_symbols)

    def __reverse__(self) -> Iterator[str]:
        return reversed(self.value_symbols)

    def copy(self, *_) -> 'NotationFormat':
        """
        `copy`

        Returns a deep copy of the object.
        """

        return NotationFormat(*self.value_symbols,
                                        undefined_symbol = self.undefined_symbol,
                                        positive_symbol = self.positive_symbol,
                                        negative_symbol = self.negative_symbol,
                                        radix_point_symbol = self.radix_point_symbol,
                                        implicit_positive = self.implicit_positive,
                                        implicit_negative = self.implicit_negative
                                       )
    __copy__ = copy
    __deepcopy__ = copy

    def __hash__(self) -> int:
        return hash(asdict(self))

DEFAULT_DIGIT_SYMBOLS:LiteralString = digits + ascii_uppercase + ascii_lowercase
DEFAULT_FORMAT:NotationFormat = NotationFormat(
                                                                   *tuple(DEFAULT_DIGIT_SYMBOLS),
                                                                   undefined_symbol = "?",
                                                                   negative_symbol = "-",
                                                                   positive_symbol = "+",
                                                                   radix_point_symbol = ".",
                                                                   implicit_positive = True
                                                                  )
