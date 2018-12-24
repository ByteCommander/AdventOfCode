# Advent Of Code 2018, day 20, part 1
# http://adventofcode.com/2018/day/20
# solution by ByteCommander, 2018-12-23

print("""WARNING:
This is a general solution that would solve all inputs based only on the problem description.
It does not make any further assumptions, but therefore is way too slow for the actual input
(didn't finish within several hours). It works well on the given examples though.
I'm leaving it here because of that and due to the amount of work I put in.
""")

# with open("inputs/aoc2018_20.txt") as file:
#     regex = file.read().strip("^$ \n")
regex = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"

doors = set()  # tuples of linked rooms (x1, y1, x2, y2), where x1 <= x2 and y1 <= y2
sx, sy = 0, 0


def parse(regex, x, y):
    # print(">", regex, x, y)

    for i, char in enumerate(regex):
        if char in "NESW":
            if char == "N":
                nx, ny = x, y - 1
            elif char == "E":
                nx, ny = x + 1, y
            elif char == "S":
                nx, ny = x, y + 1
            elif char == "W":
                nx, ny = x - 1, y

            doors.add((min(x, nx), min(y, ny), max(x, nx), max(y, ny)))
            x, y = nx, ny
            # print(char, x, y, doors)
            # show((x, y, "x"))

        elif char == "(":
            balance = 1
            branch = []
            branches = [branch]

            for j, char in enumerate(regex[i + 1:], i + 1):
                if char == "(":
                    branch.append(char)
                    balance += 1

                elif char == ")":
                    balance -= 1
                    if balance == 0:
                        rest = regex[j + 1:]
                        for branch in branches:
                            parse("".join(branch) + rest, x, y)
                        break
                    else:
                        branch.append(char)

                elif char == "|" and balance == 1:
                    branch = []
                    branches.append(branch)

                else:
                    branch.append(char)

            break

        i += 1


def show(*markers):
    xmin = min(min(x1, x2) for x1, y1, x2, y2 in doors)
    xmax = max(max(x1, x2) for x1, y1, x2, y2 in doors)
    ymin = min(min(y1, y2) for x1, y1, x2, y2 in doors)
    ymax = max(max(y1, y2) for x1, y1, x2, y2 in doors)

    printmap = [["#"] * (xmax - xmin + 1) * 2 for _ in range((ymax - ymin + 1) * 2)]

    for x1, y1, x2, y2 in doors:
        printmap[(y1 - ymin) * 2][(x1 - xmin) * 2] = " "
        printmap[(y2 - ymin) * 2][(x2 - xmin) * 2] = " "
        printmap[(2 * (y1 - ymin) + 2 * (y2 - ymin)) // 2][(2 * (x1 - xmin) + 2 * (x2 - xmin)) // 2] = "+"

    for x, y, char in markers:
        printmap[(y - ymin) * 2][(x - xmin) * 2] = char

    print("#" * ((xmax - xmin + 1) * 2 + 1))
    for row in printmap:
        print("#" + "".join(row))
    print()


def flood(startx, starty):
    flooded = set()
    waves = {(0, startx, starty)}

    while waves:
        dist, x, y = min(waves)
        waves.discard((dist, x, y))
        flooded.add((x, y))

        for nx, ny in (x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y):
            if (
                (min(x, nx), min(y, ny), max(x, nx), max(y, ny)) in doors
                and (nx, ny) not in flooded
            ):
                waves.add((dist + 1, nx, ny))

    return x, y, dist


parse(regex, sx, sy)

far_x, far_y, distance = flood(sx, sy)

show((sx, sy, "S"), (far_x, far_y, "F"))
print(f"The most distant room [F] from the start [S] is {distance} doors away.")
