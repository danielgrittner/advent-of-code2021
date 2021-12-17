import sys
from typing import List
import heapq
import math


def read_input(path: str) -> List[List[int]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return [list(map(int, line[:-1])) for line in file_content]


def _dijkstra(l: List[List[int]]) -> int:
    q = []
    visited = set()

    q.append((0, (0, 0)))
    visited.add((0, 0))

    while len(q) > 0:
        risk, (i, j) = heapq.heappop(q)
        if i == len(l)-1 and j == len(l[i])-1:
            return risk

        if i-1 >= 0 and (i-1, j) not in visited:
            heapq.heappush(q, (risk + l[i-1][j], (i-1, j)))
            visited.add((i-1, j))

        if i+1 < len(l) and (i+1, j) not in visited:
            heapq.heappush(q, (risk + l[i+1][j], (i+1, j)))
            visited.add((i+1, j))

        if j-1 >= 0 and (i, j-1) not in visited:
            heapq.heappush(q, (risk + l[i][j-1], (i, j-1)))
            visited.add((i, j-1))

        if j+1 < len(l[i]) and (i, j+1) not in visited:
            heapq.heappush(q, (risk + l[i][j+1], (i, j+1)))
            visited.add((i, j+1))

    return -1


def solve1(l: List[List[int]]) -> int:
    return _dijkstra(l)


def _a_star(l: List[List[int]]) -> int:
    n_small = len(l)
    m_small = len(l[0])
    
    n = n_small * 5
    m = m_small * 5

    def get_risk(x, y):
        block_x = x // n_small
        block_y = y // m_small
        row = x % n_small
        col = y % m_small
        r = l[row][col] + block_x + block_y
        if r >= 10:
            # We add at maximum 8!
            return r - 9
        return r

    def h(x, y):
        # Euclidean distance to goal as heuristic
        return math.sqrt((x - (n-1))**2 + (y - (m-1))**2)
    
    q = []
    visited = set()

    q.append((0, (0, 0, 0)))
    visited.add((0, 0))

    while len(q) > 0:
        _, (risk, i, j) = heapq.heappop(q)
        if i == n-1 and j == m-1:
            return risk

        if i-1 >= 0 and (i-1, j) not in visited:
            new_risk = risk + get_risk(i-1, j)
            heapq.heappush(q, (new_risk + h(i-1, j), (new_risk, i-1, j)))
            visited.add((i-1, j))

        if i+1 < n and (i+1, j) not in visited:
            new_risk = risk + get_risk(i+1, j)
            heapq.heappush(q, (new_risk + h(i+1, j), (new_risk, i+1, j)))
            visited.add((i+1, j))

        if j-1 >= 0 and (i, j-1) not in visited:
            new_risk = risk + get_risk(i, j-1)
            heapq.heappush(q, (new_risk + h(i, j-1), (new_risk, i, j-1)))
            visited.add((i, j-1))

        if j+1 < m and (i, j+1) not in visited:
            new_risk = risk + get_risk(i, j+1)
            heapq.heappush(q, (new_risk + h(i, j+1), (new_risk, i, j+1)))
            visited.add((i, j+1))

    return -1


def solve2(l: List[List[int]]) -> int:
    return _a_star(l)


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = read_input(input_path)
    print(solve1(l))
    print(solve2(l))