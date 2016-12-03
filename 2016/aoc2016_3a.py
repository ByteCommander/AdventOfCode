# Advent Of Code 2016, day 3, part 1
# http://adventofcode.com/2016/day/3
# solution by ByteCommander, 2016-12-03

data = open("inputs/aoc2016_3.txt").read()
counter = 0
for line in data.splitlines():
    a, b, c = map(int, line.split())
    if a + b > c and a + c > b and b + c > a:
        counter += 1

print("Answer: there are {} possible triangles".format(counter))
