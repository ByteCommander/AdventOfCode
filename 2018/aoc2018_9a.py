# Advent Of Code 2018, day 9, part 1
# http://adventofcode.com/2018/day/9
# solution by ByteCommander, 2018-12-09

import re

with open("inputs/aoc2018_9.txt") as file:
    players, marbles = map(int, re.match(
        r"(\d+) players; last marble is worth (\d+) points", file.read().strip()
    ).groups())

circle = [0]
current = 0
scores = [0] * players

for m in range(1, marbles):
    if m % 23:
        current = (current + 1) % len(circle) + 1
        circle.insert(current, m)
        # print(f"[{m % players + 1:3}]",
        #       " ".join(f"({x})" if i == current else f" {x} " for (i, x) in enumerate(circle)))
    else:
        current = (current - 7) % len(circle)
        scores[m % players] += m + circle.pop(current)

print(f"The highest score is {max(scores)}.")
