# Advent Of Code 2024, day 11, part 2
# http://adventofcode.com/2024/day/11
# solution by ByteCommander, 2024-12-16
from typing import TextIO

from aoc_tools.lib import run

BLINKS = 75

cache: dict[str, list[int]] = {}  # label -> number of stones it turns into after [1, ...] blinks


def main(file: TextIO):
    stones = file.read().strip().split()
    results = recurse(stones, BLINKS)
    # print(results)
    print(f"After blinking {BLINKS} times, there will be {results[-1]} stones.")


def recurse(stones: list[str], blinks: int) -> list[int]:
    if blinks == 0:
        return [len(stones)]
    # print((BLINKS - blinks) * "- ", stones[:100], len(stones) - 100 if len(stones) > 100 else "")
    results: list[list[int]] = []
    for s in stones:
        if s in cache and len(c := cache[s]) >= blinks:
            results.append(c[:blinks])
            # print("hit", blinks, s, c, c[:blinks])
        else:
            if s == "0":
                ns = ["1"]
            elif (l := len(s)) % 2 == 0:
                ns = [s[:l // 2], s[l // 2:].lstrip("0") or "0"]
            else:
                ns = [str(int(s) * 2024)]
            r = recurse(ns, blinks - 1)
            cache[s] = r
            # print(cache)
            results.append(r)
    next_stones = [len(stones), *map(sum, zip(*results))]
    return next_stones


TEST_INPUT = """
125 17
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
