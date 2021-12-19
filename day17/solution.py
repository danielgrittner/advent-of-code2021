import sys
from typing import List, Tuple, Optional
import math


def read_input(path: str) -> List[List[int]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()[0][:-1]
    file_content = file_content[len("target area: "):].split(", ")
    return [list(map(int, x[2:].split(".."))) for x in file_content]


def _gaussian_sum_formula(i: int) -> int:
    return i * (i + 1) // 2


def _min_steps(x) -> int:
    # quadratic formula for approximating the first x which hits the target
    return int(math.ceil(-0.5 + math.sqrt(0.25 + 2 * x)))


def _step(probe_x: int, probe_y: int, velo_x: int, velo_y: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    probe_x += velo_x
    probe_y += velo_y
    velo_x += -1 if velo_x > 0 else (1 if velo_x < 0 else 0)
    velo_y -= 1
    return (probe_x, probe_y), (velo_x, velo_y)


def _is_in_target(probe_x: int, probe_y: int, target_coords: List[List[int]]) -> bool:
    return (target_coords[0][0] <= probe_x and probe_x <= target_coords[0][1]) and \
            (target_coords[1][0] <= probe_y and probe_y <= target_coords[1][1])


def _simulate(velo_x: int, velo_y: int, target_coords: List[List[int]]) -> Optional[int]:
    max_y = 0
    x, y = 0, 0
    while x <= target_coords[0][1] and y >= target_coords[1][0]:
        (x, y), (velo_x, velo_y) = _step(x, y, velo_x, velo_y)
        max_y = max(max_y, y)

        if _is_in_target(x, y, target_coords):
            return max_y

    return -1


def solve1(target_coords: List[List[int]]) -> int:
    velo_x = _min_steps(target_coords[0][0]) # smallest x-velocity reaching the target

    max_h = 0
    while True:
        if _gaussian_sum_formula(velo_x) > target_coords[0][1]:
            # We would overshoot when trying to maximize the height, i.e., velo_y > 0!
            break

        velo_y = 1
        while velo_y <= 1000: # TODO: How can we best approximate this number?
            curr_max_y = _simulate(velo_x, velo_y, target_coords)
            max_h = max(max_h, curr_max_y)
            velo_y += 1

        velo_x += 1

    return max_h


def solve2(target_coords: List[List[int]]) -> int:
    cnt = 0
    # TODO: Can we set the bounds better?
    for velo_x in range(_min_steps(target_coords[0][0]), 1000):
        for velo_y in range(-1000, 1000):
            curr_max_y = _simulate(velo_x, velo_y, target_coords)
            if curr_max_y != -1:
                cnt += 1
    return cnt


if __name__ == "__main__":
    input_path = sys.argv[1]
    target_coords = read_input(input_path)
    assert len(target_coords) == 2 and target_coords[0][0] > 0 and target_coords[0][1] > 0 \
        and target_coords[1][0] < 0 and target_coords[1][1] < 0
    print(solve1(target_coords))
    print(solve2(target_coords))