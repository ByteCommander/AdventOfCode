# Advent Of Code 2019, day 5, part 1)
# http://adventofcode.com/2019/day/5
# solution by ByteCommander, 2019-12-05


def main():
    with open("inputs/aoc2019_5.txt") as file:
        mem = [int(x) for x in file.read().split(",")] + [None] * 3
        my_input = 5

    def read(xx, mode=0):
        if mode == 0:
            return mem[xx]
        elif mode == 1:
            return xx
        else:
            raise RuntimeError(f"Illegal arg mode {mode}")

    i = 0
    while True:
        mod_op, ax, bx, cx = mem[i:i + 4]
        modes, op = divmod(mod_op, 100)
        cm, bm, am = map(int, f"{modes:03.0f}")

        if op == 1:  # add
            mem[cx] = read(ax, am) + read(bx, bm)
            i += 4
        elif op == 2:  # multiply
            mem[cx] = read(ax, am) * read(bx, bm)
            i += 4
        elif op == 3:  # input
            mem[ax] = my_input
            i += 2
        elif op == 4:  # output
            print(f"Program output: {read(ax, am)}.")
            i += 2
        elif op == 5:  # jump-if-true
            i = read(bx, bm) if read(ax, am) else i + 3
        elif op == 6:  # jump-if-false
            i = read(bx, bm) if not read(ax, am) else i + 3
        elif op == 7:  # less-than
            mem[cx] = int(read(ax, am) < read(bx, bm))
            i += 4
        elif op == 8:  # equals
            mem[cx] = int(read(ax, am) == read(bx, bm))
            i += 4
        elif op == 99:
            break
        else:
            raise RuntimeError(f"Illegal opcode at {i=}: {mem[i]}")


if __name__ == "__main__":
    main()
