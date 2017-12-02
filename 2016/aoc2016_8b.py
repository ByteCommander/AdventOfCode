# advent of code 2016, day 8, part 2
# http://adventofcode.com/2016/day/8
# solution by bytecommander, 2017-12-02


data = open("inputs/aoc2016_8.txt").read()
board = [[0 for x in range(50)] for y in range(6)]


def rot_row(row, by):
    global board
    board[row] = board[row][-by:] + board[row][:-by]


def rot_col(col, by):
    global board
    board = list(map(list, zip(*board)))
    rot_row(col, by)
    board = list(map(list, zip(*board)))


for line in data.splitlines():
    # print("\n" + line)
    cmd, *args = line.split()

    if cmd == "rect":
        a, b = map(int, args[0].split("x"))
        for x in range(a):
            for y in range(b):
                board[y][x] = 1

    elif cmd == "rotate":
        direction, _a, _, b = args
        a, b = int(_a.split("=")[-1]), int(b)

        if direction == "row":
            rot_row(a, b)
        else:
            rot_col(a, b)

    pass
    # print(*["|" + "".join("#" if c else " " for c in row) + "|"
    #         for row in board], sep="\n")

print("Answer:")
print(*["".join("#" if c else " " for c in row) for row in board], sep="\n")
