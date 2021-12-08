import os
import sys
from typing import List, Tuple


class CommandTypes:
    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


class Command:
    command: str
    amount: int

    def __init__(self, command: str, amount: int) -> None:
        self.command = command
        self.amount = amount

    def apply(self, hor_pos: int, depth: int) -> Tuple[int, int]:
        if self.command == CommandTypes.FORWARD:
            hor_pos += self.amount
        elif self.command == CommandTypes.DOWN:
            depth += self.amount
        else:
            assert self.command == CommandTypes.UP
            depth -= self.amount
        return hor_pos, depth

    def apply2(self, hor_pos: int, depth: int, aim: int) -> Tuple[int, int, int]:
        if self.command == CommandTypes.DOWN:
            aim += self.amount
        elif self.command == CommandTypes.UP:
            aim -= self.amount
        else:
            assert self.command == CommandTypes.FORWARD
            hor_pos += self.amount
            depth += aim * self.amount
        return hor_pos, depth, aim


def read_input(path: str) -> List[Command]:
    with open(path, "r") as file_handle:
        file_content = map(lambda l: l[:-1].split(), file_handle.readlines())
    return list(map(lambda l: Command(l[0], int(l[1])), file_content))


def solve1(cmds: List[Command]) -> int:
    hor_pos, depth = 0, 0

    for cmd in cmds:
        hor_pos, depth = cmd.apply(hor_pos, depth)

    return hor_pos * depth


def solve2(cmds: List[Command]) -> int:
    hor_pos, depth, aim = 0, 0, 0

    for cmd in cmds:
        hor_pos, depth, aim = cmd.apply2(hor_pos, depth, aim)

    return hor_pos * depth


if __name__ == "__main__":
    file_path = sys.argv[1]
    l = read_input(file_path)
    print(solve1(l))
    print(solve2(l))
