import sys
from typing import Tuple


def read_input(path: str) -> Tuple[int, int]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    p1 = int(file_content[0][-2]) - 1
    p2 = int(file_content[1][-2]) - 1
    return p1, p2


def solve1(p1: int, p2: int) -> int:
    score_p1 = 0
    score_p2 = 0

    dice = 0
    rolls = 0

    while score_p1 < 1000 and score_p2 < 1000:
        # Player 1
        for _ in range(3):
            p1 = (p1 + dice + 1) % 10
            dice = (dice + 1) % 100
        score_p1 += p1 + 1
        rolls += 3
        if score_p1 >= 1000:
            break

        # Player 2
        for _ in range(3):
            p2 = (p2 + dice + 1) % 10
            dice = (dice + 1) % 100
        score_p2 += p2 + 1
        rolls += 3

    if score_p1 >= 1000:
        return score_p2 * rolls
    else:
        return score_p1 * rolls


def _move_player(memo: dict, rolls: int, p1: int, score_p1: int, p2: int, score_p2: int) -> Tuple[int, int]:
    key = (rolls, p1, score_p1, p2, score_p2)
    if key in memo:
        return memo[key]
    
    if rolls == 3:
        score_p1 += p1 + 1
        if score_p1 >= 21:
            # P1 won!
            return 1, 0
        
        # Other players turn!
        wins_p2, wins_p1 = _move_player(memo, 0, p2, score_p2, p1, score_p1)
        result = wins_p1, wins_p2
        memo[key] = result

        return result

    assert 0 <= rolls and rolls < 3
    
    wins_p1_univ1, wins_p2_univ1 = _move_player(memo, rolls + 1, (p1 + 1) % 10, score_p1, p2, score_p2)
    wins_p1_univ2, wins_p2_univ2 = _move_player(memo, rolls + 1, (p1 + 2) % 10, score_p1, p2, score_p2)
    wins_p1_univ3, wins_p2_univ3 = _move_player(memo, rolls + 1, (p1 + 3) % 10, score_p1, p2, score_p2)

    result = wins_p1_univ1 + wins_p1_univ2 + wins_p1_univ3, wins_p2_univ1 + wins_p2_univ2 + wins_p2_univ3
    memo[key] = result
    return result



def solve2(p1: int, p2: int) -> int:
    return max(*_move_player({}, 0, p1, 0, p2, 0))


if __name__ == "__main__":
    input_path = sys.argv[1]
    p1, p2 = read_input(input_path)
    print(solve1(p1, p2))
    print(solve2(p1, p2))