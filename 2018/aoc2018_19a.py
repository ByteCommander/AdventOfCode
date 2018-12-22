# Advent Of Code 2018, day 19, part 1
# http://adventofcode.com/2018/day/19
# solution by ByteCommander, 2018-12-22

import re

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

instructions = []
with open("inputs/aoc2018_19.txt") as file:
    ip_reg = int(re.match(r"#ip (\d+)", file.readline()).group(1))
    for line in file:
        op, a_, b_, c_ = re.match(r"(\w+) (\d+) (\d+) (\d+)", line).groups()
        instructions.append((op, int(a_), int(b_), int(c_)))

register = [0] * 6
ip = 0
counter = 0
while ip < len(instructions):
    if counter % 1_000_000 == 0:
        print(f"\rSimulating {counter // 1_000_000}M instructions...", end="", flush=True)
    register[ip_reg] = ip
    op, in_a, in_b, out_c = instructions[ip]
    # print(f"ip={ip}", register, op, in_a, in_b, out_c, end=" ")
    register[out_c] = OPERATIONS[op](register, in_a, in_b)
    # print(register)
    ip = register[ip_reg] + 1
    counter += 1

print(f"\rThe final value in register[0] after {counter / 1_000_000:.1f}M "
      f"instructions is {register[0]}.")
