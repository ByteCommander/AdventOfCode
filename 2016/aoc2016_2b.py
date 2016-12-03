# Advent Of Code 2016, day 2, part 2
# http://adventofcode.com/2016/day/2
# solution by ByteCommander, 2016-12-03

data = open("inputs/aoc2016_2.txt").read()
dirs = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}  # (x,y) steps
pad = [["", "", "1", "", ""], ["", "2", "3", "4", ""],
       ["5", "6", "7", "8", "9"], ["", "A", "B", "C", ""],
       ["", "", "D", "", ""]]
btns = []

x, y = 0, 2
for instr in data.splitlines():
    for ins in instr.strip():
        x2 = x + dirs[ins][0]
        y2 = y + dirs[ins][1]
        if 0 <= x2 < 5 and 0 <= y2 < 5 and pad[y2][x2] != "":
            x, y = x2, y2
    btns.append(pad[y][x])

print("Answer: the right combination to open the door is {}".format(
    "".join(map(str, btns))))
