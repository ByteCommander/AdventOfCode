# Advent Of Code 2024, day 11, part 1
# http://adventofcode.com/2024/day/11
# solution by ByteCommander, 2024-12-11
from typing import TextIO

from aoc_tools.lib import run

BLINKS = 25


def main(file: TextIO):
    stones = file.read().strip().split()

    for _ in range(BLINKS):
        next_stones = []
        for s in stones:
            if s == '0':
                next_stones.append('1')
            elif (l := len(s)) % 2 == 0:
                next_stones.extend([s[:l // 2], s[l // 2:].lstrip("0") or "0"])
            else:
                next_stones.append(str(int(s) * 2024))
        stones = next_stones

    print(f"After blinking {BLINKS} times, there will be {len(stones)} stones.")


TEST_INPUT = """
125 17
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
