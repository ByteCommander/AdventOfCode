# Advent Of Code 2023, day 15, part 1
# http://adventofcode.com/2023/day/15
# solution by ByteCommander, 2023-12-16
from functools import reduce
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    hash_sum = 0
    for step in file.read().strip().split(","):
        step_hash = reduce(lambda n, ch: ((n + ord(ch)) * 17) % 256, step, 0)
        # print(step, step_hash)
        hash_sum += step_hash

    print(f"The sum of all hashes of each step is {hash_sum}.")


TEST_INPUT = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
