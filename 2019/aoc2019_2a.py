# Advent Of Code 2019, day 2, part 1)
# http://adventofcode.com/2019/day/2
# solution by ByteCommander, 2019-12-02


def main():
    with open("inputs/aoc2019_2.txt") as file:
        mem = [int(x) for x in file.read().split(",")]

    mem[1] = 12
    mem[2] = 2

    i = 0
    while mem[i] != 99:
        # print(i, mem[i], mem)

        if mem[i] == 1:
            mem[mem[i + 3]] = mem[mem[i + 1]] + mem[mem[i + 2]]
        elif mem[i] == 2:
            mem[mem[i + 3]] = mem[mem[i + 1]] * mem[mem[i + 2]]
        else:
            raise RuntimeError(f"Illegal opcode at {i=}: {mem[i]}")

        i += 4

    # print(mem)
    print(f"Once the program halts, position 0 holds the value {mem[0]}.")


if __name__ == "__main__":
    main()
