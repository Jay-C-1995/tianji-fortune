from __future__ import annotations

from typing import Iterable, List, Sequence, TypeVar

T = TypeVar("T")


def bubble_sort(items: Sequence[T], *, reverse: bool = False) -> List[T]:
    """
    Return a new list sorted with bubble sort.

    - Time: O(n^2)
    - Space: O(n) due to copying input to a list
    - Stable when reverse=False (and also for reverse=True as implemented)
    """
    arr = list(items)
    n = len(arr)
    if n < 2:
        return arr

    # Compare adjacent elements and "bubble" the extreme toward the end.
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - 1 - i):
            if (arr[j] > arr[j + 1]) ^ reverse:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def _parse_ints(argv: Iterable[str]) -> List[int]:
    return [int(x) for x in argv]


if __name__ == "__main__":
    import sys

    # Usage:
    #   python bubble_sort.py 3 1 2
    #   python bubble_sort.py --reverse 3 1 2
    args = sys.argv[1:]
    reverse = False
    if args and args[0] in ("-r", "--reverse"):
        reverse = True
        args = args[1:]

    nums = _parse_ints(args) if args else [5, 1, 4, 2, 8]
    print(bubble_sort(nums, reverse=reverse))
