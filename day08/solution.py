import sys
from typing import List, Tuple


class Signals:
    signal_pattern: List[str]
    output_value: List[str]

    def __init__(self, signal_pattern: List[str], output_value: List[str]) -> None:
        self.signal_pattern = [''.join(sorted(x)) for x in signal_pattern]
        self.output_value = [''.join(sorted(x)) for x in output_value]

    def get_signal_patterns(self) -> List[str]:
        return self.signal_pattern

    def get_output_values(self) -> List[str]:
        return self.output_value


def _read_input(path: str) -> List[Signals]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
        file_content = [[x.split() for x in line[:-1].split(' | ')] for line in file_content]
    
    return [Signals(signal[0], signal[1]) for signal in file_content]


"""
Patterns:

             0:      1:      2:      3:      4:
             aaaa    ....    aaaa    aaaa    ....
            b    c  .    c  .    c  .    c  b    c
            b    c  .    c  .    c  .    c  b    c
             ....    ....    dddd    dddd    dddd
            e    f  .    f  e    .  .    f  .    f
            e    f  .    f  e    .  .    f  .    f
             gggg    ....    gggg    gggg    ....
Lengths:    6        2       5       5       4

             5:      6:      7:      8:      9:
             aaaa    aaaa    aaaa    aaaa    aaaa
            b    .  b    .  .    c  b    c  b    c
            b    .  b    .  .    c  b    c  b    c
             dddd    dddd    ....    dddd    dddd
            .    f  e    f  .    f  e    f  .    f
            .    f  e    f  .    f  e    f  .    f
             gggg    gggg    ....    gggg    gggg
Lengths:    5       6       3       7        6

Numbers with unique lengths:

1 -> l=2
4 -> l=4
7 -> l=3
8 -> l=7

"""


LENGTH_TO_NUMBER = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
    
    # None unique lengths
    6: None,
    5: None,
}


def _get_unique_length_patterns(signal_patterns: List[str]) -> Tuple[str, str, str, str]:
    for pattern in signal_patterns:
        num = LENGTH_TO_NUMBER[len(pattern)]
        if num is not None:
            if num == 1:
                one_pattern = pattern
            elif num == 4:
                four_pattern = pattern
            elif num == 7:
                seven_pattern = pattern
            else:
                assert num == 8
                eight_pattern = pattern
    
    return one_pattern, four_pattern, seven_pattern, eight_pattern


def solve1(signals: List[Signals]) -> int:
    ones = 0
    fours = 0
    sevens = 0
    eights = 0

    for signal in signals:
        one_pattern, four_pattern, seven_pattern, eight_pattern = \
                _get_unique_length_patterns(signal.get_signal_patterns())
        
        for output_val in signal.get_output_values():
            if output_val == one_pattern:
                ones += 1
            elif output_val == four_pattern:
                fours += 1
            elif output_val == seven_pattern:
                sevens += 1
            elif output_val == eight_pattern:
                eights += 1

    return ones + fours + sevens + eights


def _set_diff(signal1: List[str], signal2: List[str]) -> List[str]:
    s1, s2 = set(signal1), set(signal2)
    return sorted(list(s1 - s2))


def _set_intersect(signal1: List[str], signal2: List[str]) -> List[str]:
    s1, s2 = set(signal1), set(signal2)
    return sorted(list(s1 & s2))


def _is_set_subset(signal1: List[str], signal2: List[str]) -> List[str]:
    s1, s2 = set(signal1), set(signal2)
    return s1 <= s2

def _infer_wires(signal_patterns: List[str]) -> List[str]:
    """
        Example:
             aaaa
            b    c
            b    c
             dddd
            e    f
            e    f
             gggg

        Gets encoded into: [a, b, c, d, e, f, g]
    """
    wires = ['' for _ in range(7)]

    one_pattern, four_pattern, seven_pattern, eight_pattern = \
                _get_unique_length_patterns(signal_patterns)

    # 1) Determine top wire: 7 \ 1 
    wires[0] = _set_diff(seven_pattern, one_pattern)[0]

    # Next, we need to identify which patterns could be either 0 or 9
    
    zero_six_and_nine = [s for s in signal_patterns if len(s) == 6]
    six_pattern = [s for s in zero_six_and_nine if not _is_set_subset(one_pattern, s)][0]
    zero_and_nine = [s for s in zero_six_and_nine if _is_set_subset(one_pattern, s)]

    # 2) Determine right-top wire: 1 \ 6
    wires[2] = _set_diff(one_pattern, six_pattern)[0]

    # 3) Determine right-bottom wire: 6 \ 1
    wires[5] = _set_intersect(one_pattern, six_pattern)[0]

    # Next, we now need to obtain zero and 9
    top_left_and_middle_wire = _set_diff(four_pattern, one_pattern)
    if len(_set_diff(zero_and_nine[0], top_left_and_middle_wire)) == 5:
        zero_pattern = zero_and_nine[0]
        nine_pattern = zero_and_nine[1]
    else:
        zero_pattern = zero_and_nine[1]
        nine_pattern = zero_and_nine[0]

    # 4) Determine middle wire: 8 \ 0
    wires[3] = _set_diff(eight_pattern, zero_pattern)[0]

    # 5) Determine bottom-left wire: 8 \ 9
    wires[4] = _set_diff(eight_pattern, nine_pattern)[0]

    # 6) Determine top-left wire: left_and_middle_wire \ middle_wire
    wires[1] = _set_diff(top_left_and_middle_wire, [wires[3]])[0]

    # 7) Determine bottom wire: the last one
    wires[6] = _set_diff(eight_pattern, wires[:6])[0]

    return wires


def _infer_numbers(signal_patterns: List[str]) -> dict:
    wires = _infer_wires(signal_patterns)
    
    nums = {}
    # 0:
    nums[''.join(sorted([wires[0], wires[1], wires[2], wires[4], wires[5], wires[6]]))] = 0
    # 1:
    nums[''.join(sorted([wires[2], wires[5]]))] = 1
    # 2:
    nums[''.join(sorted([wires[0], wires[2], wires[3], wires[4], wires[6]]))] = 2
    # 3:
    nums[''.join(sorted([wires[0], wires[2], wires[3], wires[5], wires[6]]))] = 3
    # 4:
    nums[''.join(sorted([wires[1], wires[2], wires[3], wires[5]]))] = 4
    # 5:
    nums[''.join(sorted([wires[0], wires[1], wires[3], wires[5], wires[6]]))] = 5
    # 6:
    nums[''.join(sorted([wires[0], wires[1], wires[3], wires[4], wires[5], wires[6]]))] = 6
    # 7:
    nums[''.join(sorted([wires[0], wires[2], wires[5]]))] = 7
    # 8:
    nums[''.join(sorted([wires[0], wires[1], wires[2], wires[3], wires[4], wires[5], wires[6]]))] = 8
    # 9:
    nums[''.join(sorted([wires[0], wires[1], wires[2], wires[3], wires[5], wires[6]]))] = 9

    return nums

def solve2(signals: List[Signals]) -> int:
    out = 0

    for signal in signals:
        patterns_map = _infer_numbers(signal.get_signal_patterns())

        value = 0
        for output_val in signal.get_output_values():
            digit = patterns_map[output_val]
            value = value * 10 + digit
        out += value

    return out


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = _read_input(input_path)
    print(solve1(l))
    print(solve2(l))