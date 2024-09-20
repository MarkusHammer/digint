"""
errors

Holds all error classes for the `digint` module.
"""


class BaseValueError(ValueError):
    """
    `BaseValueError`

    Inherits `ValueError`

    Raised when a given value is impossible to be represented in a given base.
    """


class BaseInvalidOpperationError(ValueError):
    """
    `BaseInvalidOpperationError`

    Inherits `ValueError`

    Raised when a given opperation is impossible with a given base.
    """


class NotationError(ValueError):
    """
    `NotationError`

    Inherits `ValueError`

    Raised when a error is encountered during notation.
    """
