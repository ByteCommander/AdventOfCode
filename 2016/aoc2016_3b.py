# Advent Of Code 2016, day 3, part 2
# http://adventofcode.com/2016/day/3
# solution by ByteCommander, 2016-12-03

data = open("inputs/aoc2016_3.txt").read()

# parse input to vertical groups of 3 numbers
rows = [[int(x) for x in line.split()] for line in data.splitlines()]
vertically = [item for inner in zip(*rows) for item in inner]
v3 = [vertically[i:i + 3] for i in range(0, len(vertically), 3)]

counter = 0
for a, b, c in v3:
    if a + b > c and a + c > b and b + c > a:
        counter += 1

print("Answer: there are {} possible vertical triangles".format(counter))
