import os
import sys
from typing import List, Tuple, Callable
import copy


def read_input(path: str) -> List[List[bool]]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return list(map(lambda l:list( map(lambda bit: bit == '1', l[:-1])), file_content))


def _calculate_bit_distributions(l: List[List[bool]]) -> Tuple[List[int], List[int]]:
    bit_length = len(l[0])

    one_counts = [0 for _ in range(bit_length)]
    zero_counts = [0 for _ in range(bit_length)]

    for num in l:
        for i in range(bit_length):
            if num[i]:
                one_counts[i] += 1
            else:
                zero_counts[i] += 1

    return one_counts, zero_counts


def solve1(l: List[List[bool]]):
    one_counts, zero_counts = _calculate_bit_distributions(l)

    # Construct gamma and epsilon rate
    gamma_rate = 0
    epsilon_rate = 0

    bit_length = len(l[0])
    for i in range(bit_length):
        assert one_counts[i] != zero_counts[i]
        if one_counts[i] > zero_counts[i]:
            gamma_rate = (gamma_rate << 1) | 1
            epsilon_rate <<= 1
        else:
            gamma_rate <<= 1
            epsilon_rate = (epsilon_rate << 1) | 1

    return gamma_rate * epsilon_rate


def search(l: List[List[bool]], bit_criteria: Callable) -> List[bool]:
    bit_length = len(l[0])

    for i in range(bit_length):
        if len(l) == 1:
            break

        one_counts, zero_counts = _calculate_bit_distributions(l)

        keep_bit = bit_criteria(i, one_counts, zero_counts)
        l = list(filter(lambda num: num[i] == keep_bit, l))

    assert len(l) == 1
    target_num = l[0]

    out_num = 0
    for i in range(bit_length):
        out_num <<= 1
        if target_num[i]:
            out_num |= 1

    return out_num


def solve2(l: List[List[bool]]):
    # Search for the oxygen generator rating
    def bit_criteria_oxygen(i: int, one_counts: List[int], zero_counts: List[int]) -> bool:
        return one_counts[i] >= zero_counts[i]
    oxygen_gen_rating = search(copy.deepcopy(l), bit_criteria_oxygen)

    # Search for the CO2 scrubber rating
    def bit_criteria_co2(i: int, one_counts: List[int], zero_counts: List[int]) -> bool:
        return one_counts[i] < zero_counts[i]
    co2_scrubber_rating = search(copy.deepcopy(l), bit_criteria_co2)

    return oxygen_gen_rating * co2_scrubber_rating


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = read_input(input_path)
    print(solve1(l))
    print(solve2(l))
