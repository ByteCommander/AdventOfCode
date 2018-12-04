# Advent Of Code 2018, day 4, part 2
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

# print(*[(guard, Counter(guards[guard]).most_common(1)[0]) for guard in guards if guards[guard]], sep="\n")
guard, (sleepiest_minute, amount) = max(
    ((guard, Counter(guards[guard]).most_common(1)[0]) for guard in guards if guards[guard]),
    key=lambda guard_minute_amount: guard_minute_amount[1][1]
)

print(f"Guard {guard} is most often asleep during the same minute, at 00:{sleepiest_minute:02d}.")
print(f"Therefore solution is: {guard * sleepiest_minute}")
