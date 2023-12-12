# Advent Of Code 2023, day 6, part 1
# http://adventofcode.com/2023/day/6
# solution by ByteCommander, 2023-12-12
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    _times = map(int, file.readline().split()[1:])
    _dists = map(int, file.readline().split()[1:])
    races = list(zip(_times, _dists))

    wins_product = 1
    for rtime, rdist in races:
        wins_product *= sum(1 for t in range(1, rtime) if t * (rtime - t) > rdist)

    print(f"The product of the number of winning configurations per race is {wins_product}.")


TEST_INPUT = """
Time:      7  15   30
Distance:  9  40  200
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
