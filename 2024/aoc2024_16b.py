# Advent Of Code 2024, day 16, part 2
# http://adventofcode.com/2024/day/16
# solution by ByteCommander, 2024-12-17
from heapq import heappop, heappush
from typing import TextIO

from aoc_tools.lib import run

STEP_COST, TURN_COST = 1, 1000
WALL, FREE, START, END = "#", ".", "S", "E"
DIR_NORTH, DIR_EAST, DIR_SOUTH, DIR_WEST = CLOCKWISE = 0, 1, 2, 3

NodeType = tuple[int, int, int]  # y, x, dir


def main(file: TextIO):
    grid: list[list[bool]] = []  # True = free "." (incl. start "S", end "E"), False = wall "#"
    sy, sx, ey, ex = -1, -1, -1, -1
    for y, line in enumerate(file):
        row: list[bool] = []
        grid.append(row)
        for x, v in enumerate(line.strip()):
            row.append(v != WALL)
            if v == START:
                sy, sx = y, x
            elif v == END:
                ey, ex = y, x

    # Turn maze grid into a graph, so that each crossing and corner combined with each relevant direction
    # becomes a node, and that the edges represent the cost to transition between them
    # (i.e. walk straight until the next crossing or corner, or turn 90 degrees to each side on the spot)

    graph: dict[NodeType, dict[NodeType, int]] = {}  # node1 (y, x, dir) -> node2 -> cost
    for y, row in enumerate(grid):
        for x, free in enumerate(row):
            if not free:  # skip wall tiles
                continue
            free_n, free_s, free_w, free_e = grid[y - 1][x], grid[y + 1][x], grid[y][x - 1], grid[y][x + 1]
            path_count = sum([free_n, free_s, free_w, free_e])
            if path_count == 2 and free_n == free_s and free_w == free_e:  # straight path, no node, ignore
                continue
            else:
                # create new unconnected node in graph for every direction
                for d in CLOCKWISE:
                    graph[y, x, d] = {}
                # Search backwards to see if we can connect an edge to a previously seen node in the north or west.
                # If there is a path in that direction, we can assume all steps until the next known node are free.
                if free_n:
                    for y2 in range(y - 1, -1, -1):
                        if (y2, x, DIR_NORTH) in graph:
                            cost = (y - y2) * STEP_COST
                            graph[y, x, DIR_NORTH][y2, x, DIR_NORTH] = cost  # link from current to previous node north
                            graph[y2, x, DIR_SOUTH][y, x, DIR_SOUTH] = cost  # link from previous to current node south
                            break
                if free_w:
                    for x2 in range(x - 1, -1, -1):
                        if (y, x2, DIR_WEST) in graph:
                            cost = (x - x2) * STEP_COST
                            graph[y, x, DIR_WEST][y, x2, DIR_WEST] = cost  # link from current to previous node west
                            graph[y, x2, DIR_EAST][y, x, DIR_EAST] = cost  # link from previous to current node east
                            break
                # Add graph edges to rotate between directions on the same position
                for di in range(dl := len(CLOCKWISE)):
                    d, dcw = CLOCKWISE[di], CLOCKWISE[(di + 1) % dl]
                    graph[y, x, d][y, x, dcw] = TURN_COST
                    graph[y, x, dcw][y, x, d] = TURN_COST
    # pprint(graph)

    # Use modified A* to find all equally cheap ideal routes through the graph from start to end.
    # open: ordered heap (estimated total cost, cost from start, node, previous node) - any path found but not finished
    open_nodes: list[tuple[int, int, NodeType, NodeType | None]] = [(0, 0, (sy, sx, DIR_EAST), None)]
    # closed: dict {node: (minimal cost from start, previous nodes)} - node fully processed and minimal path found
    closed_nodes: dict[NodeType, tuple[int, list[NodeType]]] = {}

    end_nodes: set[NodeType] = set()
    best_cost = float("inf")
    while open_nodes:
        _cost_estimated, cost_so_far, node, prev = heappop(open_nodes)
        if cost_so_far > best_cost:
            break

        if node in closed_nodes:  # already processed this duplicate in the meantime
            old_cost, old_prevs = closed_nodes[node]
            if old_cost == cost_so_far:  # same cost as older path, found an alternative
                old_prevs.append(prev)
            continue
        closed_nodes[node] = (cost_so_far, [prev])

        cy, cx, _cd = node
        if cy == ey and cx == ex:  # found the end target
            best_cost = min(best_cost, cost_so_far)
            end_nodes.add(node)  # remember this because we can arrive from any direction

        # process all neighboring nodes and add to open list
        for neighbor, edge_cost in graph[node].items():
            ny, nx, nd = neighbor
            cost_until_then = cost_so_far + edge_cost
            if neighbor in closed_nodes:  # skip already visited nodes
                old_cost, old_prevs = closed_nodes[neighbor]
                if old_cost == cost_until_then:  # same cost as older path, found an alternative
                    old_prevs.append(prev)
                continue

            # A* heuristic: estimate best case total path cost through this node from start to end
            estimation = cost_until_then + STEP_COST * (abs(ey - ny) + abs(ex - nx)) + TURN_COST * (
                2 if nd == DIR_SOUTH and ny > ey or nd == DIR_NORTH and ny < ey
                     or nd == DIR_EAST and nx > ex or nd == DIR_WEST and nx < ex else
                0 if ny == ey and (nd == DIR_NORTH and ny > ey or nd == DIR_SOUTH and ny < ey)
                     or nx == ex and (nd == DIR_WEST and nx > ex or nd == DIR_EAST and ny < ex)
                else 1
            )
            heappush(open_nodes, (estimation, cost_until_then, neighbor, node))

    tiles = set()
    for node in end_nodes:
        tiles |= recurse(grid, closed_nodes, node)

    print(f"There are {len(tiles)} tiles that are part of at least one ideal path.")


def recurse(grid: list[list[bool]], closed_nodes: dict[NodeType, tuple[int, list[NodeType]]], node: NodeType | None,
            path: list[NodeType] = None, tiles: set[tuple[int, int]] = None) -> set[tuple[int, int]]:
    """Trace back all found ideal paths through the graph and count the unique visited tiles."""
    if path is None:
        path = [node]
    if tiles is None:
        tiles = set()

    ny, nx, _nd = node
    _cost, prevs = closed_nodes[node]
    for prev in prevs:
        if prev is None:
            # print(path)
            continue

        py, px, _pd = prev
        if ny != py:
            tiles |= {(y, nx) for y in range(min(ny, py), max(ny, py) + 1)}
        if nx != px:
            tiles |= {(ny, x) for x in range(min(nx, px), max(nx, px) + 1)}
        tiles |= recurse(grid, closed_nodes, prev, path + [prev], tiles)

    return tiles


TEST_INPUT_1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
TEST_INPUT_2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

if __name__ == "__main__":
    run(main, TEST_INPUT_1, test_only=True)
    run(main, TEST_INPUT_2, test_only=False)
