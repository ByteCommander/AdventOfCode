# Advent Of Code 2017, day 4, part 1
# http://adventofcode.com/2017/day/4
# solution by ByteCommander, 2017-12-04

with open("inputs/aoc2017_4.txt") as file:
    counter = 0

    for line in file:
        words = line.split()
        if len(words) == len(set(words)):
            counter += 1

    print("Answer: List contains {} valid pass phrases."
          .format(counter))
