# Advent Of Code 2019, day 12, part 2)
# http://adventofcode.com/2019/day/12
# solution by ByteCommander, 2019-12-16
import itertools
import math
import re
from concurrent.futures.process import ProcessPoolExecutor
from functools import reduce


def main():
    with open("inputs/aoc2019_12.txt") as file:
        moons = [
            [[int(coord), 0] for coord in re.fullmatch(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line.strip()).groups()]
            for line in file
        ]

    with ProcessPoolExecutor() as pool:
        loops = pool.map(find_loop, zip(*moons))

    total = lcm(*loops)
    print(f"After {total} steps, the constellation looks like its initial state again.")


def find_loop(axis):
    step = 0
    hist = {tuple(x for pv in axis for x in pv): step}

    while True:
        # apply gravity to velocity:
        for pv1, pv2 in itertools.combinations(axis, 2):
            pv1[1] += 1 if pv2[0] > pv1[0] else -1 if pv2[0] < pv1[0] else 0
            pv2[1] += 1 if pv1[0] > pv2[0] else -1 if pv1[0] < pv2[0] else 0

        # apply velocity to position:
        for pv in axis:
            pv[0] += pv[1]

        step += 1
        now = tuple(x for pv in axis for x in pv)
        # print(now)
        if now in hist:
            return step  # , hist[now]  # we seem to always loop back to step 0, so no offset required
        hist[now] = step


def lcm(*args):  # lowest common multiple
    return reduce(lambda a, b: a * b // math.gcd(a, b), args)


if __name__ == "__main__":
    main()
