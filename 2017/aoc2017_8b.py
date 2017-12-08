# Advent Of Code 2017, day 8, part 2
# http://adventofcode.com/2017/day/8
# solution by ByteCommander, 2017-12-08

import re

with open("inputs/aoc2017_8.txt") as file:
    pattern = re.compile(r"(\w+) (inc|dec) (-?\d+) if (\w+) ([<>]=?|[=!]=) (-?\d+)")
    regs = {}
    largest = 0

    for line in file:
        match = pattern.fullmatch(line.strip())
        ax, incdec, n_, bx, cmp, m_ = match.groups()
        n, m = int(n_), int(m_)
        a, b = [regs.setdefault(rx, 0) for rx in (ax, bx)]

        if eval("{} {} {}".format(b, cmp, m)):
            if incdec == "inc":
                regs[ax] += n
            else:
                regs[ax] -= n
            largest = max(largest, regs[ax])

    print("Answer: the largest value ever was {}"
          .format(largest))
