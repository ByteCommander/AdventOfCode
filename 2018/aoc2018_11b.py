# Advent Of Code 2018, day 11, part 2
# http://adventofcode.com/2018/day/11
# solution by ByteCommander, 2018-12-11

from functools import lru_cache

with open("inputs/aoc2018_11.txt") as file:
    serial = int(file.read())

max_power = 0
max_power_coords = None


@lru_cache(None)
def calc_power(x, y, size):
    global max_power, max_power_coords

    if size == 1:  # single field
        rack_id = x + 10
        power_lv = (rack_id * y + serial) * rack_id
        power = power_lv % 1000 // 100 - 5

    else:  # split the square in four partial squares
        if size % 2:
            # odd square size: make two bigger and two smaller squares and
            # subtract the intersecting center field otherwise counted twice
            half = size // 2
            power = (
                calc_power(x, y, half + 1) +
                calc_power(x + half + 1, y, half) +
                calc_power(x, y + half + 1, half) +
                calc_power(x + half, y + half, half + 1) +
                -calc_power(x + half, y + half, 1)
            )
        else:
            # even square size: four equally sized partial squares
            half = size // 2
            power = (
                calc_power(x, y, half) +
                calc_power(x + half, y, half) +
                calc_power(x, y + half, half) +
                calc_power(x + half, y + half, half)
            )

    if power > max_power:
        max_power, max_power_coords = power, (x, y, size)
        # print(max_power, max_power_coords)

    return power


print(f"Progress: {0:3}%", end="")

for size in range(1, 301):
    if not size % 3:
        print(f"\rProgress: {size // 3:3}%", end="")
    for x in range(1, 302 - size):
        for y in range(1, 302 - size):
            calc_power(x, y, size)

print(end="\r")
# print(calc_power.cache_info())

print(f"The highest powered square has {max_power} total power "
      f"and the coordinates/size {','.join(map(str, max_power_coords))}.")
