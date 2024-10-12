"""
userint

Holds the `UserInt` and `ExtendedUserInt` classes.
"""

import operator
from functools import partialmethod, total_ordering
from sys import version_info
from .typings import * # pylint:disable=unused-wildcard-import, wildcard-import


class attr_forward_operators: # pylint:disable=invalid-name
    """
    `attr_forward_operators`

    Used to set an attribute of a class's opperators
    as the operators of it's containing class as well.
    """
    class partial_opperator: # pylint:disable=invalid-name
        """
        `partial_opperator`

        Used to get partial callable to a specific opperator of a attribute of the target class.
        """

        def __init__(self, operator_module_attr_name:str, instance_attr_name:str):
            self.op_func:Callable = getattr(operator, operator_module_attr_name)
            self.instance_attr_name:str = instance_attr_name

        def __call__(self, inst_self, *args, **kwargs):
            return self.op_func(getattr(inst_self, self.instance_attr_name), *args, **kwargs)

        def callable_method(self) -> partialmethod:
            """
            `callable_method`

            Returns:
                A partial callable method to the operator.
            """
            return partialmethod(self)

    class partial_inline_opperator: # pylint:disable=invalid-name
        """
        `partial_inline_opperator`

        Similar to `partial_opperator`, but specifically compatable with inline opperators instead.
        """

        def __init__(self, operator_module_attr_name:str, instance_attr_name:str):
            self.op_func:Callable = getattr(operator, operator_module_attr_name)
            self.instance_attr_name:str = instance_attr_name

        def __call__(self, inst_self, *args, **kwargs):
            setattr(inst_self,
                    self.instance_attr_name,
                    self.op_func(getattr(inst_self, self.instance_attr_name), *args, **kwargs))
            return inst_self

        def callable_method(self) -> partialmethod:
            """
            `callable_method`

            Returns:
                A partial callable method to the inline operator.
            """
            return partialmethod(self)

    @staticmethod
    def undunder(name:str) -> str:
        """
        `undunder`

        Removes underscores form an attribute name.

        Arguments:
            name -- The attribute to remove underscores from.

        Returns:
            The name with underscores removed.
        """
        return name.strip("_")

    @staticmethod
    def dunder(name:str) -> str:
        """
        `dunder`

        Add the proper amount of underscores to an attribute name.

        Arguments:
            name -- The attribute to add underscores to.

        Returns:
            The name with underscores added.
        """
        return f"__{attr_forward_operators.undunder(name)}__"

    @staticmethod
    def inline_name(name:str) -> str:
        """
        `inline_name`

        Gets returns the inline name for the given opperator.

        Arguments:
            name -- The operator to get the inline name of.

        Returns:
            The inline opperator name.
        """
        return f"i{attr_forward_operators.undunder(name)}"

    @staticmethod
    def inline_name_dunder(name:str) -> str:
        """
        `inline_name_dunder`

        Gets returns the inline double underscored name for the given opperator.

        Arguments:
            name -- The operator to get the underscored inline name of.

        Returns:
            The underscored inline opperator name.
        """
        return f"__i{attr_forward_operators.undunder(name)}__"

    def __init__(self,
                 instance_attr_name:str,
                 *opperator_names:str,
                 set_undundered:bool = False,
                 replace_existing:bool = False,
                 set_inline:bool = False
                 ):
        self.instance_attr_name:str = instance_attr_name
        self.opperator_names:Tuple[str, ...] = opperator_names
        self.set_undundered:bool = set_undundered
        self.set_inline:bool = set_inline
        self.replace_existing:bool = replace_existing

    def __call__(self, cls:Type) -> Type:
        for op_name in self.opperator_names:
            dundered = self.dunder(op_name)
            undundered = self.undunder(op_name)

            operator_name = None
            if hasattr(operator, op_name) and callable(getattr(operator, op_name)):
                operator_name = op_name
            elif hasattr(operator, undundered):
                operator_name = undundered
            elif hasattr(operator, dundered):
                operator_name = dundered

            if operator_name is None:
                raise NameError(f"Operator {op_name} was not found in the operators module")

            op = self.partial_opperator(operator_name, self.instance_attr_name)
            targets = {dundered : op.callable_method()}

            if self.set_undundered:
                targets[undundered] = op.callable_method()

            if self.set_inline:
                iop = self.partial_inline_opperator(operator_name,self.instance_attr_name)
                targets[self.inline_name_dunder(op_name)] = iop.callable_method()
                if self.set_undundered:
                    targets[self.inline_name(op_name)] = iop.callable_method()

            if not self.replace_existing:
                for target_name in targets:
                    if hasattr(cls, target_name):
                        raise PermissionError(f"Attempted to overwrite prexisting method {op_name}")

            for name, func in targets.items():
                setattr(cls, name, func)

        return cls


