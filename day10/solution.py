import sys
from typing import List, Optional, Tuple


def _read_input(path: str) -> List[str]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return [line[:-1] for line in file_content]


def _syntax_analysis(s: str) -> Tuple[Optional[int], List[str]]:
    stack = []
    for c in s:
        if c == '(' or c == '[' or c == '{' or c == '<':
            stack.append(c)
        else:
            if c == ')':
                expected = '('
            elif c == ']':
                expected = '['
            elif c == '}':
                expected = '{'
            elif c == '>':
                expected = '<'
            else:
                assert False

            if len(stack) == 0 or stack[-1] != expected:
                return c, []
            stack.pop()
    return None, stack


def solve1(l: List[str]) -> int:
    CHAR_SCORES = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    
    score = 0

    for x in l:
        illegal_char, _ = _syntax_analysis(x)
        if illegal_char is not None:
            score += CHAR_SCORES[illegal_char]

    return score


def solve2(l: List[str]) -> int:
    CHAR_SCORES = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }

    scores = []

    for x in l:
        illegal_char, stack = _syntax_analysis(x)
        if illegal_char is None:
            # Perform autocomplete for the incomplete lines
            autocomplete_score = 0
            for i in range(len(stack) - 1, -1, -1):
                autocomplete_score *= 5
                autocomplete_score += CHAR_SCORES[stack[i]]
            scores.append(autocomplete_score)

    assert len(scores) % 2 == 1
    scores = sorted(scores)
    return scores[len(scores) // 2]


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = _read_input(input_path)
    print(solve1(l))
    print(solve2(l))