# Advent Of Code 2017, day 12, part 1
# http://adventofcode.com/2017/day/12
# solution by ByteCommander, 2017-12-12

with open("inputs/aoc2017_12.txt") as file:
    links = {}

    for line in file:
        src, dests = line.split(" <-> ")
        links[int(src)] = [int(dest) for dest in dests.split(", ")]

    visited = set()
    todo = {0}
    while todo:
        node = todo.pop()
        visited.add(node)
        for link in links[node]:
            if link not in visited:
                todo.add(link)

    print("Answer: {} nodes are connected to node 0."
          .format(len(visited)))
