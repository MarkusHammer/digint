"""
tools

Holds common tool functions and classes used in the `dint` module.
"""

from .typings import * #pylint:disable=unused-wildcard-import, wildcard-import

def absindex(index:int, reference_length:Union[Sized, int]) -> int:
    """
    `absindex`

    Takes the given index and the legnth contex its
    used in and returns a absolute index that
    wraps a negative index into a positive one while
    throwing relevant errors for out of bounds indexes.

    Arguments:
        index -- The index in question.
        reference_length -- The length of the object being sliced, or the `Sized` object itself.

    Raises:
        ValueError: Raised when an erroneous length is given.
        IndexError: Raised when the given index is / would be out of bounds.

    Returns:
        The absolute index (will never be negative).
    """

    length:int = 0
    if isinstance(reference_length, int):
        length = reference_length
    else:
        length = len(reference_length)

    if length < 0:
        raise ValueError(length)
    if index + length < 0:
        raise IndexError(index)

    return index if index >= 0 else length + index

def slice_to_range(sl:slice, reference_length:Union[Sized, int]) -> range:
    """
    `slice_to_range`
    
    Used to convert a `slice` object into a `range` object.

    Arguments:
        sl -- The source slice to convert.
        reference_length -- The length of the object being sliced, or the `Sized` object itself.

    Returns:
        The generated range from the slice.
    """

    length:int = 0
    if isinstance(reference_length, int):
        length = reference_length
    else:
        length = len(reference_length)

    if length < 0:
        raise IndexError("The reference length was negative")

    start = (absindex(sl.start, length) if (sl.start is not None) else 0)
    stop = (absindex(sl.stop, length) if (sl.stop is not None) else length)
    step = (sl.step if (sl.step is not None) else (1 if (start < stop) else -1))

    return range(start, stop, step)

# only makes slices of step 1, intentional
def iter_to_slices(i:Iterable[int], reference_length:Union[Sized, int]) -> Tuple[slice, ...]:
    """
    `iter_to_slices`

    Converts an iterable of integers into a series of slices with a `step` value of 1.

    Arguments:
        i -- The iterable to be converted.
        reference_length -- The length of the object being sliced, or the `Sized` object itself.

    Returns:
        A tuple of slices, each with a `step` of 1.
    """
    if isinstance(i, range):
        if i.step == 1:
            return (slice(i.start, i.stop, 1), )
        else:
            return tuple(slice(x, x+1, 1) for x in i)

    i = sorted(set(absindex(x, reference_length) for x in i))

    slices = []

    current_slice = None
    for v in i:
        if current_slice is None:
            current_slice = slice(v, v+1, 1)
        elif current_slice.stop == v:
            current_slice = slice(current_slice.start, v+1, 1)
        else:
            slices.append(current_slice)
            current_slice = None
    if current_slice is not None:
        slices.append(current_slice)

    return tuple(slices)
