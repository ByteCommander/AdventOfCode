# Advent Of Code 2016, day 1, part 2
# http://adventofcode.com/2016/day/1
# solution by ByteCommander, 2016-12-01

data = open("inputs/aoc2016_1.txt").read()
dirs = [(0, 1), (1, 0), (0, -1),
        (-1, 0)]  # dirs[0]: North, [1]: East, ... - (x,y) steps
instr = [[-1 if s[0] == "L" else 1, int(s[1:])] for s in data.split(", ")]

cd, x, y = 0, 0, 0
track = [(x, y)]
for d, l in instr:
    cd = (cd + d) % 4
    for i in range(l):
        x += dirs[cd][0]
        y += dirs[cd][1]
        if (x, y) in track:
            print(
                "Answer: first coordinates visited twice are {} steps away ({}|{})"
                    .format(abs(x) + abs(y), y, x))
            exit()
        track.append((x, y))
