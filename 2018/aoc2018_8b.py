# Advent Of Code 2018, day 8, part 2
# http://adventofcode.com/2018/day/8
# solution by ByteCommander, 2018-12-08

with open("inputs/aoc2018_8.txt") as file:
    numbers = [int(x) for x in file.read().strip().split()]


def parse(data):
    num_of_children, num_of_metadata, *data = data

    length = 2 + num_of_metadata

    if num_of_children:
        children = []
        while num_of_children:
            child_value, child_length = parse(data)

            num_of_children -= 1
            children.append(child_value)
            length += child_length
            data = data[child_length:]

        metadata = data[:num_of_metadata]
        value = sum(children[i - 1] for i in metadata if 0 < i <= len(children))

    else:
        value = sum(data[:num_of_metadata])

    return value, length


result, total_length = parse(numbers)

print(f"The root node's value is {result}.")
