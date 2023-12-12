# Advent Of Code 2023, day 5, part 1
# http://adventofcode.com/2023/day/5
# solution by ByteCommander, 2023-12-12
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    seeds = list(map(int, file.readline().split(":")[-1].strip().split()))
    maps: list[GardenMap] = []

    for line in file:
        if "map" in line:
            maps.append(GardenMap(line.split()[0]))
        elif line.strip():
            maps[-1].remap(tuple(map(int, line.split())))

    closest: int = 0
    for seed in seeds:
        val = seed
        for m in maps:
            val = m.find(val)
        # print(f"Seed {seed} is in location {val}.")
        closest = min(closest, val) if closest else val

    print(f"The closest location of any seed is {closest}.")


class GardenMap:
    def __init__(self, name: str):
        self.name = name
        self.ranges: list[tuple[int, int, int]] = []  # destination start, source start, range length

    def remap(self, map_range: tuple[int, int, int]):
        self.ranges.append(map_range)

    def find(self, x: int) -> int:
        target = x
        for dst, src, rlen in self.ranges:
            if src <= x < src + rlen:
                target = dst + x - src
                break
        # print(self.name, x, target)
        return target


TEST_INPUT = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
