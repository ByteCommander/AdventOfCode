# Advent Of Code 2019, day 2, part 2)
# http://adventofcode.com/2019/day/2
# solution by ByteCommander, 2019-12-02


def main():
    with open("inputs/aoc2019_2.txt") as file:
        mem = [int(x) for x in file.read().split(",")]

    WANTED = 19690720

    for noun in range(100):
        for verb in range(100):
            if compute(noun, verb, mem) == WANTED:
                print(f"The result of {WANTED} was found using {noun=} and {verb=},")
                print(f"so the answer is {100 * noun + verb}.")
                break
        else:
            continue
        break
    else:
        print("No solution found.")


def compute(noun, verb, memory):
    mem = list(memory)  # shallow copy
    mem[1] = noun
    mem[2] = verb

    i = 0
    while mem[i] != 99:
        if mem[i] == 1:
            mem[mem[i + 3]] = mem[mem[i + 1]] + mem[mem[i + 2]]
        elif mem[i] == 2:
            mem[mem[i + 3]] = mem[mem[i + 1]] * mem[mem[i + 2]]
        else:
            raise RuntimeError(f"Illegal opcode at {i=}: {mem[i]}")

        i += 4
    return mem[0]


if __name__ == "__main__":
    main()
