# Advent Of Code 2017, day 1, part 1
# http://adventofcode.com/2017/day/1
# solution by ByteCommander, 2017-12-01

with open("inputs/aoc2017_1.txt") as file:
    s = file.read().strip()
    m = len(s) // 2
    print(sum(int(c) for c, n in zip(s, s[m:] + s[:m]) if c == n))
