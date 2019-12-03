# Advent Of Code 2019, day 3, part 2)
# http://adventofcode.com/2019/day/3
# solution by ByteCommander, 2019-12-03


def main():
    wires = []
    with open("inputs/aoc2019_3.txt") as file:
        for line in file:
            wire = {}
            wires.append(wire)
            x, y, s = 0, 0, 0
            for instr in line.split(","):
                direction = instr[0]
                distance = int(instr[1:])
                for step in range(distance):
                    if direction == "U":
                        y += 1
                    elif direction == "D":
                        y -= 1
                    elif direction == "L":
                        x -= 1
                    elif direction == "R":
                        x += 1
                    else:
                        raise RuntimeError("Invalid direction")

                    # important: a self-crossing wire does not short-circuit,
                    # don't reset s to the lower value on the crossing, just leave the existing crossing value alone
                    s += 1
                    wire.setdefault((x, y), s)

    intersections = set.intersection(*map(set, wires))
    # print(*[(i, wires[0][i], wires[1][i], wires[0][i]+wires[1][i]) for i in intersections], sep="\n")
    closest = min(sum(wire[(x, y)] for wire in wires) for x, y, in intersections)
    print(f"The closest wire intersection is {closest} total steps on the wires away from the start.")


if __name__ == "__main__":
    main()
