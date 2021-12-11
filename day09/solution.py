import sys
from typing import List
from collections import deque


def _read_input(path: str) -> List[List[int]]:
    with open(path, "r") as file_handle:
        file_content = [list(map(int, line[:-1])) for line in file_handle.readlines()]
    return file_content


def _get_low_points(l: List[List[int]]) -> int:
    low_points = []

    for i in range(len(l)):
        for j in range(len(l[i])):
            curr = l[i][j]
            is_low = True

            if i - 1 >= 0 and curr >= l[i-1][j]:
                is_low = False

            if i + 1 < len(l) and curr >= l[i+1][j]:
                is_low = False

            if j - 1 >= 0 and curr >= l[i][j-1]:
                is_low = False

            if j + 1 < len(l[i]) and curr >= l[i][j+1]:
                is_low = False

            if is_low:
                low_points.append((i, j))

    return low_points


def solve1(l: List[List[int]]) -> int:
    return len(_get_low_points(l))


def solve2(l: List[List[int]]) -> int:
    low_points = _get_low_points(l)

    basin_sizes = []

    for i, j in low_points:
        q = deque()
        visited = set()
        
        q.append((i, j))
        visited.add((i, j))
        
        size = 0

        while len(q) > 0:
            x, y = q.popleft()
            cur_height = l[x][y]
            size += 1

            if x - 1 >= 0 and 9 > l[x-1][y] and l[x-1][y] > cur_height and (x-1, y) not in visited:
                q.append((x-1, y))
                visited.add((x-1, y))
            
            if x + 1 < len(l) and 9 > l[x+1][y] and l[x+1][y] > cur_height and (x+1, y) not in visited:
                q.append((x+1, y))
                visited.add((x+1, y))

            if y - 1 >= 0 and 9 > l[x][y-1] and l[x][y-1] > cur_height and (x, y-1) not in visited:
                q.append((x, y-1))
                visited.add((x, y-1))
            
            if y + 1 < len(l[x]) and 9 > l[x][y+1] and l[x][y+1] > cur_height and (x, y+1) not in visited:
                q.append((x, y+1))
                visited.add((x, y+1))

        basin_sizes.append(size)
        
        if len(basin_sizes) == 4:
            basin_sizes.sort()
            basin_sizes = basin_sizes[1:]

    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = _read_input(input_path)
    print(solve1(l))
    print(solve2(l))