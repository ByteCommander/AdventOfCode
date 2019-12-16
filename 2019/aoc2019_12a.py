# Advent Of Code 2019, day 12, part 1)
# http://adventofcode.com/2019/day/12
# solution by ByteCommander, 2019-12-12
import itertools
import re


def main():
    with open("inputs/aoc2019_12.txt") as file:
        moons = [
            ([int(coord) for coord in re.fullmatch(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line.strip()).groups()],
             [0, 0, 0]) for line in file
        ]

    for step in range(1000):

        # apply gravity:
        for (pos1, vel1), (pos2, vel2) in itertools.combinations(moons, 2):
            for i in range(3):
                vel1[i] += 1 if pos2[i] > pos1[i] else -1 if pos2[i] < pos1[i] else 0
                vel2[i] += 1 if pos1[i] > pos2[i] else -1 if pos1[i] < pos2[i] else 0

        # apply velocity:
        for pos, vel in moons:
            for i in range(3):
                pos[i] += vel[i]

    energy = sum(sum(map(abs, pos)) * sum(map(abs, vel)) for pos, vel in moons)
    print(f"After {step + 1} steps, the total energy is {energy}.")


if __name__ == "__main__":
    main()
