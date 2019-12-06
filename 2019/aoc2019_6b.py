# Advent Of Code 2019, day 6, part 2)
# http://adventofcode.com/2019/day/6
# solution by ByteCommander, 2019-12-06


def main():
    with open("inputs/aoc2019_6.txt") as file:
        lines = [line.strip().split(")") for line in file]
        direct = {sat: cen for cen, sat in lines}

    orbits = {}
    for sat, cen in direct.items():
        centers = orbits[sat] = []
        while cen:
            centers.append(cen)
            sat, cen = cen, direct.get(cen)

    you, san = list(orbits["YOU"]), list(orbits["SAN"])
    while you[-1] == san[-1]:
        you, san = you[:-1], san[:-1]

    print(f"There are {len(you) + len(san)} orbit transfers needed.")


if __name__ == "__main__":
    main()
