# Advent Of Code 2018, day 20, part 2
# http://adventofcode.com/2018/day/20
# solution by ByteCommander, 2018-12-24

# INFO: This code makes the assumption that all branches in the regex are either
# terminal (no more NESW characters afterwards) or return back to their starting
# point. There is no clear indication this assumption is valid in the problem
# description, but it fits the examples and input. Without this assumption,
# the program does not finish within hours (see first attempt aoc2018_20a_.py).

with open("inputs/aoc2018_20.txt") as file:
    regex = file.read().strip("^$ \n")

doors = set()  # tuples of linked rooms (x1, y1, x2, y2), where x1 <= x2 and y1 <= y2
sx, sy = 0, 0


def show(*markers):
    xmin = min(min(x1, x2) for x1, y1, x2, y2 in doors)
    xmax = max(max(x1, x2) for x1, y1, x2, y2 in doors)
    ymin = min(min(y1, y2) for x1, y1, x2, y2 in doors)
    ymax = max(max(y1, y2) for x1, y1, x2, y2 in doors)

    grid = [["#"] * (xmax - xmin + 1) * 2 for _ in range((ymax - ymin + 1) * 2)]

    for x1, y1, x2, y2 in doors:
        grid[(y1 - ymin) * 2][(x1 - xmin) * 2] = " "
        grid[(y2 - ymin) * 2][(x2 - xmin) * 2] = " "
        grid[(2 * (y1 - ymin) + 2 * (y2 - ymin)) // 2][(2 * (x1 - xmin) + 2 * (x2 - xmin)) // 2] = "+"

    for x, y, char in markers:
        grid[(y - ymin) * 2][(x - xmin) * 2] = char

    print("#" * ((xmax - xmin + 1) * 2 + 1))
    for row in grid:
        print("#" + "".join(row))
    print()


# stack-based regex parsing (with the assumption stated above):

stack = []
x, y, = sx, sy
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
        stack.append((x, y))

    elif char == "|":
        x, y = stack[-1]

    elif char == ")":
        stack.pop()

# flood-fill to find all paths longer than 1000 doors

flooded = set()
waves = {(0, sx, sy)}
counter = 0

while waves:
    dist, x, y = min(waves)
    waves.discard((dist, x, y))
    flooded.add((x, y))
    if dist >= 1000:
        counter += 1

    for nx, ny in (x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y):
        if (
            (min(x, nx), min(y, ny), max(x, nx), max(y, ny)) in doors
            and (nx, ny) not in flooded
        ):
            waves.add((dist + 1, nx, ny))

show((sx, sy, "S"), (x, y, "F"))
print(f"There are {counter} rooms which are 1000 or more doors away.")
