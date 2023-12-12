# Advent Of Code 2023, day 8, part 1
# http://adventofcode.com/2023/day/8
# solution by ByteCommander, 2023-12-12
import re
from itertools import cycle
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    instr = file.readline().strip()  # "sequence of L or R"
    file.readline()  # skip blank

    nodes: dict[str, (str, str)] = {}  # current -> (left, right)
    for line in file:
        node, left, right = re.fullmatch(r"(\w+) = \((\w+), (\w+)\)", line.strip()).groups()
        nodes[node] = (left, right)

    count, node = 0, "AAA"
    for step in cycle(instr):
        node = nodes[node][step == "R"]
        count += 1
        if node == "ZZZ":
            break

    print(f"You need {count} steps to reach the target.")


TEST_INPUT = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
