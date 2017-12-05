# Advent Of Code 2017, day 5, part 1
# http://adventofcode.com/2017/day/5
# solution by ByteCommander, 2017-12-05

with open("inputs/aoc2017_5.txt") as file:
    instructions = [int(instr) for instr in file]

    i, counter = 0, 0
    while 0 <= i < len(instructions):
        instr = instructions[i]
        instructions[i] += 1
        i += instr
        counter += 1

    print("Answer: {} steps needed."
          .format(counter))
