# Advent Of Code 2017, day 15, part 2
# http://adventofcode.com/2017/day/15
# solution by ByteCommander, 2017-12-15

CONST = 2147483647
BIN16 = 2 ** 16 - 1
PAIRS = 5000000
FACTA = 16807
FACTB = 48271
CRITA = 4
CRITB = 8


def generate(prev, factor, criteria):
    while True:
        r = (prev * factor) % CONST
        if r % criteria:
            prev = r
        else:
            return r


def compare16(n1, n2):
    return n1 & BIN16 == n2 & BIN16


with open("inputs/aoc2017_15.txt") as file:
    a = int(file.readline().split()[-1])
    b = int(file.readline().split()[-1])

    counter = 0
    for i in range(PAIRS):
        a = generate(a, FACTA, CRITA)
        b = generate(b, FACTB, CRITB)
        comp = compare16(a, b)
        counter += comp

        if not i % 100000: print(i / 1000000, "/", 5)

    print("Answer: {} pairs share equal lower 16 bits."
          .format(counter))
