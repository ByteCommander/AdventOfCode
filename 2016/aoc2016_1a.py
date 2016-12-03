# Advent Of Code 2016, day 1, part 1
# http://adventofcode.com/2016/day/1
# solution by ByteCommander, 2016-12-01

data = open("inputs/aoc2016_1.txt").read()
dirs = [(0, 1), (1, 0), (0, -1),
        (-1, 0)]  # dirs[0]: North, [1]: East, ... - (x,y) steps
instr = [[-1 if s[0] == "L" else 1, int(s[1:])] for s in data.split(", ")]

cd, x, y = 0, 0, 0
for d, l in instr:
    cd = (cd + d) % 4
    x += dirs[cd][0] * l
    y += dirs[cd][1] * l

print("Answer: shortest path is {} steps ({} N, {} E)"
      .format(abs(x) + abs(y), y, x))
