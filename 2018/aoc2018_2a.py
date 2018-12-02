# Advent Of Code 2018, day 2, part 1
# http://adventofcode.com/2018/day/2
# solution by ByteCommander, 2018-12-02

from collections import Counter

with open("inputs/aoc2018_2.txt") as file:
    counters = [Counter(line) for line in file]

    count2 = 0
    count3 = 0
    for counter in counters:
        count2 += 2 in counter.values()
        count3 += 3 in counter.values()

    checksum = count2 * count3

print(f"The checksum is {checksum}.")
