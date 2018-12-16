# Advent Of Code 2018, day 16, part 1
# http://adventofcode.com/2018/day/16
# solution by ByteCommander, 2018-12-16

import re

PATTERN = re.compile(
    r"^Before: +\[(\d+), (\d+), (\d+), (\d+)\]\n"
    r"^(\d+) (\d+) (\d+) (\d+)\n"
    r"^After: +\[(\d+), (\d+), (\d+), (\d+)\]\n",
    re.MULTILINE
)


def try_all_ops(reg, a, b, c, reg_after):
    result = reg_after[c]

    operation_checks = {
        "addr": result == reg[a] + reg[b],
        "addi": result == reg[a] + b,
        "mulr": result == reg[a] * reg[b],
        "muli": result == reg[a] * b,
        "banr": result == reg[a] & reg[b],
        "bani": result == reg[a] | b,
        "borr": result == reg[a] | reg[b],
        "bori": result == reg[a] & b,
        "setr": result == reg[a],
        "seti": result == a,
        "gtir": result == (a > reg[b]),
        "gtri": result == (reg[a] > b),
        "gtrr": result == (reg[a] > reg[b]),
        "eqir": result == (a == reg[b]),
        "eqri": result == (reg[a] == b),
        "eqrr": result == (reg[a] == reg[b])
    }

    return sum(operation_checks.values())


with open("inputs/aoc2018_16.txt") as file:
    matches = PATTERN.finditer(file.read())

counter = 0
for match in matches:
    (
        before0, before1, before2, before3,
        opcode, in_a, in_b, out_c,
        after0, after1, after2, after3
    ) = map(int, match.groups())

    counter += try_all_ops(
        (before0, before1, before2, before3),
        in_a, in_b, out_c,
        (after0, after1, after2, after3)
    ) >= 3

print(f"There are {counter} samples that would match 3 or more operations.")
