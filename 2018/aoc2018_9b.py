# Advent Of Code 2018, day 9, part 1
# http://adventofcode.com/2018/day/9
# solution by ByteCommander, 2018-12-09
import collections
import re

with open("inputs/aoc2018_9.txt") as file:
    players, marbles = map(int, re.match(
        r"(\d+) players; last marble is worth (\d+) points", file.read().strip()
    ).groups())

circle = collections.deque([0])
current = 0
scores = [0] * players

for m in range(1, marbles * 100):
    if m % 23:
        circle.rotate(-2)
        circle.appendleft(m)
        # print(f"[{m % players:3}]", *circle)
    else:
        circle.rotate(7)
        scores[m % players] += m + circle.popleft()

print(f"The highest score with 100 times more marbles is {max(scores)}.")
