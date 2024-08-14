"""
digint

Holds the main digitwise intiger classes `digint` module.
"""

from sys import version_info

from .typings import * #pylint:disable=unused-wildcard-import, wildcard-import
from .userint import ExtendedUserInt
from .tools import absindex, slice_to_range, iter_to_slices
from .notation_format import NotationFormat, DEFAULT_FORMAT
from .errors import NotationError, BaseInvalidOpperationError, BaseValueError

__POSITIONAL_BASED_INT_BASES:List[Type] = [ExtendedUserInt]
if version_info.minor >= 10:
    __POSITIONAL_BASED_INT_BASES.append(MutableSequenceABC)
    __POSITIONAL_BASED_INT_BASES.append(SupportsBytes)

class PositionalBasedIntiger(*tuple(__POSITIONAL_BASED_INT_BASES)):
    """
    `PositionalBasedIntiger`
    
    A mutable sequence type of intiger that has a explicitly set base,
    allowing for specific digit values to be get and set.
    
    Supports any initger base starting at binary (base 2).
    These bases are presumed to be in the traditional place value format of
    `value == d[x] * (base ** x)` where `value` is the value the digit holds in the intiger,
    `d` is a single digit value form a sequence of digits,
    `base` is the base,
    and `x` is the specific index in question of the intiger.
    
    Supports many operators and methods that built in integers suport,
    casting the type back into a default intiger type when possible.
    
    Also supports customizable notation formats with the optional `notation_format` attribute.
    """

    def __init__(self,
                 value:Union[int, str] = 0,
                 base:int = 10,
                 *,
                 notation_format:Optional[NotationFormat] = DEFAULT_FORMAT
                ):

        super().__init__(0)
        self.__base:int = 2

        self.x = int(value, base) if isinstance(value, str) else value
        self.base = base
        self.notation_format:Optional[NotationFormat] = notation_format

    def copy(self,
             value:Optional[Union[int, str]] = None,
             base:Optional[int] = None,
             notation_format_override:Optional[NotationFormat] = None
            ) -> 'PositionalBasedIntiger':
        """
        `copy`
        
        Creates a shallow copy of this object.

        Keyword Arguments:
            value -- When not `None`, will overrides the `x` value of the copy.
            base -- When not `None`, will overrides the `base` of the copy.
            notation_format_override -- When not `None`,
                will overrides the `notation_format` of the copy.

        Returns:
            The copy of the object.
        """
        if notation_format_override is not None:
            notation_format_override = self.notation_format
        return PositionalBasedIntiger(value if value is not None else self.x,
                                      base if base is not None else self.base,
                                      notation_format = notation_format_override
                                     )
    __copy__ = copy
    def __deepcopy__(self, _ = None) -> 'PositionalBasedIntiger':
        return self.copy(None,
                         None,
                         None if self.notation_format is None else self.notation_format.copy()
                        )

    @property
    def base(self) -> int:
        """
        `base`
        
        The base of the intiger.
        Must be at or above 2, as this class does not support any non-standard bases.
        """
        return self.__base
    @base.setter
    def base(self, value:int):
        if value < 2:
            raise ValueError("Invalid base", value)
        self.__base = value

    @property
    def radix(self) -> int:
        """
        radix

        Returns:
            _description_
        """
        return abs(self.base)

    def _ensure_notated(self, value:Union[int,str]) -> str:
        if self.notation_format is None:
            raise NotationError("Cannot reference a symbol without a notation format")

        if isinstance(value, str):
            return value
        else:
            dig = self.notation_format.get_digit(value)
            if dig is None:
                raise NotationError(f"Could not find digit for {value} in current notation format")
            return dig

    def _ensure_unnotated(self, value:Union[int,str]) -> int:
        if self.notation_format is None:
            raise NotationError("Cannot reference a symbol without a notation format")

        if isinstance(value, int):
            return value

        v = self.notation_format.get_value(value)
        if v is None:
            raise NotationError(f"Given symbol '{value}' not found in current notation format")
        return v

    def _get_single_digit(self, index:int) -> int:
        index = absindex(index, self.digit_length())
        if self.base == 2:
            return (abs(self.x) >> index) % (0b1 << 1)
        else:
            return (abs(self.x) // (self.base ** index)) % self.base

    #this pops the digit in the units spot,
    #effectively shifts left once while returning units shifted out
    #slightly faster than the arbitrary pop method
    def _pop_first(self) -> int:
        dm = divmod(self.x, self.base)
        self.x = dm[0]
        return dm[1]

    #this pushes a value into the units place
    #effectively shifts right while appending a new value to the units
    #slightly faster than the arbitrary insert method
    def _prepend(self, value:Union[int,str]):
        value = self._ensure_unnotated(value)

        if self.base == 0:
            raise BaseInvalidOpperationError("Base 0 digits cannot be pushed")

        if value < 0 or value >= self.base:
            raise ValueError("Digit value out of bounds of base")

        if self.sign == -1:
            value *= -1

        self.x = (self.x*self.base) + value

    # effectively, this returns a continuous sequence
    # form the intiger with its place value still intact
    def _mask_value_continuous(self, dindex:int, count:int = 1) -> int:
        if count <= 0:
            raise IndexError("The length of a continuous mask must be at least 1")

        dindex = absindex(dindex, self.digit_length())

        if self.base == 2: #binary optimisable
            return abs(self.x) & (((0b1 << (count - 1)) - 1) << dindex)
        else:
            pv1 = self.base ** dindex
            pv2 = pv1 * (self.base ** count) # aka ```self.base ** (dindex + count)```
            return (abs(self.x) % pv2) - (abs(self.x) % pv1)

    def iter_digits(self, at_least:int = 0) -> Iterator[int]:
        """
        `iter_digits`
        Returns an iterable that iterates through the digit values of the integer,
        starting at the units spot.
        Will iterate 0 when all other digits are already iterated.

        Keyword Arguments:
            `at_least` -- Ensures that at least the given amount of digits are iterated, if above 1.

        Returns:
            An iterator that returns the digit values, starting at the units spot.

        Yields:
            The digits of the intiger, starting at the units spot.
        """
        indexes = range(max(self.digit_length(), at_least))
        return (self._get_single_digit(i) for i in indexes)
    __iter__ = iter_digits

    def reversed_iter_digits(self, at_least:int = 0) -> Iterator[int]:
        """
        `reversed_iter_digits`
        Returns an iterable that iterates through the digit values of the integer,
        ending at the units spot.
        Will iterate 0 when all other digits are already iterated.

        Keyword Arguments:
            `at_least` -- Ensures that at least the given amount of digits are iterated, if above 1.

        Returns:
            An iterator that returns the digit values, ending at the units spot.

        Yields:
            The digits of the intiger, ending at the units spot.
        """
        indexes = range(max(self.digit_length(), at_least)-1, -1, -1)
        return (self._get_single_digit(i) for i in indexes)
    __reverse__ = reversed_iter_digits

    def __bytes__(self):
        return bytes(self.iter_digits(0))

    def iter_symbols(self, at_least:int = 1) -> Iterator[str]:
        """
        `iter_symbols`
        
        Iterate the digit symbols starting at the units spot.
        When intending to use iteration for notation,
        it's suggested to use `reversed_iter_symbols` to avoid odering errors.

        Keyword Arguments:
            `at_least` -- ensures that at least the given amount of symbols are returned.
                Defaults to 1.

        Returns:
            An iterator of symbols.

        Yields:
            Digit symdols, starting at the units spot.
        """
        return (self._ensure_notated(x) for x in self.iter_digits(at_least))

    def reversed_iter_symbols(self, at_least:int = 1) -> Iterator[str]:
        """
        `reversed_iter_symbols`
        
        Iterate the digit symbols ending at the units spot.
        Intending to be used for notation purposes, as the ordering for string notation is correct.

        Keyword Arguments:
            `at_least` -- ensures that at least the given amount of symbols are returned.
                Defaults to 1.

        Returns:
            An iterator of symbols.

        Yields:
            Digit symdols, ending at the units spot.
        """
        return (self._ensure_notated(x) for x in self.reversed_iter_digits(at_least))

    def notate(self, notation_format:Optional[NotationFormat] = None) -> str:
        """
        `notate`
        Notates the intiger, using the given notation format if possible,
        or the `notation_format` set in the object's attributes if the paramater is not set. 

        Keyword Arguments:
            notation_format -- A notation format to use
                over the one set in `self.notation_format`, if not `None`.

        Raises:
            NotationError: Raised when both the argument and attribute `notation_format` are `None`;
                or when other errors are raised during notation.

        Returns:
            The final notation of the intiger.
        """
        if notation_format is None:
            notation_format = self.notation_format

        if notation_format is None:
            raise NotationError("No format set, cannot notate")

        relevant_sign = ""
        if self.x < 0 and not notation_format.implicit_negative:
            if notation_format.negative_symbol is None:
                raise NotationError("Explicit negative values require a negative symbol")
            else:
                relevant_sign = notation_format.negative_symbol
        elif self.x > 0 and not notation_format.implicit_positive:
            if notation_format.positive_symbol is None:
                raise NotationError("Explicit positive values require a positive symbol")
            else:
                relevant_sign = notation_format.positive_symbol

        return relevant_sign + "".join(self.reversed_iter_symbols())
    __str__ = notate
    __repr__ = notate

    @overload
    def get_digit(self, index:int) -> int: ...
    @overload
    def get_digit(self, index:Union[slice,range,Iterable[int]]) -> List[int]: ...
    def get_digit(self, index:Union[int,slice,range,Iterable[int]]) -> Union[int,List[int]]:
        """
        `get_digit`
        
        Gets the specific digit's (or digits's) value at the specific index (or indexes).

        Arguments:
            `index` -- The index (or indexes) in question.

        Returns:
            The value (or values, contained in a `List`) found at the index.
        """
        if isinstance(index, int):
            return self._get_single_digit(index)

        if isinstance(index, slice):
            index = slice_to_range(index, self.digit_length())

        return list(self._get_single_digit(absindex(i, self.digit_length())) for i in index)
    __getitem__ = get_digit

    @overload
    def set_digit(self, index:int, value:Union[int,str]): ...
    @overload
    def set_digit(self, index:Union[slice,range,Iterable[int]], value:Iterable[Union[int,str]]): ...
    def set_digit(self,
                  index:Union[int,slice,range,Iterable[int]],
                  value:Union[int,str,Iterable[Union[int,str]]]
                 ):
        """
        `set_digit`

        Sets the digit (or digits) at the given index (or indexes) to the given value (or values).
        With multiple indexes and,
        there must be a matching quantity of values to set at those indexes.

        Arguments:
            `index` -- The index (or indexes) to set.
            `value` -- The value (or values) to set the index (or indexes) to.

        Raises:
            `ValueError`: Raised when the given value is out of bounds of the current `base`.
        """
        if isinstance(value, Iterable):
            value = (self._ensure_unnotated(v) for v in value)
        else:
            value = self._ensure_unnotated(value)

        if isinstance(value, int):
            value = [value]
        else:
            value = cast(List[int], list(value))

        if isinstance(index, int):
            index = (index, )
        elif isinstance(index, slice):
            index = slice_to_range(index, self.digit_length())

        sign = self.sign
        self.x = abs(self.x)

        for i, v in zip(index, value):
            if v < 0 or v >= self.base:
                raise ValueError("Digit value out of bounds of base")
            i = absindex(i, self.digit_length())
            if self.base == 2: #binary optimisable
                if v == 1:
                    self.x |= (0b1 << i)
                else:
                    self.x &= ~(0b1 << i)
            else:
                pv = self.base ** i
                mask = self._mask_value_continuous(i)
                self.x = (self.x - mask) + (v * pv)

        if sign != 0:
            self.x *= sign
    __setitem__ = set_digit

    def delete_digit(self, index:Union[int,slice,range,Iterable[int]]):
        """
        `delete_digit`
        
        Removes the value at the given index (or indexes).

        Arguments:
            `index` -- The index (or indexes) digit to be removed.
        """

        if isinstance(index, slice):
            index = slice_to_range(index, self.digit_length())

        if isinstance(index, int):
            index = (index, )

        for i in sorted(index, reverse=True):
            self.pop(i)
    __delitem__ = delete_digit

    def unset_digit(self, index:Union[int,slice,range,Iterable[int]]):
        """
        `unset_digit`
        
        Unsets (set to 0) the value at the given index (or indexes).

        Arguments:
            `index` -- The index (or indexes) digit to be unset.
        """
        if isinstance(index, slice):
            index = slice_to_range(index, self.digit_length())

        if isinstance(index, int):
            index = (index, )

        sign = self.sign
        self.x = abs(self.x)

        if self.base == 2: #binary optimization
            for i in index:
                i = absindex(i, self.digit_length())
                self.x = (self.x >> 1) << 1
        else:
            for i in index:
                i = absindex(i, self.digit_length())
                self.x -= self._mask_value_continuous(i)

        if sign != 0:
            self.x *= sign

    #NOTE: just like python handles it in bit_length, a value of 0 will always have no digits
    def digit_length(self) -> int:
        """
        `digit_length`
        
        Similar to `bit_length`, but relitive to the current `base`.
        Not to be confused with `digit_count`.

        Returns:
            The minimum necessary about of digits needed to display the number in full.
        """
        if self.x == 0:
            return 0

        if self.base == 2:
            return abs(self.x).bit_length()
        else:
            c = 0
            v = abs(self.x)
            while v != 0:
                c += 1
                v //= self.base
            return c
    __len__ = digit_length

    def insert(self, index:int, value:Union[int,str,Iterable[Union[int,str]]]):
        """
        `insert`
        
        Inserts the given value (or values) before the given index.
        When given multiple values, each value will be inserted before the given index in order.

        Arguments:
            `index` -- The index (or indexes) to be inserted before.
            `value` -- The value (or values) to insert.
        """

        index = absindex(index, self.digit_length())

        if isinstance(value, Iterable):
            value = (self._ensure_unnotated(v) for v in value)
        else:
            value = self._ensure_unnotated(value)

        if isinstance(value, int):
            value = (value, )

        for v in value:
            if v < 0 or v >= self.base:
                raise ValueError("Digit value out of bounds of base")

            restore_sign = self.sign
            self.x = abs(self.x)

            if index == 0:
                self._prepend(v)
                continue

            high = self.copy()
            high.unset_digit(slice(0, index+1))

            if high.x != 0:
                self.x -= high.x
                high.x *= high.base
                self.x += high.x

            v = self.copy(v)
            v.x *= (v.base ** (index+1))
            self.x += v.x

            self.x *= restore_sign

    def pop(self, index:int = -1) -> int:
        """
        `pop`

        Gets the value at the given index while popping it.

        Keyword Arguments:
            index -- The target index to pop. Defaults to -1.

        Returns:
            The value at the given index before removal.
        """
        index = absindex(index, self.digit_length())

        if index == 0:
            return self._pop_first()

        popped = self._get_single_digit(index)
        high = self.copy()

        self.unset_digit(range(index, len(self)))
        high.unset_digit(range(0, index+1))

        if int(high) != 0:
            high.x //= high.base
            self.x += int(high)

        return popped

    def digit_count(self) -> int:
        """
        `digit_count`
        
        Similar to `bit_count`, but relitive to the current `base`.
        Not to be confused with `digit_length`.

        Returns:
            The amount of non-zero (non-unset) digits in the value.
        """
        if self.x == 0:
            return 0

        if self.base == 2:
            return abs(self.x).bit_count()
        else:
            c = 0
            v = abs(self.x)
            while v != 0:
                if v % self.base != 0:
                    c += 1
                v //= self.base
            return c

    #gets the specified digits with their place value as an int
    #a higher level implementation of the concept of bit masking done with binary numbers
    def mask(self, index:Union[int,slice,range,Iterable[int]]) -> int:
        """
        `mask`

        Similar to the concept of a 'bit mask', but on a arbitrary base.
        Returns a value with all digits unset except for the given index (or indexes).

        Arguments:
            index -- The index (or indexes) to mask the digits of.

        Returns:
            The value with all digits unset except for the given index (or indexes).
        """
        if isinstance(index, int):
            return self._mask_value_continuous(index)

        slices = []

        if isinstance(index, slice) and index.step == 1:
            slices = [index]
        else:
            if isinstance(index, slice):
                index = slice_to_range(index, self.digit_length())
            slices = iter_to_slices(cast(Iterable[int], index), self.digit_length())

        return sum(self._mask_value_continuous(s.start, s.stop - s.start) for s in slices)

    def digit_shift_left(self, amount:int):
        """
        `digit_shift_left`

        Similar to a binary shift left, shifts the value left according to the set base.

        Arguments:
            amount -- The amount to shift left. Will shift right when negative.
        """
        if amount < 0:
            self.digit_shift_right(-amount)
            return

        if self.base == 2:
            self.x = (abs(self.x) << amount) * self.sign
        else:
            self.x *= (self.base**amount)

    def digit_shift_right(self, amount:int):
        """
        `digit_shift_right`

        Similar to a binary shift right, shifts the value right according to the set base.

        Arguments:
            amount -- The amount to shift right. Will shift left when negative.
        """
        if amount < 0:
            self.digit_shift_left(-amount)
            return

        if self.base == 2:
            self.x = (abs(self.x) >> amount) * self.sign
        else:
            self.x //= (self.base**amount)

class ExtendedBasedIntiger(PositionalBasedIntiger):
    """
    `ExtendedBasedIntiger`
    
    A mutable sequence type of intiger that has a explicitly set base,
    allowing for specific digit values to be get and set.
    
    Supports any initger base starting at base 0.
    These bases are presumed to be in the traditional place value format of
    `value == d[x] * (base ** x)` where `value` is the value the digit holds in the intiger,
    `d` is a single digit value form a sequence of digits,
    `base` is the base,
    and `x` is the specific index in question of the intiger.
    This extends to bases 1 and 0 as best as possible.
    Base 1 acts as a tally system, with digits of only a single possible value,
    with that value being 0.
    This means that the base 1, while expected to have only one active digit,
    still uses antoher digit (naught) in order to display digits that do not hold value.
    Base 0 acts as a base that can only possibly hold a value of 0, and nothing else.
    This specific base stretches the conventional notion of positional notation
    as defined for use in this library.
    Due to the stretching and occasional breaking of these rules,
    these bases are only included in this 'extended' class.
    
    Supports many operators and methods that built in integers suport,
    casting the type back into a default intiger type when possible.
    
    Also supports customizable notation formats with the optional `notation_format` attribute.
    """
    def __init__(self,
                 value:Union[int, str] = 0,
                 base:int = 10,
                 *,
                 notation_format:Optional[NotationFormat] = DEFAULT_FORMAT
                ):

        self.__base:int = 2
        super().__init__(value, base, notation_format=notation_format)

    @override
    def copy(self,
             value:Optional[Union[int, str]] = None,
             base:Optional[int] = None,
             notation_format_override:Optional[NotationFormat] = None
            ) -> 'ExtendedBasedIntiger':
        """
        `copy`
        
        Creates a shallow copy of this object.

        Keyword Arguments:
            `value` -- When not `None`, will overrides the `x` value of the copy.
            `base` -- When not `None`, will overrides the `base` of the copy.
            `notation_format_override` -- When not `None`,
                will overrides the `notation_format` of the copy.

        Returns:
            The copy of the object.
        """
        if notation_format_override is not None:
            notation_format_override = self.notation_format
        return ExtendedBasedIntiger(value if value is not None else self.x,
                                      base if base is not None else self.base,
                                      notation_format = notation_format_override
                                     )
    __copy__ = copy
    @override
    def __deepcopy__(self, _ = None) -> 'ExtendedBasedIntiger':
        return self.copy(None,
                         None,
                         None if self.notation_format is None else self.notation_format.copy()
                        )

    @property
    @override
    def x(self) -> int:
        """
        `x`

        The explicit value of the intiger.
        """
        return self.__x
    @x.setter
    @override
    def x(self, value:int):
        if value == 0 and self.base == 1:
            raise BaseValueError("0 can not be represented in base 1")
        elif value != 0 and self.base == 0:
            raise BaseValueError("No value other than 0 can be represented in base 0")
        self.__x = value

    @property
    def base(self) -> int:
        """
        `base`

        The base of this number. Must be greater than or equal to 0.
        Base 0 and 1 are handled particularly differently than other bases.
        """
        return self.__base
    @base.setter
    def base(self, value:int):
        if self.x == 0 and value == 1:
            raise BaseValueError("0 can not be represented in base 1")
        elif self.x != 0 and value == 0:
            raise BaseValueError("No value other than 0 can be represented in base 0")
        elif value < 0:
            raise ValueError("Invalid base", value)
        self.__base = value

    @override
    def _get_single_digit(self, index:int) -> int:
        if self.base == 0:
            return 0
        elif self.base == 1:
            return 1 if index < abs(self.x) else 0
        else:
            return super()._get_single_digit(index)

    @override
    def _pop_first(self) -> int:
        if self.base == 0:
            return 0
        elif self.base == 1:
            self.x -= 1
            return 1
        else:
            return super()._pop_first()

    #this pushes a value into the units place
    #effectively shifts right while appending a new value to the units
    #slightly faster than the arbitrary insert method
    @override
    def _prepend(self, value:Union[int,str]):
        if self.base == 0:
            raise BaseInvalidOpperationError("Base 0 digits cannot be pushed")

        super()._prepend(value)

    @override
    def _mask_value_continuous(self, dindex: int, count: int = 1) -> int:
        if count <= 0:
            raise IndexError("The length of a continuous mask must be at least 1")

        if self.base == 0:
            return 0
        elif self.base == 1:
            return min(abs(self.x) - dindex, count)
        else:
            return super()._mask_value_continuous(dindex, count)

    @override
    def iter_digits(self, at_least:int = 0) -> Iterator[int]:
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Base {self.base} digits cannot be iterated")
        return super().iter_digits(at_least)

    @override
    def reversed_iter_digits(self, at_least:int = 0) -> Iterator[int]:
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Base {self.base} digits cannot be iterated")
        return super().reversed_iter_digits(at_least)

    @override
    def iter_symbols(self, at_least:int = 1) -> Iterator[str]:
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Base {self.base} digits cannot be iterated")
        return super().iter_symbols(at_least)

    @override
    def reversed_iter_symbols(self, at_least:int = 1) -> Iterator[str]:
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Base {self.base} digits cannot be iterated")
        return super().reversed_iter_symbols(at_least)

    @override
    def notate(self, notation_format:Optional[NotationFormat] = None) -> str:
        if self.base >= 2:
            return super().notate(notation_format)

        if notation_format is None:
            notation_format = self.notation_format

        if notation_format is None:
            raise BaseInvalidOpperationError("No format set, cannot notate")

        relevant_sign = ""
        if self.x < 0 and not notation_format.implicit_negative:
            if notation_format.negative_symbol is None:
                raise ValueError("Explicit negative values require a negative symbol")
            else:
                relevant_sign = notation_format.negative_symbol
        elif self.x > 0 and not notation_format.implicit_positive:
            if notation_format.positive_symbol is None:
                raise ValueError("Explicit positive values require a positive symbol")
            else:
                relevant_sign = notation_format.positive_symbol

        if self.base < 0:
            raise BaseValueError()
        elif self.base == 0:
            raise BaseInvalidOpperationError("Base 0 cannot be notated")
        elif self.base == 1:
            if notation_format.unity is None:
                raise NotationError("Cannot notate base 1 without a digit for unity")
            return relevant_sign + ((notation_format.unity) * self.x)
        else:
            raise BaseInvalidOpperationError()

    @overload
    @override
    def set_digit(self, index:int, value:Union[int,str]): ...
    @overload
    @override
    def set_digit(self, index:Union[slice,range,Iterable[int]], value:Iterable[Union[int,str]]): ...
    @override
    def set_digit(self,
                  index:Union[int,slice,range,Iterable[int]],
                  value:Union[int,str,Iterable[Union[int,str]]]
                 ):
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Digits cannot be set in base {self.base}")

        super().set_digit(index, value) #type: ignore

    @override
    def unset_digit(self, index:Union[int,slice,range,Iterable[int]]):
        if self.base < 2:
            raise BaseInvalidOpperationError(f"Cannot unset digits in base {self.base}")

        return super().unset_digit(index)

    #NOTE: just like python handles it in bit_length, a value of 0 will always have no digits
    @override
    def digit_length(self) -> int:
        if self.x == 0:
            return 0

        if self.base == 0:
            return 0
        if self.base == 1:
            return abs(self.x)
        else:
            return super().digit_length()


    @override
    def insert(self, index:int, value:Union[int,str,Iterable[Union[int,str]]]):
        if self.base == 0 or self.base == 1:
            raise BaseInvalidOpperationError(f"Cannot insert digits into a base {self.base} number")

        super().insert(index, value)

    @override
    def pop(self, index:int = -1) -> int:
        if self.base == 0:
            raise BaseInvalidOpperationError("Cannot pop digits form a base 0 number")
        elif self.base == 1:
            index = absindex(index, self.digit_length())
            self.x -= 1
            return 1
        else:
            return super().pop(index)

    #returns the count of non-zero (non-unset) digits
    @override
    def digit_count(self) -> int:
        if self.base < 2:
            raise BaseInvalidOpperationError(f"Cannot count digits in a base {self.base} number")
        else:
            return super().digit_count()

    @override
    def digit_shift_left(self, amount:int):
        if self.base == 0:
            raise BaseInvalidOpperationError("This base cannot be shifted")

        if amount < 0:
            self.digit_shift_right(-amount)
            return

        if self.base == 1:
            if self.sign == -1:
                amount *= -1
            self.x += amount
        else:
            super().digit_shift_left(amount)

    @override
    def digit_shift_right(self, amount:int):
        if self.base == 0:
            raise BaseInvalidOpperationError("This base cannot be shifted")

        if amount <= 0:
            self.digit_shift_left(-amount)
            return

        if self.base == 1:
            if self.sign == -1:
                amount *= -1
            self.x -= amount
        else:
            super().digit_shift_right(amount)

# give it a more common name
digitint = ExtendedBasedIntiger #pylint: disable=invalid-name
