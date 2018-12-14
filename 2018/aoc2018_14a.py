# Advent Of Code 2018, day 14, part 1
# http://adventofcode.com/2018/day/14
# solution by ByteCommander, 2018-12-14

with open("inputs/aoc2018_14.txt") as file:
    num = int(file.read())

recipes = [3, 7]
elves = [0, 1]

while len(recipes) < num + 10:
    new = sum(recipes[elf] for elf in elves)
    recipes.extend(divmod(new, 10) if new >= 10 else [new])
    elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]

last10 = "".join(map(str, recipes[:num + 10][-10:]))
print(f"The last ten recipe scores will be {last10}.")
