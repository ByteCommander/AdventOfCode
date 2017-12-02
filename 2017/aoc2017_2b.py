# Advent Of Code 2017, day 2, part 2
# http://adventofcode.com/2017/day/2
# solution by ByteCommander, 2017-12-02


def find_divisibles(values):
    for a in values:
        for b in values:
            if a > b and a % b == 0:
                return a // b


with open("inputs/aoc2017_2.txt") as file:
    checksum = 0
    for line in file:
        vals = [int(x) for x in line.split()]
        checksum += find_divisibles(vals)

    print("Answer: Checksum is {}"
          .format(checksum))
