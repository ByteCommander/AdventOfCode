# Advent Of Code 2024, day 9, part 2
# http://adventofcode.com/2024/day/9
# solution by ByteCommander, 2024-12-09
from itertools import batched
from typing import TextIO, Iterator

from aoc_tools.lib import run


def main(file: TextIO):
    sequences: Iterator[tuple[int, ...]] = batched(map(int, file.read().strip() + "0"), 2)
    file_spans: list[list[int]] = []  # [[offset, length, id], ...]
    gaps: list[list[int]] = []  # [[offset, length], ...]

    # separate file spans and gaps, compute all offsets and ids
    offset = 0
    for i, (file_len, free_len) in enumerate(sequences):
        file_spans.append([offset, file_len, i])
        offset += file_len
        if free_len:
            gaps.append([offset, free_len])
            offset += free_len

    # go through file spans from right to left, then search all remaining gaps left to right for the first one
    # which is big enough, and change the file offset to move it in there, while shrinking the gap accordingly
    for file_span in reversed(file_spans):
        file_offset, file_len, _file_id = file_span
        for gap in gaps:
            gap_offset, gap_len = gap
            if gap_offset > file_offset:  # never move a file to the right
                break
            if file_len <= gap_len:
                file_span[0] = gap_offset  # change file position value in-place in the spans list
                gap[0] = gap_offset + file_len  # increase gap start position and reduce size in-place accordingly
                gap[1] = gap_len - file_len
                break

    # visualization of linear disk space
    # disk: list[int | None] = []
    # offset = 0
    # for file_offset, file_len, file_id in sorted(file_spans):
    #     disk.extend([None] * (file_offset - offset) + [file_id] * file_len)
    #     offset = file_offset + file_len
    # print(" ".join("." if b is None else str(b) for b in disk))

    checksum = sum([o * fi for fo, fl, fi in file_spans for o in range(fo, fo + fl)])
    print(f"The disk checksum after defragmentation of all file blocks is {checksum}.")


TEST_INPUT = """
2333133121414131402
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
