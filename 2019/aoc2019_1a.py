# Advent Of Code 2019, day 1, part 1)
# http://adventofcode.com/2019/day/1
# solution by ByteCommander, 2019-12-01


def main():
    with open("inputs/aoc2019_1.txt") as file:
        fuel = sum(int(line) // 3 - 2 for line in file)

    print(f"The total fuel requirement is {fuel} units.")


if __name__ == "__main__":
    main()
