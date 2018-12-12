# Advent Of Code 2018, day 12, part 1
# http://adventofcode.com/2018/day/12
# solution by ByteCommander, 2018-12-12

import re

rules = set()
with open("inputs/aoc2018_12.txt") as file:
    state = re.match(r"initial state: ([#.]+)", file.readline()).group(1)
    for line in file:
        match = re.match(r"([#.]{5}) => #", line)
        if match:
            rules.add(match.group(1))

offset = 0
for i in range(20):
    print(i, offset, state, sep="\t")

    prev_length = len(state)
    padded_state = "...." + state + "...."

    state = "".join(
        ".#"[padded_state[current_pot:current_pot + 5] in rules]
        for current_pot in range(prev_length + 4)
    )

    state = state.lstrip(".")
    offset -= len(state) - 2 - prev_length
    state = state.rstrip(".")

print(i + 1, offset, state, sep="\t")

result = sum(index for index, pot in enumerate(state, offset) if pot == "#")
print(f"The resulting sum of occupied pot indexes is {result}.")
