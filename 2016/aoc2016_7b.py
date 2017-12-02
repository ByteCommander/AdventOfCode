# Advent Of Code 2016, day 7, part 2
# http://adventofcode.com/2016/day/7
# solution by ByteCommander, 2016-12-14

import regex  # instead of re because we need overlapped=True

data = open("inputs/aoc2016_7.txt").read()

counter = 0
for line in data.splitlines():
    found = False
    m1 = regex.findall(r'(\w)((?!\W|\1).)\1(?=[^[\]]*?(?:\[|\Z))', line, overlapped=True)
    if m1:
        for groups in m1:
            m2 = regex.search(r'{1}{0}{1}(?=[^[\]]*?\])'.format(*groups), line)
            if m2:
                counter += 1
                break

print("Answer: {} IPs support SSL".format(counter))
