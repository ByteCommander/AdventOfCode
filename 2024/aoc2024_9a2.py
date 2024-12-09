# Advent Of Code 2024, day 9, part 1, attempt 2
# http://adventofcode.com/2024/day/9
# solution by ByteCommander, 2024-12-09
from itertools import batched
from typing import TextIO

from aoc_tools.lib import run


# This approach attempts to optimize memory consumption and time complexity by working with just the sequence lengths
# instead of simulating the actual disk contents. The checksum is computed on the fly while processing the sequence
# left to right, filling gaps by shortening the length of the last non-empty sequence item (tail).

def main(file: TextIO):
    sequences: list[tuple[int, ...]] = list(batched(map(int, file.read().strip()), 2))
    file_id, offset = 0, 0
    tail_len, tail_id = 0, len(sequences)
    checksum = 0
    # disk = []

    while file_id < tail_id:
        file_len, free_len = sequences[file_id]

        # process file blocks staying in place
        for _ in range(file_len):
            checksum += offset * file_id
            # disk.append(file_id)
            offset += 1
        file_id += 1

        # process file blocks relocated from the end of the disk
        for _ in range(free_len):
            if not tail_len:
                if tail_id <= file_id:  # no files left after current position, we're finished
                    break
                tail_id -= 1
                tail_len = sequences[tail_id][0]
            checksum += offset * tail_id
            tail_len -= 1
            # disk.append(tail_id)
            offset += 1

    # process rest of the chopped up tail file
    for offset in range(offset, offset + tail_len):
        checksum += offset * tail_id
        # disk.append(tail_id)

    # print(" ".join(map(str, disk)))
    print(f"The disk checksum after consolidating all file blocks is {checksum}. (sequence based)")


TEST_INPUT = """
2333133121414131402
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
