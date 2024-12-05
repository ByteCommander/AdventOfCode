# Advent Of Code 2024, day 5, part 2
# http://adventofcode.com/2024/day/5
# solution by ByteCommander, 2024-12-05
from functools import cmp_to_key
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    rules: list[tuple[int, int]] = []
    updates: list[list[int]] = []
    for line in file:
        if line.strip():
            if "|" in line:
                first, second = line.split("|")
                rules.append((int(first), int(second)))
            else:
                updates.append([int(page) for page in line.split(",")])

    unordered: list[list[int]] = []
    for update in updates:
        for first, second in rules:
            if first in update and second in update and update.index(first) > update.index(second):
                unordered.append(update)
                break

    def cmp_by_rules(a: int, b: int) -> int:
        """Old style comparison function, returns 0 if a==b, 1 if a>b and -1 if a<b"""
        if a == b:
            return 0
        for fst, snd in rules:
            if a == fst and b == snd:
                return -1
            elif a == snd and b == fst:
                return 1
        return 0  # no ordering rule between them, so for sorting comparison treat them as equal

    result = 0
    for update in unordered:
        ordered = sorted(update, key=cmp_to_key(cmp_by_rules))
        result += ordered[len(ordered) // 2]

    print(f"The sum of all middle page numbers of now corrected update sequences is {result}.")


TEST_INPUT = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
