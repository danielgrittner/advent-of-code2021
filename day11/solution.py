import sys
from typing import List
from collections import deque


def _read_input(path: str) -> List[List[int]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return [list(map(int, list(line[:-1]))) for line in file_content]


def _simulate_step(l: List[List[int]]) -> int:
    flashes = 0
    
    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] == 9:
                # Expand the flashing to surrounding
                q = deque()
                q.append((i, j))

                while len(q) > 0:
                    x, y = q.popleft()

                    l[x][y] += 1
                    if l[x][y] == 10:
                        # By only counting the flashes at 10, we ensure
                        # to only count each flash just once
                        flashes += 1
                        
                        # Expand
                        if x - 1 >= 0:
                            q.append((x-1, y))
                            if y - 1 >= 0:
                                q.append((x-1, y-1))
                            if y + 1 < len(l[x]):
                                q.append((x-1, y+1))

                        if y - 1 >= 0:
                            q.append((x, y-1))
                        if y + 1 < len(l[x]):
                            q.append((x, y+1))

                        if x + 1 < len(l):
                            q.append((x+1, y))
                            if y - 1 >= 0:
                                q.append((x+1, y-1))
                            if y + 1 < len(l[x+1]):
                                q.append((x+1, y+1))
                
            else:
                l[i][j] += 1

    # Now, we need to reset the flashes
    l = [[0 if x > 9 else x for x in row] for row in l]

    return l, flashes


def solve1(l: List[List[int]]) -> int:
    flashes = 0

    SIMULATION_STEPS = 100
    for _ in range(SIMULATION_STEPS):
        l, flashes_per_step = _simulate_step(l)
        flashes += flashes_per_step

    return flashes


def solve2(l: List[List[int]]) -> int:
    stop = len(l) * len(l[0])

    step = 1
    flashes_per_step = 0

    while flashes_per_step != stop:
        l, flashes_per_step = _simulate_step(l)
        step += 1

    return step


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = _read_input(input_path)
    print(solve1(l))
    print(solve2(l))