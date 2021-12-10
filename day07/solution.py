import sys
from typing import List
import math


def read_input(path: str) -> List[int]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
        assert len(file_content) == 1
        file_content = file_content[0]
    return list(map(int, file_content.split(",")))


def _naive_median(l: List[int]) -> int:
    """
    Naive algorithm
    Runtime: O(nlogn)
    """
    l.sort()
    k = len(l) // 2
    return l[k]


def _median_of_medians(l: List[int], i: int) -> int:
    """
    Runtime: O(n)
    Source: https://brilliant.org/wiki/median-finding-algorithm/
    """
    chunks = [l[j:min(j+5, len(l))] for j in range(0, len(l), 5)]
    medians_of_chunks = [_naive_median(c) for c in chunks]

    if len(medians_of_chunks) <= 5:
        return _naive_median(medians_of_chunks)
    
    pivot = _median_of_medians(medians_of_chunks, len(medians_of_chunks) // 2)

    left = [x for x in l if x < pivot]
    middle = [x for x in l if x == pivot]
    right = [x for x in l if x > pivot]

    if len(left) <= i and i < len(left) + len(middle):
        return pivot

    if i < len(left):
        return _median_of_medians(left, i)

    return _median_of_medians(right, i - (len(left) + len(middle)))


def median(l: List[int]) -> int:
    return _median_of_medians(l, len(l) // 2)


def solve1(l: List[int]) -> int:
    target = median(l)

    out = 0
    for x in l:
        out += abs(x - target)
    return out


def solve2(l: List[int]) -> int:
    # Average
    target1 = int(math.floor(sum(l) / len(l)))
    target2 = int(math.ceil(sum(l) / len(l)))

    out1 = 0
    out2 = 0
    for x in l:
        diff1 = abs(x - target1)
        out1 += (diff1 * (diff1 + 1)) // 2

        diff2 = abs(x - target2)
        out2 += (diff2 * (diff2 + 1)) // 2

    return min(out1, out2)


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = read_input(input_path)
    print(solve1(l))
    print(solve2(l))