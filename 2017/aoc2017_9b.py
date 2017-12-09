# Advent Of Code 2017, day 9, part 2
# http://adventofcode.com/2017/day/9
# solution by ByteCommander, 2017-12-09

import re

with open("inputs/aoc2017_9.txt") as file:
    line = file.read().strip()

    no_esc = re.sub(r"!.", "", line)

    garbage = 0


    def replacer(match):
        global garbage
        garbage += len(match.group(0)) - 2
        return ""


    no_garb = re.sub(r"<.*?>", replacer, no_esc)

    print("Answer: the stream contained {} characters of garbage."
          .format(garbage))
