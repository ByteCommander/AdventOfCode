# Advent Of Code 2018, day 12, part 2
# http://adventofcode.com/2018/day/12
# solution by ByteCommander, 2018-12-12

import re
from collections import OrderedDict
from itertools import islice

TARGET = 50_000_000_000

rules = set()
with open("inputs/aoc2018_12.txt") as file:
    state = re.match(r"initial state: ([#.]+)", file.readline()).group(1)
    for line in file:
        match = re.match(r"([#.]{5}) => #", line)
        if match:
            rules.add(match.group(1))

offset = 0
state_history = OrderedDict()
for i in range(TARGET):
    print(i, offset, state, sep="\t")
    state_history[state] = (i, offset)

    prev_length, prev_offset = len(state), offset
    padded_state = "...." + state + "...."

    state = "".join(
        ".#"[padded_state[current_pot:current_pot + 5] in rules]
        for current_pot in range(prev_length + 4)
    )

    state = state.lstrip(".")
    offset -= len(state) - 2 - prev_length
    state = state.rstrip(".")

    if state in state_history:
        loop_start, old_offset = state_history[state]
        offset_diff = offset - old_offset

        history_index = (TARGET - i) % (i - loop_start + 1) + loop_start
        repeats = (TARGET - i) // (i - loop_start + 1)

        offset = prev_offset + repeats * offset_diff
        state = next(islice(state_history, history_index, None))  # nth element from iterable

        print(f"\nRepetition detected: same pattern as step {loop_start}, "
              f"loop length {i - loop_start}, offset difference {offset_diff}, "
              f"skipping {repeats} loops\n")
        break

print(TARGET, offset, state, sep="\t")

result = sum(index for index, pot in enumerate(state, offset) if pot == "#")
print(f"\nThe resulting sum of occupied pot indexes is {result}.")
