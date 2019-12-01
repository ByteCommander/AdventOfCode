# Advent Of Code 2017, day 17, part 1
# http://adventofcode.com/2017/day/17
# solution by ByteCommander, 2017-12-17


with open("inputs/aoc2017_17.txt") as file:
    progs = [chr(x) for x in range(ord("a"), ord("p") + 1)]

    for cmd in file.read().strip().split(","):
        if cmd[0] == "s":
            x = int(cmd[1:])
            progs = progs[-x:] + progs[:-x]
        elif cmd[0] == "x":
            a, b = map(int, cmd[1:].split("/"))
            progs[a], progs[b] = progs[b], progs[a]
        elif cmd[0] == "p":
            p, q = cmd[1:].split("/")
            a, b = progs.index(p), progs.index(q)
            progs[a], progs[b] = q, p

    print("Answer: after the dance, the order is '{}'"
          .format("".join(progs)))
