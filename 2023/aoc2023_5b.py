# Advent Of Code 2023, day 5, part 2
# http://adventofcode.com/2023/day/5
# solution by ByteCommander, 2023-12-12
from _operator import itemgetter
from bisect import bisect, insort
from itertools import batched
from operator import itemgetter
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    # seed values in format [(range start, range length), ...]
    ranges: list[(int, int)] = list(batched(map(int, file.readline().split(":")[-1].strip().split()), 2))
    maps: list[GardenMap] = []

    for line in file:
        if "map" in line:
            maps.append(GardenMap(line.split()[0]))
        elif line.strip():
            maps[-1].remap(*map(int, line.split()))

    # for m in maps: print(m.name, m.ranges); print()

    for m in maps:
        dest_ranges: list[(int, int)] = []
        for range_start, range_length in ranges:
            dest_ranges.extend(m.translate(range_start, range_length))
        # print("Ranges after", m.name, dest_ranges)
        ranges = dest_ranges

    closest = min(map(itemgetter(0), ranges))
    print(f"The closest location of any seed is {closest}.")


class GardenMap:
    def __init__(self, name: str):
        self.name = name
        self.ranges: list[list[int]] = [[0, 0]]  # source range start (sorted!), target offset

    def remap(self, dst_start: int, src_start: int, length: int):
        src_end = src_start + length
        old_left_range = self.ranges[bisect(self.ranges, src_start, key=itemgetter(0)) - 1]
        old_right_range_start, old_right_offset = self.ranges[bisect(self.ranges, src_end, key=itemgetter(0)) - 1]

        if old_left_range[0] == src_start:  # overwrite older range starts (should be offset 0 ranges only?)
            old_left_range[1] = dst_start - src_start
        else:
            insort(self.ranges, [src_start, dst_start - src_start], key=itemgetter(0))

        if old_right_range_start < src_end:  # create new range after end with old offset, unless there is a border
            insort(self.ranges, [src_end, old_right_offset], key=itemgetter(0))
        # print("remap", self.name, dst_start, src_start, length, "->", self.ranges)

    def translate(self, src_start: int, src_len: int) -> list[list[int]]:
        """
        :param src_start:
        :param src_len:
        :return: list of continuous mapped range partitions [(dst_start, length), ...]
        """
        x = src_start + src_len - 1
        mappings: list[list[int]] = []
        while x > src_start:
            whole_range_start, offset = self.ranges[bisect(self.ranges, x, key=itemgetter(0)) - 1]
            range_start: int = max(whole_range_start, src_start)
            dest_start: int = range_start + offset
            range_len = x - range_start + 1
            mappings.append([dest_start, range_len])
            x = range_start - 1
        mappings.reverse()
        # print(f"{self.name} {src_start}-{src_start + src_len} ({src_len}) -> {mappings}")
        return mappings


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
