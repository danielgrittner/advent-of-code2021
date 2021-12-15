from os import read
import sys
from typing import List, Tuple


HASHTAG = True
DOT = False


class FoldInstruction:
    dir: str
    axis: int

    def __init__(self, input: str) -> None:
        if input.startswith("y="):
            self.dir = "y"
        else:
            assert input.startswith("x=")
            self.dir = "x"
        self.axis = int(input[2:])

    def _fold_y(self, field: List[List[bool]]) -> List[List[bool]]:
        assert self.dir == "y"

        new_field = [[DOT for _ in range(self.axis)] for _ in range(len(field))]
        
        for row in range(len(field)):
            # Combine column-wise
            i, j = self.axis - 1, self.axis + 1

            while i >= 0:
                assert j < len(field[i])
                new_field[row][i] = field[row][i] or field[row][j]
                i -= 1
                j += 1

            assert i == -1 and j == len(field[0])

        return new_field

    def _fold_x(self, field: List[List[bool]]) -> List[List[bool]]:
        assert self.dir == "x"
        
        new_field = [[DOT for _ in range(len(field[0]))] for _ in range(self.axis)]

        for col in range(len(field[0])):
            # Combine row-wise
            i, j = self.axis - 1, self.axis + 1

            while i >= 0:
                assert j < len(field)
                new_field[i][col] = field[i][col] or field[j][col]
                i -= 1
                j += 1

            assert i == -1 and j == len(field)

        return new_field

    def fold(self, field: List[List[bool]]) -> List[List[bool]]:
        if self.dir == "y":
            return self._fold_y(field)
        return self._fold_x(field)


def _create_field(input: List[List[int]]) -> List[List[bool]]:
    xs = max(map(lambda x: x[0], input)) + 1
    ys = max(map(lambda x: x[1], input)) + 1

    field = [[DOT for _ in range(ys)] for _ in range(xs)]
    
    for pos in input:
        field[pos[0]][pos[1]] = HASHTAG

    return field


def read_input(path: str) -> Tuple[List[List[bool]], List[FoldInstruction]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()

    i = 0
    while i < len(file_content) and file_content[i] != '\n':
        i += 1

    field_input = [[int(num) for num in line[:-1].split(',')] for line in file_content[:i]]
    instrs = [FoldInstruction(line.split()[-1]) for line in file_content[i+1:]]

    return _create_field(field_input), instrs


def solve1(field: List[List[bool]], instrts: List[FoldInstruction]) -> int:
    field = instrts[0].fold(field)
    return sum([sum(x) for x in field])


def _print_field(field: List[List[bool]]) -> None:
    for y in range(len(field[0])):
        curr_row = []
        for x in range(len(field)):
            curr_row.append('.' if field[x][y] == DOT else '#')
        print(''.join(curr_row))


def solve2(field: List[List[str]], instrts: List[FoldInstruction]) -> None:
    for instr in instrts:
        field = instr.fold(field)
    _print_field(field)


if __name__ == "__main__":
    input_path = sys.argv[1]
    field, instrts = read_input(input_path)
    print(solve1(field, instrts))
    solve2(field, instrts)