# Advent Of Code 2019, day 3, part 1)
# http://adventofcode.com/2019/day/3
# solution by ByteCommander, 2019-12-03


def main():
    wires = []
    with open("inputs/aoc2019_3.txt") as file:
        for line in file:
            wire = set()
            x, y = 0, 0
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
                    wire.add((x, y))
            wires.append(wire)

    closest = min(abs(a) + abs(b) for a, b in set.intersection(*wires))
    print(f"The closest wire intersection is {closest} squares away from the start.")


if __name__ == "__main__":
    main()
