# Advent Of Code 2018, day 7, part 1
# http://adventofcode.com/2018/day/7
# solution by ByteCommander, 2018-12-07

import re

dependencies = {}
order = []

with open("inputs/aoc2018_7.txt") as file:
    for line in file:
        dep, step = re.match(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line).groups()
        dependencies.setdefault(step, set()).add(dep)
        dependencies.setdefault(dep, set())

while any(dependencies):
    step = min(step for step, conditions in dependencies.items() if not conditions)

    order.append(step)
    dependencies.pop(step)
    for conditions in dependencies.values():
        conditions.discard(step)


print(f"The step order is {''.join(order)}")
