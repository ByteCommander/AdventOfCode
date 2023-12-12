# Advent Of Code 2023, day 8, part 2
# http://adventofcode.com/2023/day/8
# solution by ByteCommander, 2023-12-12
import re
from itertools import cycle
from math import lcm
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    instr = file.readline().strip()  # "sequence of L or R"
    file.readline()  # skip blank

    nodes: dict[str, (str, str)] = {}  # current -> (left, right)
    for line in file:
        node, left, right = re.fullmatch(r"(\w+) = \((\w+), (\w+)\)", line.strip()).groups()
        nodes[node] = (left, right)

    # Assumptions: all ghosts follow a route that is basically a cycle. The first few steps are not repeated,
    # but "parallel" to steps inside the cycle, so that we can act as if we start each route on the "target" field
    # and just have to find the full distance between two states with all routes being back to the start.

    # Determine cycles and ends for each ghost.
    # Apart from the example, it would have been sufficient to just find the end state and assume it equals the
    # cycle length. In the example, the cycle length is not a multiple of the instruction length though.
    cycle_lengths = []
    for initial_node in nodes.keys():
        if not initial_node.endswith("A"):
            continue

        index, node = 0, initial_node
        seen: set[(int, str)] = {(index % len(instr), node)}

        for step in cycle(instr):
            node = nodes[node][step == "R"]
            index += 1
            current = (index % len(instr), node)

            # if node.endswith("Z"):
            #     print(ghost, "has potential end at", index, node)
            if current in seen:
                break
            seen.add(current)

        cycle_start = index % len(instr)
        cycle_len = index - cycle_start
        # print(f"{initial_node}: cycle length {cycle_len} from {cycle_start}-{index}")
        cycle_lengths.append(cycle_len)

    # Since we assume that the start constellation is equivalent to every cycle being at the target position,
    # we just need the lowest common multiple of all cycle lengths to find the next target constellation.

    solution = lcm(*cycle_lengths)

    print(f"All ghosts reach a target node simultaneously after {solution} steps.")


TEST_INPUT = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
