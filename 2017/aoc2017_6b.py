# Advent Of Code 2017, day 6, part 2
# http://adventofcode.com/2017/day/6
# solution by ByteCommander, 2017-12-06

with open("inputs/aoc2017_6.txt") as file:
    banks = [int(x) for x in file.read().strip().split()]
    seen = []

    # print(banks)
    while True:
        t_banks = tuple(banks)
        if t_banks in seen:
            break
        seen.append(t_banks)
        i_max = banks.index(max(banks))
        cache = banks[i_max]
        banks[i_max] = 0

        i = i_max
        while cache:
            i = (i + 1) % len(banks)
            banks[i] += 1
            cache -= 1
        # print(banks)

    print("Answer: {} steps are in the loop."
          .format(len(seen) - seen.index(t_banks)))
