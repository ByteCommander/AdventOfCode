# Advent Of Code 2018, day 7, part 2
# http://adventofcode.com/2018/day/7
# solution by ByteCommander, 2018-12-07

import re

WORKERS = 5
BASE_DURATION = 60

dependencies = {}
second = -1

with open("inputs/aoc2018_7.txt") as file:
    for line in file:
        dep, step = re.match(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line).groups()
        dependencies.setdefault(step, set()).add(dep)
        dependencies.setdefault(dep, set())


class Worker:
    def __init__(self, id_):
        self.id = id_
        self.task = None
        self.remaining = 0

    def __bool__(self):
        return self.task is not None

    def work(self):
        if self.remaining == 0:
            if self.task:
                for conditions in dependencies.values():
                    conditions.discard(self.task)

            self.task = min((step for step, conditions in dependencies.items() if not conditions), default=None)
            if self.task:
                dependencies.pop(self.task)
                self.remaining = ord(self.task) - ord("A") + 1 + BASE_DURATION

        # print(f"{second:3d}s: Worker {self.id} - {self.task or '.'} ({self.remaining} remaining)")

        if self.remaining:
            self.remaining -= 1


workers = [Worker(i) for i in range(WORKERS)]

while dependencies or any(workers):
    second += 1
    for w in workers:
        w.work()

print(f"The whole work takes {second - 1} seconds.")
