# Advent Of Code 2016, day 4, part 1
# http://adventofcode.com/2016/day/4
# solution by ByteCommander, 2016-12-04

import re
from collections import Counter

data = open("inputs/aoc2016_4.txt").read()
idsum = 0
for line in data.splitlines():
    name, rid, cs = re.fullmatch(r"([a-z-]+)-(\d+)\[([a-z]+)\]", line).groups()
    c = Counter(name.replace("-", ""))
    sc = sorted(sorted(c.items(), key=lambda x: x[0]), key=lambda x: -x[1])
    s = "".join(x[0] for x in sc[:5])
    if s == cs:
        idsum += int(rid)

print("Answer: the sum of all existing rooms' IDs is {}".format(idsum))
