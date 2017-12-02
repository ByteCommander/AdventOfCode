# Advent Of Code 2017, day 2, part 1
# http://adventofcode.com/2017/day/2
# solution by ByteCommander, 2017-12-02

with open("inputs/aoc2017_2.txt") as file:
    checksum = 0
    for line in file:
        values = [int(x) for x in line.split()]
        print(values)
        checksum += max(values) - min(values)

    print("Answer: Checksum is {}"
          .format(checksum))
