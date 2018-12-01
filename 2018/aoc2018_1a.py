# Advent Of Code 2018, day 1, part 1
# http://adventofcode.com/2018/day/1
# solution by ByteCommander, 2018-12-01

with open("inputs/aoc2018_1.txt") as file:
    f = sum(int(line) for line in file)

print(f"The final frequency is {f}.")
