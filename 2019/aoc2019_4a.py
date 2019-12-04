# Advent Of Code 2019, day 4, part 1)
# http://adventofcode.com/2019/day/4
# solution by ByteCommander, 2019-12-04

import re


def main():
    wires = []
    with open("inputs/aoc2019_4.txt") as file:
        a, b = map(int, file.read().split("-"))

    count = sum(
        1 for x in range(a, b + 1) if (
                re.search(r"(\d)\1", str(x)) and
                all(int(d1) <= int(d2) for d1, d2 in zip(str(x), str(x)[1:]))
        )
    )

    print(f"There are {count} possible passwords in the range.")


if __name__ == "__main__":
    main()
