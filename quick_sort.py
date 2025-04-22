
from typing import Any, Callable

import operator


def _in_place_partition(lst: list, b: int, e: int, val=lambda s: s, reverse: bool = False) -> Any:
    """
    >>> a = [5, 7, 8, 9, 1, 2, 3, 4]
    >>> _in_place_partition(a, 0, len(a))
    4
    >>> a
    [1, 4, 3, 2, 5, 9, 8, 7]
    """
    if reverse:
        comp = operator.ge
    else:
        comp = operator.le

    pivot = lst[b]

    small_i = b + 1

    big_i = e

    while small_i != big_i:
        if comp(val(lst[small_i]), val(pivot)):
            small_i += 1
        else:
            big_i -= 1
            lst[big_i], lst[small_i] = lst[small_i], lst[big_i]

    lst[b], lst[small_i - 1] = lst[small_i - 1], pivot
    return small_i - 1


def quicksort(lst: list, b: int, e: int, val: Callable = lambda s: s, reverse: bool = False) -> None:
    """
    quicksort on sublist list[b:e] based on val values of each element

    >>> a = [5, 7, 8, 9, 1, 2, 3, 4]
    >>> quicksort(a, 0, len(a))
    >>> a
    [1, 2, 3, 4, 5, 7, 8, 9]

    >>> a = [5, 7, 8, 9, 1, 2, 3, 4]
    >>> quicksort(a, 0, len(a), reverse=True)
    >>> a
    [9, 8, 7, 5, 4, 3, 2, 1]
    """
    if e - b < 2:
        return

    pivot_index = _in_place_partition(lst, b, e, val, reverse)

    quicksort(lst, b, pivot_index, val, reverse)
    quicksort(lst, pivot_index + 1, e, val, reverse)

