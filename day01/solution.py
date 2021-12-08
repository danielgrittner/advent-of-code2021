import os
from typing import List
import sys


def read_input(path: str) -> List[int]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return list(map(lambda l: int(l[:-1]), file_content))


def solve1(l: List[int]) -> int:
    cnt = 0
    for i in range(1, len(l)):
        if l[i] > l[i - 1]:
            cnt += 1
    return cnt


def solve2(l: List[int]) -> int:
    cnt = 0

    prev_sum = -1
    curr_sum = sum(l[:3])

    for i in range(3, len(l)):
        prev_sum = curr_sum
        
        # New window sum
        curr_sum -= l[i - 3]
        curr_sum += l[i]

        if curr_sum > prev_sum:
            cnt += 1

    return cnt


if __name__ == "__main__":
    l = read_input(sys.argv[1])
    print(solve1(l))
    print(solve2(l))
