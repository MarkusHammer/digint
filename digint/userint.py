"""
userint

Holds the `UserInt` and `ExtendedUserInt` classes.
"""

import operator
from functools import partialmethod, total_ordering
from sys import version_info
from .typings import * #pylint:disable=unused-wildcard-import, wildcard-import

class attr_forward_operators:#pylint: disable=invalid-name
    """
    `attr_forward_operators`

    Used to set an attribute of a class's opperators
    as the operators of it's containing class as well.
    """
    class partial_opperator:#pylint: disable=invalid-name
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

    class partial_inline_opperator:#pylint: disable=invalid-name
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
            if hasattr(operator, op_name) and isinstance(getattr(operator, op_name), Callable):
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
if version_info.minor >= 10:
    __USERINT_ABCS.append(SupportsIndex)

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

    def __bool__(self):
        return bool(self.x)

    def __bytes__(self):
        return bytes(self.x)

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

    #these are all handled by the decorators, but type checkers miss that sometimes
    def __abs__(self): ...
    def __neg__(self): ...
    def __pos__(self): ...
    def __invert__(self): ...

class ExtendedUserInt(UserInt):
    """
    `ExtendedUserInt`

    A class the extends `UserInt`, adding some basic quality of life attributes.
    """
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