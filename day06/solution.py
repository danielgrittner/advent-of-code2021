import sys
from typing import List


def read_input(path: str) -> List[int]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
        assert len(file_content) == 1
    l = list(map(int, file_content[0].split(',')))

    state = [0 for _ in range(9)]
    for x in l:
        state[x] += 1

    return state


def _simulate(days: int, state: List[int]) -> int:
    for _ in range(days):
        new_state = [0 for _ in range(9)]
        
        for t in range(9):
            if t == 0:
                new_state[8] += state[t]
                new_state[6] += state[t]
            else:
                new_state[t - 1] += state[t]

        state = new_state
            
    return sum(state)


def solve1(state: List[int]) -> int:
    return _simulate(80, state)


def solve2(state: List[int]) -> int:
    return _simulate(256, state)


if __name__ == "__main__":
    input_path = sys.argv[1]
    init_state = read_input(input_path)
    print(solve1(init_state))
    print(solve2(init_state))