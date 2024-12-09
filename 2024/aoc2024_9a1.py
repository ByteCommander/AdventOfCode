# Advent Of Code 2024, day 9, part 1, attempt 1
# http://adventofcode.com/2024/day/9
# solution by ByteCommander, 2024-12-09
from itertools import batched
from typing import TextIO, Iterable

from aoc_tools.lib import run


# This attempt uses a naive approach of simulating the whole disk as big array in memory, traversing it from both ends
# while moving individual blocks from right to left until both pointers meet in the middle.

def main(file: TextIO):
    sequences: Iterable[tuple[int, ...]] = batched(map(int, file.read().strip() + "0"), 2)
    disk: list[int | None] = []

    for i, (file_len, free_len) in enumerate(sequences):
        disk.extend([i] * file_len + [None] * free_len)
    # print(" ".join("." if b is None else str(b) for b in disk))

    i, j = 0, len(disk) - 1
    for i in range(len(disk)):
        if i >= j:
            break
        if disk[i] is None:
            while disk[j] is None and j > i:
                j -= 1
            disk[i] = disk[j]
            disk[j] = None
    # print(" ".join("." if b is None else str(b) for b in disk))

    checksum = sum([i * b for i, b in enumerate(disk[:disk.index(None, i - 1)])])
    print(f"The disk checksum after consolidating all file blocks is {checksum}. (simulation based)")


TEST_INPUT = """
2333133121414131402
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
