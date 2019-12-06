# Advent Of Code 2019, day 6, part 1)
# http://adventofcode.com/2019/day/6
# solution by ByteCommander, 2019-12-06


def main():
    with open("inputs/aoc2019_6.txt") as file:
        lines = [line.strip().split(")") for line in file]
        direct = {sat: cen for cen, sat in lines}

    indirect = {}
    for sat, cen in direct.items():
        centers = indirect[sat] = set()
        while cen:
            centers.add(cen)
            sat, cen = cen, direct.get(cen)

    # print(*indirect.items(), sep="\n")
    total_orbits = sum(len(centers) for centers in indirect.values())
    print(f"There are {total_orbits} direct and indirect orbits in total.")


if __name__ == "__main__":
    main()