__USERINT_ABCS:List[Type] = [SupportsInt,
                             SupportsFloat,
                             SupportsAbs,
                             SupportsComplex,
                             SupportsRound]
if version_info.major >= 3 and version_info.minor >= 10:
    __USERINT_ABCS.append(SupportsIndex)
    __USERINT_ABCS.append(HashableABC)


@attr_forward_operators("x", "xor", "lshift", "rshift", replace_existing=True, set_inline=True)
@attr_forward_operators("x", "and_", "or_", replace_existing=True, set_inline=True)
@attr_forward_operators("x", "invert", replace_existing=True)
@attr_forward_operators("x", "neg", "abs", "pos", replace_existing=True)
@attr_forward_operators("x", "floordiv", "mod", "pow", set_inline=True)
@attr_forward_operators("x", "add", "sub", "mul", "truediv", set_inline=True)
@total_ordering
@attr_forward_operators("x", "lt", "eq", "gt", "le", "ge", replace_existing=True)
class UserInt(*tuple(__USERINT_ABCS)):
    """
    `UserInt`

    A class making a extendable intiger type, using the x attribute.
    Based off of the intent of objects like `UserList`, for the `int` type.

    (Source: Some of the following docstring descriptions are derived form the official python docs:
    https://docs.python.org/3/library/stdtypes.html)
    """
    def __init__(self, x:int):
        self.__x:int = x

    @property
    def x(self) -> int:
        """
        `x`

        The explicit value of the intiger.
        """
        return self.__x

    @x.setter
    def x(self, value:int):
        self.__x = value

    def __int__(self):
        return self.x
    __index__ = __int__
    __trunc__ = __int__
    __floor__ = __int__
    __ceil__ = __int__

    def __hash__(self):
        return hash(self.x)

    def __bool__(self):
        return bool(self.x)

    def __float__(self):
        return float(self.x)

    def __complex__(self):
        return complex(self.x)

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return repr(self.x)

    def __format__(self, s):
        return format(self.x, s)

    def __round__(self, ndigits:Union[None, int] = None) -> int:
        return round(self.x, ndigits)

    def bit_count(self) -> int:
        """
        `bit_count`

        Number of ones in the binary representation of the absolute value of self.

        Also known as the population count.
        """
        return self.x.bit_count()

    def bit_length(self) -> int:
        """
        `bit_count`

        Number of bits necessary to represent self in binary.
        """
        return self.x.bit_length()

    def to_bytes(self,
                 length:SupportsIndex,
                 byteorder:Literal['little', 'big'],
                 *,
                 signed:bool = False
                 ) -> bytes:
        """
        `to_bytes`

        Arguments:
        Convert the 'int' into an array of 'bytes' representing the intiger.
        Wraps `int.to_bytes()`

        Arguments:
            `length` -- Length of bytes object to use.
            An `OverflowError` is raised if the integer is not
            representable with the given number of bytes.

            `byteorder` -- The byte order used to represent the integer. If `byteorder` is `'big'`,
            the most significant byte is at the beginning of the byte array. If
            `byteorder` is `'little'`, the most significant byte is at the end of the
            byte array. To request the native byte order of the host system, use
            `sys.byteorder` as the byte order value.

            `signed` -- Determines whether two's complement is used to represent the integer.
            If signed is `False` and a negative integer is given, an `OverflowError`
            is raised.

        """
        return self.x.to_bytes(length, byteorder, signed=signed)

    def is_integer(self) -> bool:
        """
        `is_integer`

        Always returns True. Exists for duck type compatibility with `float.is_integer()`.
        """
        return True

    # these are all handled by the decorators, but type checkers miss that sometimes
    def __abs__(self): ...
    def __neg__(self): ...
    def __pos__(self): ...
    def __invert__(self): ...


