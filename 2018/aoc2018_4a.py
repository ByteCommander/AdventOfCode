# Advent Of Code 2018, day 4, part 1
# http://adventofcode.com/2018/day/4
# solution by ByteCommander, 2018-12-04

import re
from collections import Counter

pattern = re.compile(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (?:Guard #(\d+) )?(begins shift|falls asleep|wakes up)")
records = []
guards = {}

with open("inputs/aoc2018_4.txt") as file:
    for line in file:
        records.append([(int(x) if x and x.isdecimal() else x) for x in pattern.match(line).groups()])

current_guard = None
sleep_start = None
for year, month, day, hour, minute, guard, event in sorted(records):
    if event == "begins shift":
        current_guard = guard
        guards.setdefault(current_guard, [])
    elif event == "falls asleep":
        sleep_start = minute
    elif event == "wakes up":
        # print(current_guard, sleep_start, minute,
        # "." * sleep_start + "#" * (minute-sleep_start) + "." * (60-minute), sep="\t")
        guards[current_guard].extend(range(sleep_start, minute))

sleep_length, sleepiest_guard = max([(len(guards[guard]), guard) for guard in guards])
sleepiest_minute, amount = Counter(guards[sleepiest_guard]).most_common(1)[0]

print(f"Guard {sleepiest_guard} is the sleepiest one with {sleep_length} minutes total nap time.")
print(f"They sleep most often during the minute at 00:{sleepiest_minute:02d}.")
print(f"Therefore solution is: {sleepiest_guard * sleepiest_minute}")
