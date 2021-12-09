import os 
import sys
from typing import List, Tuple


# We have 5x5 boards
BOARD_SIDE_LENGTH = 5


class BingoBoard:
    nums: dict
    row_hits: List[int]
    col_hits: List[int]

    def __init__(self, board: List[List[int]]) -> None:
        assert BOARD_SIDE_LENGTH == len(board) and BOARD_SIDE_LENGTH == len(board[0])
        
        self.nums = {}
        for i in range(BOARD_SIDE_LENGTH):
            for j in range(BOARD_SIDE_LENGTH):
                self.nums[board[i][j]] = (i, j)

        self.row_hits = [0 for _ in range(BOARD_SIDE_LENGTH)]
        self.col_hits = [0 for _ in range(BOARD_SIDE_LENGTH)]

    def mark(self, num: int) -> bool:
        if num in self.nums and self.nums[num] is not None:
            i, j = self.nums[num]
            self.row_hits[i] += 1
            self.col_hits[j] += 1
            self.nums[num] = None

            return self.row_hits[i] == BOARD_SIDE_LENGTH or self.col_hits[j] == BOARD_SIDE_LENGTH
        
        return False

    def get_score(self, last_num: int) -> int:
        unmarked_sum = 0
        for num in self.nums:
            if self.nums[num] is not None:
                unmarked_sum += num

        return unmarked_sum * last_num


def read_input(path: str) -> Tuple[List[BingoBoard], List[int]]:
    with open(path, "r") as file_handle:
        # Parse random numbers
        nums = file_handle.readline()
        nums = list(map(int, nums[:-1].split(',')))

        file_handle.readline()  # Empty line

        # Parse boards
        boards = []

        line = file_handle.readline()
        while len(line) > 0 and line != '\n':
            curr_board = []
            for _ in range(BOARD_SIDE_LENGTH):
                line = line[:-1] if line.endswith('\n') else line
                line = list(map(int, line.split()))
                curr_board.append(line)
                line = file_handle.readline()
            
            boards.append(BingoBoard(curr_board))
            
            line = file_handle.readline() # Skipy empty line

    return boards, nums


def solve1(boards: List[BingoBoard], nums: List[int]) -> int:
    for num in nums:
        for board in boards:
            if board.mark(num):
                return board.get_score(num)
    return -1


def solve2(boards: List[BingoBoard], nums: List[int]) -> int:
    ignore = [False for _ in range(len(boards))]
    winning_boards = 0
    
    for num in nums:
        for i, board in enumerate(boards):
            if ignore[i]:
                # This board already won.
                continue

            if board.mark(num):
                winning_boards += 1
                ignore[i] = True

                if winning_boards == len(boards):
                    # That was the last one!
                    return board.get_score(num)
                
    return -1


if __name__ == "__main__":
    input_path = sys.argv[1]
    boards, nums = read_input(input_path)
    print(solve1(boards, nums))
    print(solve2(boards, nums))