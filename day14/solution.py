import sys
from typing import Tuple


def read_input(path: str) -> Tuple[str, dict]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    
    polymer_template = file_content[0][:-1]
    pair_insertion_rules = {}
    for rule in file_content[2:]:
        rule = rule[:-1].split(" -> ")
        assert len(rule[0]) == 2 and len(rule[1]) == 1
        pair_insertion_rules[rule[0]] = rule[1]

    return polymer_template, pair_insertion_rules


def _simulate_and_diff(steps: int, polymer_template: str, pair_insertion_rules: dict) -> int:
    pairs = {}
    for i in range(len(polymer_template) - 1):
        pair = polymer_template[i:i+2]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1

    for _ in range(steps):
        new_pairs = {}
        for pair in pairs:
            assert pair in pair_insertion_rules
            new_p = pair_insertion_rules[pair]
            
            new_pair1 = f"{pair[0]}{new_p}"
            if new_pair1 in new_pairs:
                new_pairs[new_pair1] += pairs[pair]
            else:
                new_pairs[new_pair1] = pairs[pair]
            
            new_pair2 = f"{new_p}{pair[1]}"
            if new_pair2 in new_pairs:
                new_pairs[new_pair2] += pairs[pair]
            else:
                new_pairs[new_pair2] = pairs[pair]

        pairs = new_pairs

    cnts = {}
    for pair in pairs:
        c1, c2 = pair[0], pair[1]
        if c1 in cnts:
            cnts[c1] += pairs[pair]
        else:
            cnts[c1] = pairs[pair]

        if c2 in cnts:
            cnts[c2] += pairs[pair]
        else:
            cnts[c2] = pairs[pair]

    for key in cnts:
        if key == polymer_template[0] or key == polymer_template[-1]:
            cnts[key] = (cnts[key] + 1) // 2
        else:
            cnts[key] = cnts[key] // 2

    max_cnt_key = max(cnts, key=cnts.get)
    min_cnt_key = min(cnts, key=cnts.get)
    
    return cnts[max_cnt_key] - cnts[min_cnt_key]


def solve1(polymer_template: str, pair_insertion_rules: dict) -> int:
    return _simulate_and_diff(10, polymer_template, pair_insertion_rules)


def solve2(polymer_template: str, pair_insertion_rules: dict) -> int:
    return _simulate_and_diff(40, polymer_template, pair_insertion_rules)


if __name__ == "__main__":
    input_path = sys.argv[1]
    polymer_template, pair_insertion_rules = read_input(input_path)
    print(solve1(polymer_template, pair_insertion_rules))
    print(solve2(polymer_template, pair_insertion_rules))