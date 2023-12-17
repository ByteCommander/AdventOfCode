# Advent Of Code 2023, day 17, part 1
# http://adventofcode.com/2023/day/17
# solution by ByteCommander, 2023-12-17
from heapq import heappop, heappush
from typing import TextIO

from aoc_tools.lib import run


# Task: find a path through the grid from top left to bottom right with the lowest cost,
# while never going more than 3 steps in a straight line at a time.
# Idea: write an A*, but instead of 1 edge per field, treat any sequence of 1-3 straight steps between curves
# as a single edge in the network graph. So from one node, you can end up on the nodes 1-3 left to it,
# or 1-3 right to it. You can't go further straight because that would have been covered already by the previous node.
# This means every step has up to six potential next steps, and any field can be visited twice, approaching it
# either vertically or horizontally, so it has to be represented as (y:int, x:int, v:bool).


def main(file: TextIO):
    grid: list[list[int]] = [[*map(int, line.strip())] for line in file]
    height, width = len(grid), len(grid[0])
    start = 0, 0
    goal = height - 1, width - 1

    path_cost = a_star(grid, start, goal)
    print(f"Found optimal path with cost {path_cost}:")


def a_star(grid: list[list[int]], start: (int, int), goal: (int, int)):
    # A* closed list (fully expanded nodes): (y,x,v) -> (cost, predecessor(y,x,v))
    closed: dict[(int, int, bool), (int, (int, int, bool))] = {}

    # A* open list (heap based priority queue for next promising candidates):
    # open_q: [(cost estimate, cost so far, y, x, v, predecessor(y,x,v))]
    h0 = abs(goal[0] - start[0]) + abs(goal[1] - start[1])  # heuristic (optimistic cost estimation) for start point
    open_q: list[(int, int, int, int, bool, (int, int, bool))] = [
        (h0, 0, *start, False, None),
        (h0, 0, *start, True, None)
    ]

    while open_q:
        _, c, y, x, v, pre = heappop(open_q)
        # print(f"visiting c={c}, ({y},{x},{int(v)}), closed: {len(closed)}, open: {len(open_q)}")
        if (y, x, v) in closed:  # skip if node was queued multiple times and already processed in the meantime
            continue

        closed[y, x, v] = (c, pre)

        if (y, x) == goal:
            break

        for jc, ny, nx in next_nodes(grid, y, x, v):
            nv = not v
            if (ny, nx, nv) not in closed:  # don't queue already fully processed nodes
                nc = c + jc  # known cost so far of next node (current node cost + jump cost)
                nh = nc + abs(goal[0] - ny) + abs(goal[1] - nx)  # heuristic of next node
                heappush(open_q, (nh, nc, ny, nx, nv, (y, x, v)))
                # print(f"added c={nc}, ({ny},{nx},{int(nv)})")
    else:
        return 0  # no solution

    node = (y, x, v)
    while node:
        cost, prev = closed[node]
        # print(node, cost)
        node = prev
    return c


def next_nodes(grid: list[list[int]], y: int, x: int, v: bool) -> list[(int, int, int)]:
    height, width = len(grid), len(grid[0])

    # find y,x coordinates of possible target fields to jump to
    ds = [*range(-3, 0)] + [*range(1, 4)]  # distances to walk: [-3..3] without 0
    if v:  # arrived vertically, must walk horizontally now
        nxt_yxs = [(y, x + d) for d in ds if 0 <= x + d < width]
    else:
        nxt_yxs = [(y + d, x) for d in ds if 0 <= y + d < height]

    # sum up the intermediate field costs for every jump
    nxts: list[(int, int, int)] = []  # [(jump cost, next y, next x), ...]
    for ny, nx in nxt_yxs:
        ic = 0
        # loop over intermediate fields from (y,x) exclusive to (ny,nx) inclusive:
        for iy in [y] if ny == y else range(ny, y, 1 if ny < y else -1):
            for ix in [x] if nx == x else range(nx, x, 1 if nx < x else -1):
                ic += grid[iy][ix]
        nxts.append((ic, ny, nx))
    return nxts


TEST_INPUT = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
