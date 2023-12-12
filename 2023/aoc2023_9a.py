# Advent Of Code 2023, day 9, part 1
# http://adventofcode.com/2023/day/9
# solution by ByteCommander, 2023-12-13
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    total = 0
    for line in file:
        seq = list(map(int, line.split()))
        nxt = extrapolate(seq)
        # print(*seq, "->", nxt)
        total += nxt
    print(f"The sum of all extrapolated values is {total}.")


def extrapolate(seq: list[int]) -> int:
    # recurse down until all diffs are 0s, then build the sequences back up
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    if any(d != 0 for d in diffs):
        return seq[-1] + extrapolate(diffs)
    return seq[-1]


TEST_INPUT = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
