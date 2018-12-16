# Advent Of Code 2018, day 16, part 2
# http://adventofcode.com/2018/day/16
# solution by ByteCommander, 2018-12-16

import re

SAMPLE_PATTERN = re.compile(
    r"^Before: +\[(\d+), (\d+), (\d+), (\d+)\]\n"
    r"^(\d+) (\d+) (\d+) (\d+)\n"
    r"^After: +\[(\d+), (\d+), (\d+), (\d+)\]\n",
    re.MULTILINE
)
PROGRAM_PATTERN = re.compile(
    r"^(\d+) (\d+) (\d+) (\d+)$",
    re.MULTILINE
)

OPERATIONS = {
    "addr": lambda reg, a, b: reg[a] + reg[b],
    "addi": lambda reg, a, b: reg[a] + b,
    "mulr": lambda reg, a, b: reg[a] * reg[b],
    "muli": lambda reg, a, b: reg[a] * b,
    "banr": lambda reg, a, b: reg[a] & reg[b],
    "bani": lambda reg, a, b: reg[a] | b,
    "borr": lambda reg, a, b: reg[a] | reg[b],
    "bori": lambda reg, a, b: reg[a] & b,
    "setr": lambda reg, a, b: reg[a],
    "seti": lambda reg, a, b: a,
    "gtir": lambda reg, a, b: (a > reg[b]),
    "gtri": lambda reg, a, b: (reg[a] > b),
    "gtrr": lambda reg, a, b: (reg[a] > reg[b]),
    "eqir": lambda reg, a, b: (a == reg[b]),
    "eqri": lambda reg, a, b: (reg[a] == b),
    "eqrr": lambda reg, a, b: (reg[a] == reg[b])
}

with open("inputs/aoc2018_16.txt") as file:
    samples, program = file.read().split("\n\n\n")

# find all possible opname candidates for each opcode
candidates = {}
for match in SAMPLE_PATTERN.finditer(samples):
    b0, b1, b2, b3, opcode, in_a, in_b, out_c, a0, a1, a2, a3 = map(int, match.groups())

    names = [
        opname for opname, check in OPERATIONS.items()
        if (a0, a1, a2, a3)[out_c] == check((b0, b1, b2, b3), in_a, in_b)
    ]

    candidates.setdefault(opcode, set(names)).intersection_update(names)

# resolve all opcodes to a distinct opname
opnames = {}
while candidates:
    opcode, opname = next(
        (code, *names) for code, names in candidates.items() if len(names) == 1
    )
    candidates.pop(opcode)
    opnames[opcode] = opname

    for names in candidates.values():
        names.discard(opname)

# execute program
register = [0] * 4
for match in PROGRAM_PATTERN.finditer(program):
    opcode, in_a, in_b, out_c = map(int, match.groups())

    operation = OPERATIONS[opnames[opcode]]
    register[out_c] = operation(register, in_a, in_b)

print(f"After all program instructions, the register contents are {register}.")