class ExtendedUserInt(UserInt):
    """
    `ExtendedUserInt`

    A class the extends `UserInt`, adding some basic quality of life attributes.
    """

    def __init__(self, x:int):
        super().__init__(x)

        self.__x:int = x
        self.__high:Optional[int] = None
        self.__low:Optional[int] = None
        self.on_changed:Optional[Callable[['ExtendedUserInt', int], Any]] = None
        """
        `on_changed`

        The `Callable` call back to be called **after** the
        `x` property is set, providing a reference to
        the current instance after the change is applied,
        and the `int` value `x` was previous to the change.

        When set to `None` (as by default), no callback will be triggered.
        """

    @property
    def x(self) -> int:
        """
        `x`

        The explicit value of the intiger.
        """
        return self.__x

    @x.setter
    def x(self, value:int):
        if self.limit_low is not None:
            value = max(value, self.limit_low)
        if self.limit_high is not None:
            value = min(value, self.limit_high)
        old = self.__x
        self.__x = value
        if callable(self.on_changed):
            self.on_changed(self, old) # pylint:disable=not-callable

    @property
    def limit_high(self) -> Optional[int]:
        """
        limit_high

        The high limit for the value of `x`, if any.
        `None` means there is no limit.
        Raises `ValueError` when the high limit is lower than the low limit, if both are not `None`.
        """
        return self.__high

    @limit_high.setter
    def limit_high(self, value:Optional[int]):
        if value is not None and self.limit_low is not None and self.limit_low > value:
            raise ValueError("A high limit must not be less than the low limit")
        self.__high = value
        if self.__high is not None and self.x > self.__high:
            self.x = self.__high

    @property
    def limit_low(self) -> Optional[int]:
        """
        limit_low

        The low limit for the value of `x`, if any.
        `None` means there is no limit.
        Raises `ValueError` when the low limit is higher than the high limit,
        if both are not `None`.
        """
        return self.__low

    @limit_low.setter
    def limit_low(self, value:Optional[int]):
        if value is not None and self.limit_high is not None and self.limit_high < value:
            raise ValueError("A low limit must not be greater than the high limit")
        self.__low = value
        if self.__low is not None and self.x > self.__low:
            self.x = self.__low

    @property
    def sign(self) -> int:
        """
        `sign`

        `-1` if `x` is negative, `1` if `x` is positive, `0` if `x` is `0`.
        """
        return 0 if self.x == 0 else (1 if self.x > 0 else -1)

    @sign.setter
    def sign(self, value:int):
        value = max(min(value, 1), -1)
        if value == 0:
            self.x = 0
        elif self.sign != value:
            self.x *= -1

    def fixed_sign_invert(self) -> int:
        """
        `fixed_sign_invert`

        Returns:
            The absolute value of this intiger, inverted, with its sign restored after.
                If this intiger is 0, the value returned is `~0` (`0` inverted), not `0`.
        """
        return (~abs(self.x)) * (-1 if self.x < 0 else 1)

    def fixed_sign_and(self, value:int) -> int:
        """
        `fixed_sign_and`

        Returns:
            The absolute value of this intiger, and-ed with the given `value`,
                with its sign restored after.
        """
        return (abs(self.x) & value) * (-1 if self.x < 0 else 1)

    def fixed_sign_or(self, value:int) -> int:
        """
        `fixed_sign_or`

        Returns:
            The absolute value of this intiger, or-ed with the given `value`,
                with its sign restored after.
        """
        return (abs(self.x) | value) * (-1 if self.x < 0 else 1)

    def fixed_sign_xor(self, value:int) -> int:
        """
        `fixed_sign_xor`

        Returns:
            The absolute value of this intiger, xor-ed with the given `value`,
                with its sign restored after.
        """
        return (abs(self.x) ^ value) * (-1 if self.x < 0 else 1)
