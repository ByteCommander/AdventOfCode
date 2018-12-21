# Advent Of Code 2018, day 18, part 2
# http://adventofcode.com/2018/day/18
# solution by ByteCommander, 2018-12-21

from collections import Counter
from functools import reduce
from itertools import chain, repeat
from operator import mul

MINUTES = 1_000_000_000

world = []

with open("inputs/aoc2018_18.txt") as file:
    for line in file:
        world.append([".|#".index(field) + 1 for field in line.strip()])
    WIDTH = len(world[0])

history = []

for minute in range(MINUTES):
    if minute % 10 == 0:
        print(".", end="", flush=True)

    environments = zip(
        chain(repeat(1, WIDTH), *([1] + row[:-1] for row in world[:-1])),
        chain(repeat(1, WIDTH), *world[:-1]),
        chain(repeat(1, WIDTH), *(row[1:] + [1] for row in world[:-1])),
        chain(*([1] + row[:-1] for row in world)),
        chain(*(row[1:] + [1] for row in world)),
        chain(*([1] + row[:-1] for row in world[1:]), repeat(1, WIDTH)),
        chain(*world[1:], repeat(1, WIDTH)),
        chain(*(row[1:] + [1] for row in world[1:]), repeat(1, WIDTH)),
    )

    new_area = []
    for y, row in enumerate(world):
        new_row = []
        new_area.append(new_row)
        for x, field in enumerate(row):
            env = reduce(mul, next(environments))
            if field == 1:  # is "." and has 3 or more "|" --> becomes "|"
                new_row.append(2 if env % 8 == 0 else field)
            elif field == 2:  # is "|" and has 3 or more "#" --> becomes "#"
                new_row.append(3 if env % 27 == 0 else field)
            elif field == 3:  # is "#" and has NOT at least one "|" and "#" --> becomes "."
                new_row.append(1 if env % 6 != 0 else field)

    world = new_area

    if world in history:
        loop_start = history.index(world)
        final_index = (MINUTES - minute - 1) % (minute - loop_start) + loop_start
        print(f"\rRepeated pattern detected ({loop_start} - {minute} minutes).\n")
        world = history[final_index]
        break

    history.append(world)

print("Final world:")
print(*["".join("?.|#"[field] for field in row) for row in world], sep="\n")

counter = Counter(chain(*world))
print(f"\nThe total resource value after {MINUTES} minutes is {counter[2] * counter[3]}.")
