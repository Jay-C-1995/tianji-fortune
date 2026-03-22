from __future__ import annotations

from typing import Iterable, List, Sequence, TypeVar

T = TypeVar("T")


def shell_sort(items: Sequence[T], *, reverse: bool = False) -> List[T]:
    """
    Return a new list sorted with shell sort.

    Shell sort is a generalization of insertion sort that allows the exchange
    of elements that are far apart. It uses a decreasing sequence of gaps
    (Knuth's sequence: 1, 4, 13, 40, ...) to progressively sort the list.

    - Time: O(n log^2 n) average (with Knuth's gap sequence)
    - Space: O(n) due to copying input to a list
    - Not stable
    """
    arr = list(items)
    n = len(arr)
    if n < 2:
        return arr

    # Generate Knuth's gap sequence: 1, 4, 13, 40, 121, ...
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    # Reduce gap and perform gapped insertion sort for each gap size.
    while gap >= 1:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and (arr[j - gap] > temp) ^ reverse:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 3

    return arr


def _parse_ints(argv: Iterable[str]) -> List[int]:
    return [int(x) for x in argv]


if __name__ == "__main__":
    import sys

    # Usage:
    #   python shell_sort.py 3 1 2
    #   python shell_sort.py --reverse 3 1 2
    args = sys.argv[1:]
    reverse = False
    if args and args[0] in ("-r", "--reverse"):
        reverse = True
        args = args[1:]

    nums = _parse_ints(args) if args else [5, 1, 4, 2, 8]
    print(shell_sort(nums, reverse=reverse))
