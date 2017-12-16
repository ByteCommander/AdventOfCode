# Advent Of Code 2017, day 16, part 2
# http://adventofcode.com/2017/day/16
# solution by ByteCommander, 2017-12-16

DANCES = 1000000000


def dance():
    global progs, instrs
    for cmd in instrs:
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
    return progs


with open("inputs/aoc2017_16.txt") as file:
    progs = [chr(x) for x in range(ord("a"), ord("p") + 1)]
    instrs = file.read().strip().split(",")

    states = []
    i = 1
    while i <= DANCES:
        dance()
        s = "".join(progs)
        if states is not None and s in states:
            loop_len = len(states) - states.index(s)
            remaining = (DANCES - i) % loop_len
            i = DANCES - remaining + 1
            states = None
        else:
            if states is not None:
                states.append(s)
            i += 1

    print("Answer: after {} dances, the order is '{}'"
          .format(DANCES, "".join(progs)))
