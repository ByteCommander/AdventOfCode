# Advent Of Code 2019, day 1, part 2)
# http://adventofcode.com/2019/day/1
# solution by ByteCommander, 2019-12-01


def main():
    fuel = 0
    with open("inputs/aoc2019_1.txt") as file:
        for line in file:
            mass = int(line)
            while mass:
                mass = max(mass // 3 - 2, 0)
                fuel += mass

    print(f"The total fuel requirement is {fuel} units.")


if __name__ == "__main__":
    main()
