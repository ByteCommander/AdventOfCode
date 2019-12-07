# Advent Of Code 2019, day 7, part 2)
# http://adventofcode.com/2019/day/7
# solution by ByteCommander, 2019-12-07

import asyncio
import itertools
from asyncio.queues import Queue


async def main():
    with open("inputs/aoc2019_7.txt") as file:
        mem = [int(x) for x in file.read().split(",")] + [None] * 3

    signal = (0, (None,))

    for phases in itertools.permutations(range(5, 10)):
        value = await run_loop(mem, phases)
        signal = max(signal, (value, phases))

    print(f"Maximum signal is {signal[0]} for phase sequence {signal[1]}.")


async def run_loop(mem, phases):
    queues = [Queue() for _ in phases]

    for queue, phase in zip(queues, phases):
        await queue.put(phase)
    await queues[0].put(0)  # initial input

    await asyncio.gather(*[
        run(list(mem), qin, qout) for qin, qout in zip(queues, queues[1:] + [queues[0]])
    ])
    return await queues[0].get()


async def run(mem, inp: Queue, out: Queue):
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
            mem[ax] = await inp.get()
            i += 2
        elif op == 4:  # output
            output = read(mem, ax, am)
            # print(f"{output=} for {inputs=}")
            await out.put(output)
            i += 2
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
    asyncio.run(main())
