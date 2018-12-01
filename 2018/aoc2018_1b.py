# Advent Of Code 2018, day 1, part 2
# http://adventofcode.com/2018/day/1
# solution by ByteCommander, 2018-12-01

with open("inputs/aoc2018_1.txt") as file:
    freqs = set()
    diffs = [int(line) for line in file]

    f = 0
    while True:
        for d in diffs:
            f += d
            if f in freqs:
                break
            freqs.add(f)
        else:
            continue
        break

print(f"First duplicate frequency is {f}.")
