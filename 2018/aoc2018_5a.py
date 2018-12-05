# Advent Of Code 2018, day 5, part 1
# http://adventofcode.com/2018/day/5
# solution by ByteCommander, 2018-12-05

from collections import deque

with open("inputs/aoc2018_5.txt") as file:
    molecule = deque(file.read().strip())

result = []

while molecule:
    if not result:
        result.append(molecule.popleft())
    unit = molecule.popleft() if molecule else ""

    if unit.swapcase() == result[-1]:
        result.pop()
    else:
        result.append(unit)

print(f"After the reaction, the polymer is still {len(result)} units long.")
