from __future__ import annotations

from typing import Iterable, List, Sequence, TypeVar

T = TypeVar("T")


def quick_sort(items: Sequence[T], *, reverse: bool = False) -> List[T]:
    """
    Return a new list sorted with quick sort.

    - Time: O(n log n) average, O(n^2) worst case
    - Space: O(log n) average due to recursion stack
    - Not stable
    """
    arr = list(items)
    if len(arr) < 2:
        return arr

    def _quick_sort(low: int, high: int) -> None:
        if low >= high:
            return
        pivot_idx = _partition(low, high)
        _quick_sort(low, pivot_idx - 1)
        _quick_sort(pivot_idx + 1, high)

    def _partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if (arr[j] <= pivot) ^ reverse:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(0, len(arr) - 1)
    return arr


def _parse_ints(argv: Iterable[str]) -> List[int]:
    return [int(x) for x in argv]


if __name__ == "__main__":
    import sys

    # Usage:
    #   python quick_sort.py 3 1 2
    #   python quick_sort.py --reverse 3 1 2
    args = sys.argv[1:]
    reverse = False
    if args and args[0] in ("-r", "--reverse"):
        reverse = True
        args = args[1:]

    nums = _parse_ints(args) if args else [5, 1, 4, 2, 8]
    print(quick_sort(nums, reverse=reverse))
