# Advent Of Code 2016, day 4, part 2
# http://adventofcode.com/2016/day/4
# solution by ByteCommander, 2016-12-04

import re
from collections import Counter


def decrypt(name, rid):
    d = ""
    for l in name:
        if l == "-":
            d += " "
        else:
            d += chr(((ord(l) - ord("a") + rid) % 26) + ord("a"))
    return d


data = open("inputs/aoc2016_4.txt").read()
idsum = 0
for line in data.splitlines():
    name, rid, cs = re.fullmatch(r"([a-z-]+)-(\d+)\[([a-z]+)\]", line).groups()
    c = Counter(name.replace("-", ""))
    sc = sorted(sorted(c.items(), key=lambda x: x[0]), key=lambda x: -x[1])
    s = "".join(x[0] for x in sc[:5])
    if s == cs:
        d = decrypt(name, int(rid))
        if "north" in d:
            print("Answer: room {} is the '{}'"
                  .format(rid, d))
            break
