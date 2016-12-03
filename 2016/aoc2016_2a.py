# Advent Of Code 2016, day 2, part 1
# http://adventofcode.com/2016/day/2
# solution by ByteCommander, 2016-12-02

data = open("inputs/aoc2016_2.txt").read()
dirs = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}  # (x,y) steps
pad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
btns = []

x, y = 1, 1
for instr in data.splitlines():
    for ins in instr.strip():
        x += dirs[ins][0]
        y += dirs[ins][1]
        if x < 0:
            x = 0
        elif x > 2:
            x = 2
        if y < 0:
            y = 0
        elif y > 2:
            y = 2
    btns.append(pad[y][x])

print("Answer: the right combination to open the door is {}".format(
    "".join(map(str, btns))))
