# Advent Of Code 2017, day 15, part 1
# http://adventofcode.com/2017/day/15
# solution by ByteCommander, 2017-12-15

CONST = 2147483647
BIN16 = 2 ** 16 - 1
PAIRS = 40000000
FACTA = 16807
FACTB = 48271


def generate(prev, factor):
    return (prev * factor) % CONST


def compare16(n1, n2):
    return n1 & BIN16 == n2 & BIN16


with open("inputs/aoc2017_15.txt") as file:
    a = int(file.readline().split()[-1])
    b = int(file.readline().split()[-1])

    counter = 0
    for i in range(PAIRS):
        a = generate(a, FACTA)
        b = generate(b, FACTB)
        comp = compare16(a, b)
        counter += comp

        if not i % 1000000: print(i//1000000, "/", 40)

    print("Answer: {} pairs share equal lower 16 bits."
          .format(counter))
