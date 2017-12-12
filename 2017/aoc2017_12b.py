# Advent Of Code 2017, day 12, part 2
# http://adventofcode.com/2017/day/12
# solution by ByteCommander, 2017-12-12

with open("inputs/aoc2017_12.txt") as file:
    links = {}

    for line in file:
        src, dests = line.split(" <-> ")
        links[int(src)] = [int(dest) for dest in dests.split(", ")]

    groups = 0
    while links:
        todo = {list(links)[0]}
        while todo:
            node = todo.pop()
            link_list = links.pop(node)
            for link in link_list:
                if link in links:
                    todo.add(link)
        groups += 1

    print("Answer: there are {} separated groups."
          .format(groups))
