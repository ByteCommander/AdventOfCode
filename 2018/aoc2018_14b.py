# Advent Of Code 2018, day 14, part 2
# http://adventofcode.com/2018/day/14
# solution by ByteCommander, 2018-12-14

from collections import deque

with open("inputs/aoc2018_14.txt") as file:
    numbers = deque(map(int, file.read().strip()))

recipes = [3, 7]
last_recipes = deque(recipes, maxlen=len(numbers))
elves = [0, 1]

print("Warning: expected runtime around 2:30 minutes...")

while True:
    new = sum(recipes[elf] for elf in elves)
    new_recipes = divmod(new, 10) if new >= 10 else [new]
    for r in new_recipes:
        recipes.append(r)
        last_recipes.append(r)
        if last_recipes == numbers:
            break
    else:
        elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]
        continue
    break

print(f"The elves will generate {len(recipes) - len(last_recipes)} recipes before the specified sequence.")
