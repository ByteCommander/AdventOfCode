# Advent Of Code 2017, day 10, part 1
# http://adventofcode.com/2017/day/10
# solution by ByteCommander, 2017-12-10

import re

with open("inputs/aoc2017_10.txt") as file:
    line = file.read().strip()

    no_esc = re.sub(r"!.", "", line)
    no_garb = re.sub(r"<.*?>", "", no_esc)

    stack = [0]
    score = 0
    for x in no_garb:
        top = stack[-1]
        if x == "{":
            stack.append(top + 1)
        elif x == "}":
            score += stack.pop()

    print("Answer: the stream has a score of {}."
          .format(score))
