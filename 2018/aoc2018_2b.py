# Advent Of Code 2018, day 2, part 2
# http://adventofcode.com/2018/day/2
# solution by ByteCommander, 2018-12-02

with open("inputs/aoc2018_2.txt") as file:
    lines = [line.strip() for line in file]

    for i, line in enumerate(lines):
        for other in lines[i+1:]:
            if sum(c1 != c2 for c1, c2 in zip(line, other)) == 1:
                break
        else:
            continue
        break

    common = "".join((c1 if c1 == c2 else "") for c1, c2 in zip(line, other))


print(f"The common ID part is {common}.")
