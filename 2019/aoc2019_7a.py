# Advent Of Code 2019, day 7, part 1)
# http://adventofcode.com/2019/day/7
# solution by ByteCommander, 2019-12-07
import itertools


def main():
    with open("inputs/aoc2019_7.txt") as file:
        mem = [int(x) for x in file.read().split(",")] + [None] * 3

    signal = (0, (None,))
    for phases in itertools.permutations(range(5)):
        value = 0
        for phase in phases:
            value = run(mem, (phase, value))
        signal = max(signal, (value, phases))

    print(f"Maximum signal is {signal[0]} for phase sequence {signal[1]}.")


def run(memory, inputs):
    mem = list(memory)  # copy
    inp = iter(inputs)
    i = 0

    while True:
        mod_op, ax, bx, cx = mem[i:i + 4]
        modes, op = divmod(mod_op, 100)
        cm, bm, am = map(int, f"{modes:03.0f}")

        if op == 1:  # add
            mem[cx] = read(mem, ax, am) + read(mem, bx, bm)
            i += 4
        elif op == 2:  # multiply
            mem[cx] = read(mem, ax, am) * read(mem, bx, bm)
            i += 4
        elif op == 3:  # input
            mem[ax] = next(inp)
            i += 2
        elif op == 4:  # output
            output = read(mem, ax, am)
            # print(f"{output=} for {inputs=}")
            # i += 2
            return output  # assuming single output, terminating prematurely
        elif op == 5:  # jump-if-true
            i = read(mem, bx, bm) if read(mem, ax, am) else i + 3
        elif op == 6:  # jump-if-false
            i = read(mem, bx, bm) if not read(mem, ax, am) else i + 3
        elif op == 7:  # less-than
            mem[cx] = int(read(mem, ax, am) < read(mem, bx, bm))
            i += 4
        elif op == 8:  # equals
            mem[cx] = int(read(mem, ax, am) == read(mem, bx, bm))
            i += 4
        elif op == 99:
            break
        else:
            raise RuntimeError(f"Illegal opcode at {i=}: {mem[i]}")


def read(mem, xx, mode=0):
    if mode == 0:
        return mem[xx]
    elif mode == 1:
        return xx
    else:
        raise RuntimeError(f"Illegal arg mode {mode}")


if __name__ == "__main__":
    main()
