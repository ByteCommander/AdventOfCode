# Advent Of Code 2018, day 5, part 2
# http://adventofcode.com/2018/day/5
# solution by ByteCommander, 2018-12-05

from collections import deque
from string import ascii_lowercase

with open("inputs/aoc2018_5.txt") as file:
    whole_molecule = file.read().strip()

shortest = len(whole_molecule)

for blocker in ascii_lowercase:
    molecule = deque(whole_molecule.replace(blocker, "").replace(blocker.upper(), ""))

    result = []
    while molecule:
        if not result:
            result.append(molecule.popleft())
        unit = molecule.popleft() if molecule else ""

        if unit.swapcase() == result[-1]:
            result.pop()
        else:
            result.append(unit)

    shortest = min(shortest, len(result))

print(f"The shortest fully reacted molecule after removing one type is {shortest} units long.")
