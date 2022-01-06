import sys
from typing import List, Tuple, Optional
import numpy as np
from copy import deepcopy
import bisect


Range = List[int]


def parse_command(cmd: str) -> Tuple[bool, List[Range]]:
    turn_on = cmd[:2] == "on"
    if turn_on:
        cmd = cmd[3:].split(',')
    else:
        cmd = cmd[4:].split(',')
    assert len(cmd) == 3

    ranges = []
    for i in range(3):
        s = cmd[i][2:] # Cut off "x="/"y="/"z="
        s = s.split("..")
        start, end = int(s[0]), int(s[1])
        ranges.append([start, end])

    return turn_on, ranges


def read_input(path: str) -> List[Tuple[bool, List[Range]]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return [parse_command(line[:-1]) for line in file_content]


def solve1(commands: List[Tuple[bool, List[Range]]]) -> int:
    cubes = np.full((101, 101, 101), False, dtype=bool)

    for turn_on, ranges in commands:
        x_from, x_to = ranges[0]
        if x_from > 50 or x_to < -50:
            continue
        x_from, x_to = max(-50, x_from) + 50, min(50, x_to) + 50
        
        y_from, y_to = ranges[1]
        if y_from > 50 or y_to < -50:
            continue
        y_from, y_to = max(-50, y_from) + 50, min(50, y_to) + 50
        
        z_from, z_to = ranges[2]
        if z_from > 50 or z_to < -50:
            continue
        z_from, z_to = max(-50, z_from) + 50, min(50, z_to) + 50

        cubes[x_from:x_to+1, y_from:y_to+1, z_from:z_to+1] = turn_on

    return cubes.sum()


"""
Part 2, Approach 1
"""


FROM = 0
TO = 1


class CubeIntervalTree:
    range: Optional[Range] = None
    children: Optional[List['CubeIntervalTree']] = None
    is_on: Optional[bool] = None

    def __init__(self, interval: Optional[List[Range]]=None, turn_on: Optional[bool]=None, stored_interval: Optional[Range]=None) -> None:
        if interval is not None and turn_on is not None:
            assert 0 <= len(interval) and len(interval) <= 3
            if len(interval) > 0:
                self.children = [CubeIntervalTree(interval=interval[1:], turn_on=turn_on, stored_interval=interval[0])]
            else:
                self.is_on = turn_on
        if stored_interval is not None:
            self.range = stored_interval

    def get_from(self) -> int:
        assert self.range is not None
        return self.range[0]

    def get_to(self) -> int:
        assert self.range is not None
        return self.range[1]

    def _copy(self) -> 'CubeIntervalTree':
        copy_interval = CubeIntervalTree()
        if self.range is not None:
            copy_interval.range = deepcopy(self.range)
        if self.is_on is not None:
            copy_interval.is_on = self.is_on
        if self.children is not None:
            copy_interval.children = []
            for child in self.children:
                copy_interval.children.append(child._copy())
        return copy_interval

    def _split(self, threshold: int) -> 'CubeIntervalTree':
        assert self.range is not None
        other = self._copy()
        self.range[0] = threshold + 1
        other.range[1] = threshold
        return other

    def update_interval(self, interval: List[Range], turn_on: bool) -> None:
        if len(interval) == 0:
            assert self.children is None
            self.is_on = turn_on
            return
        
        new_children = []

        idx = 0
        while idx < len(self.children):
            assert len(interval) > 0
            
            if self.children[idx].get_to() < interval[0][FROM]:
                new_children.append(self.children[idx])
                idx += 1
                continue

            if interval[0][TO] < self.children[idx].get_from():
                new_children.append(CubeIntervalTree(interval=interval[1:], turn_on=turn_on, stored_interval=interval[0]))
                new_children += self.children[idx:]
                interval = []
                break

            if interval[0][FROM] < self.children[idx].get_from():
                interval_copy = deepcopy(interval)
                interval_copy[0][TO] = self.children[idx].get_from() - 1
                interval[0][FROM] = self.children[idx].get_from()
                new_children.append(CubeIntervalTree(interval=interval_copy[1:], turn_on=turn_on, stored_interval=interval_copy[0]))
                continue

            if self.children[idx].get_from() < interval[0][FROM]:
                other = self.children[idx]._split(interval[0][FROM] - 1)
                new_children.append(other)
                continue

            if self.children[idx].get_from() == interval[0][FROM]:
                if self.children[idx].get_to() == interval[0][TO]:
                    new_children.append(self.children[idx])
                    new_children[-1].update_interval(interval[1:], turn_on)
                    idx += 1
                    new_children += self.children[idx:]
                    interval = []
                    break

                if self.children[idx].get_to() < interval[0][TO]:
                    interval_copy = deepcopy(interval)
                    interval_copy[0][1] = self.children[idx].get_to()
                    interval[0][FROM] = self.children[idx].get_to() + 1
                    new_children.append(self.children[idx])
                    new_children[-1].update_interval(interval_copy[1:], turn_on)
                    idx += 1
                    continue

                if self.children[idx].get_to() > interval[0][TO]:
                    other = self.children[idx]._split(interval[0][TO])
                    new_children.append(other)
                    new_children[-1].update_interval(interval[1:], turn_on)
                    new_children += self.children[idx:]
                    interval = []
                    break

        if len(interval) > 0:
            new_children.append(CubeIntervalTree(interval=interval[1:], turn_on=turn_on, stored_interval=interval[0]))

        self.children = new_children

    def count_turned_on_cubes(self):
        if self.children is None:
            return 1 if self.is_on else 0

        count = 0
        for child in self.children:
            count += child.count_turned_on_cubes() * (child.get_to() - child.get_from() + 1)
        
        return count

    def get_str(self, depth: int=0) -> str:
        out_str = ""
        for _ in range(depth*3):
            out_str += " "
        out_str += f"d={depth}\n"
        if self.range is not None:
            for _ in range(depth*3):
                out_str += " "
            out_str += str(self.range)
            out_str += "\n"
        if self.is_on is not None:
            for _ in range(depth*3):
                out_str += " "
            out_str += str(self.is_on)
            out_str += "\n"
        if self.children is not None:
            for child in self.children:
                out_str += child.get_str(depth + 1)
            out_str += "\n"
        return out_str


def solve2(commands: List[Tuple[bool, List[Range]]]) -> int:
    tree = CubeIntervalTree(interval=commands[0][1], turn_on=commands[0][0])
    commands = commands[1:]
    for turn_on, interval_3d in commands:
        tree.update_interval(interval_3d, turn_on)
    return tree.count_turned_on_cubes()


"""
Part 2, Approach 2
"""


def solve2_v2(commands: List[Tuple[bool, List[Range]]]) -> int:
    xs = []
    ys = []
    zs = []

    for _, ranges in commands:
        xs.append(ranges[0][0])
        xs.append(ranges[0][1] + 1)
        ys.append(ranges[1][0])
        ys.append(ranges[1][1] + 1)
        zs.append(ranges[2][0])
        zs.append(ranges[2][1] + 1)

    xs = sorted(xs)
    ys = sorted(ys)
    zs = sorted(zs)

    N = len(xs)

    cubes = [[[False for _ in range(N)] for _ in range(N)] for _ in range(N)]

    for turn_on, cmd in commands:
        x0 = bisect.bisect_left(xs, cmd[0][0])
        x1 = bisect.bisect_left(xs, cmd[0][1] + 1)
        y0 = bisect.bisect_left(ys, cmd[1][0])
        y1 = bisect.bisect_left(ys, cmd[1][1] + 1)
        z0 = bisect.bisect_left(zs, cmd[2][0])
        z1 = bisect.bisect_left(zs, cmd[2][1] + 1)
        
        for i in range(x0, x1):
            for j in range(y0, y1):
                for k in range(z0, z1):
                    cubes[i][j][k] = turn_on

    count = 0
    for i in range(N - 1):
        for j in range(N - 1):
            for k in range(N - 1):
                count += cubes[i][j][k] * (xs[i+1] - xs[i]) * (ys[j+1] - ys[j]) * (zs[k+1] - zs[k])

    return count


if __name__ == "__main__":
    input_path = sys.argv[1]
    commands = read_input(input_path)
    # print(solve1(commands))
    print(solve2(commands))
    # print(solve2_v2(commands))