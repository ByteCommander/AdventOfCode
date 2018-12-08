# Advent Of Code 2018, day 8, part 1
# http://adventofcode.com/2018/day/8
# solution by ByteCommander, 2018-12-08

with open("inputs/aoc2018_8.txt") as file:
    numbers = [int(x) for x in file.read().strip().split()]


def parse(data):
    num_of_children, num_of_metadata, *data = data

    children_sum = 0
    length = 2 + num_of_metadata

    while num_of_children:
        child_sum, child_length = parse(data)

        num_of_children -= 1
        children_sum += child_sum
        length += child_length
        data = data[child_length:]

    meta_sum = sum(data[:num_of_metadata])

    return meta_sum + children_sum, length


result, total_length = parse(numbers)

print(f"The sum of all metadata nodes is {result}.")
