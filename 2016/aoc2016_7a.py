# Advent Of Code 2016, day 7, part 1
# http://adventofcode.com/2016/day/7
# solution by ByteCommander, 2016-12-07

import re

data = open("inputs/aoc2016_7.txt").read()

counter = 0
for line in data.splitlines():
    m1 = re.search(r'\[[^[\]]*(\w)((?!\W|\1).)\2\1[^[\]]*\]', line)
    if not m1:
        m2 = re.search(r'(\w)((?!\W|\1).)\2\1', line)
        if m2:
            counter += 1

print("Answer: {} IPs support TLS".format(counter))
