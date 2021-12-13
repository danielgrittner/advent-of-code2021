import sys
from typing import List


class SparseFloor:
    floor: dict
    xs: int
    ys: int

    def __init__(self, ignore_diagonal_lines=True):
        self.floor = {}
        self.xs = 0
        self.ys = 0
        self.ignore_diag_lines = ignore_diagonal_lines

    def add_line(self, line: List[List[str]]) -> None:
        assert len(line) == 2
        x1, y1 = int(line[0][0]), int(line[0][1])
        x2, y2 = int(line[1][0]), int(line[1][1])

        self.xs = max(self.xs, max(x1, x2) + 1)
        self.ys = max(self.ys, max(y1, y2) + 1)

        x_diff = x2 - x1
        x_sign = x_diff // max(1, abs(x_diff))
        
        y_diff = y2 - y1
        y_sign = y_diff // max(1, abs(y_diff))

        if self.ignore_diag_lines:
            if x_diff != 0 and y_diff != 0:
                return

        curr = (x1, y1)
        end = (x2, y2)

        if curr in self.floor:
                self.floor[curr] += 1
        else:
            self.floor[curr] = 1

        while curr != end:
            curr = (curr[0] + x_sign, curr[1] + y_sign)
            if curr in self.floor:
                self.floor[curr] += 1
            else:
                self.floor[curr] = 1

    def get_floor_size(self):
        return self.xs, self.ys

    def get(self, x: int, y: int) -> int:
        point = (x, y)
        if point in self.floor:
            return self.floor[point]
        return 0


def _read_input(path: str, ignore_diag_lines) -> SparseFloor:
    with open(path, "r") as file_handle:
        file_content = [[pos.split(',') for pos in line[:-1].split(' -> ')] for line in file_handle.readlines()]
    
    sparse_floor = SparseFloor(ignore_diagonal_lines=ignore_diag_lines)
    for line in file_content:
        sparse_floor.add_line(line)

    return sparse_floor


def _count(path: str, diag_lines: bool) -> int:
    sparse_floor = _read_input(path, diag_lines)

    cnt = 0

    xs, ys = sparse_floor.get_floor_size()
    for x in range(xs):
        for y in range(ys):
            if sparse_floor.get(x, y) > 1:
                cnt += 1

    return cnt


def solve1(path: str) -> int:
    return _count(path, True)


def solve2(path: str) -> int:
    return _count(path, False)


if __name__ == "__main__":
    input_path = sys.argv[1]
    print(solve1(input_path))
    print(solve2(input_path))