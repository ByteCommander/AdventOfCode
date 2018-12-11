# Advent Of Code 2018, day 11, part 1
# http://adventofcode.com/2018/day/11
# solution by ByteCommander, 2018-12-11

with open("inputs/aoc2018_11.txt") as file:
    serial = int(file.read())


def get_power(x_, y_):
    rack_id = x_ + 10
    power_lv = (rack_id * y_ + serial) * rack_id
    return power_lv % 1000 // 100 - 5


biggest = None  # (total power, (x, y))

for x in range(1, 301):
    for y in range(1, 301):
        big_square = sum(get_power(x + dx, y + dy) for dx in range(3) for dy in range(3))
        if biggest is None or big_square > biggest[0]:
            biggest = (big_square, (x, y))

print(f"The highest powered 3x3 square has {biggest[0]} total power "
      f"and the coordinates {','.join(map(str, biggest[1]))}")
