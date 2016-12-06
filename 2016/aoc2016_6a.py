# Advent Of Code 2016, day 6, part 1
# http://adventofcode.com/2016/day/6
# solution by ByteCommander, 2016-12-06

from collections import Counter

data = open("inputs/aoc2016_6.txt").read()
rows = data.splitlines()
columns = zip(*rows)

counters = [Counter(col) for col in columns]
message = "".join(c.most_common()[0][0] for c in counters)

print("Answer: the received message is {}".format(message))
