# Advent Of Code 2023, day 12, part 2
# http://adventofcode.com/2023/day/12
# solution by ByteCommander, 2023-12-15
from functools import cache
from re import match
from typing import TextIO

from aoc_tools.lib import run

GOOD = "."
BAD = "#"
UNKN = "?"


def main(file: TextIO):
    total = 0
    for line in file:
        record, _hints = line.split()
        # unfold the input *5
        record = UNKN.join([record] * 5)
        hints = tuple(map(int, _hints.split(","))) * 5

        valid_opts = recurse(record, hints)

        # print(record, "has", valid_opts, "valid options")
        total += valid_opts

    print(f"There are {total} possible arrangements in total in the unfolded records.")
    # print(recurse.cache_info())


@cache
def recurse(record: str, hints: tuple[int, ...]) -> int:
    if not hints:  # end of hints, record is only valid if it has no more bad fields
        return 1 if BAD not in record else 0

    # record is invalid if it has less bad/unknown fields than hints or is too short for all sequences and delimiters
    if (lr := len(record)) - record.count(GOOD) < (sh := sum(hints)) or lr < sh + len(hints) - 1:
        return 0

    record = record.lstrip(GOOD)  # skip known good fields
    count = 0
    if record[0] == UNKN:
        count += recurse(record[1:], hints)  # recurse with guessing the unknown field to be good (skipping it)

    # both if the field is known bad or unknown, try to fit the next hint sequence and recurse with the remainder
    if match(rf"[{BAD}{UNKN}]{{{hints[0]}}}(?!{BAD})", record):
        count += recurse(record[hints[0] + 1:], hints[1:])

    return count


TEST_INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
