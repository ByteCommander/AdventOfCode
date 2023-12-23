# Advent Of Code 2023, day 23, part 1
# http://adventofcode.com/2023/day/23
# solution by ByteCommander, 2023-12-23
from typing import TextIO

from aoc_tools.lib import run

PATH, FOREST, SLOPE_UP, SLOPE_DOWN, SLOPE_LEFT, SLOPE_RIGHT = ".#^v<>"
SLOPES = (SLOPE_UP, SLOPE_DOWN, SLOPE_LEFT, SLOPE_RIGHT)

type Point = (int, int)


def main(file: TextIO):
    grid = [list(line.strip()) for line in file]
    start = (0, grid[0].index(PATH))
    goal = (len(grid) - 1, grid[-1].index(PATH))

    # Assumption: crossings are always flat and never have slopes, so we only check we don't walk up against one.
    # Idea: convert grid map into a directional graph first (crossroads as nodes, whole path length between crossroads
    # as edge weights), then only span up a tree of all possible ways through the graph, rather than having to
    # walk the whole maze over and over.

    crossings: dict[Point, list[(Point, int)]] = {start: []}  # (y, x) -> [(connected_cross(y, x), distance)...]
    # heads: ((y, x), prev(y, x), prev crossing, distance, sloped?)
    heads: list[(Point, Point, Point, int, bool)] = [(start, start, start, 0, False)]
    while heads:
        (y, x), (py, px), p_cross, dist, sloped = heads.pop()

        neighbors: list[Point] = []
        if (ny := y - 1) >= 0 and (ny, x) != (py, px) and grid[ny][x] not in (FOREST, SLOPE_DOWN):  # walk up
            neighbors.append((ny, x))
        if (ny := y + 1) < len(grid) and (ny, x) != (py, px) and grid[ny][x] not in (FOREST, SLOPE_UP):  # down
            neighbors.append((ny, x))
        if (nx := x - 1) >= 0 and (y, nx) != (py, px) and grid[y][nx] not in (FOREST, SLOPE_RIGHT):  # left
            neighbors.append((y, nx))
        if (nx := x + 1) < len(grid[y]) and (y, nx) != (py, px) and grid[y][nx] not in (FOREST, SLOPE_LEFT):  # right
            neighbors.append((y, nx))

        if len(neighbors) == 1:  # simple path segment -> add distance to current edge
            ny, nx = neighbors[0]
            heads.append(((ny, nx), (y, x), p_cross, dist + 1, sloped or grid[ny][nx] in SLOPES))
        elif len(neighbors) > 1 or (y, x) == goal:  # crossroad (or goal) -> create new node
            crossings[p_cross].append(((y, x), dist))  # add new crossing to list of previous crossing's connections
            if (y, x) not in crossings:  # first time seeing a new crossing, otherwise end search head here (cycle)
                crossings[y, x] = [] if sloped else [(p_cross, dist)]  # add path back if we had no slope
                for ny, nx in neighbors:
                    heads.append(((ny, nx), (y, x), (y, x), 1, grid[ny][nx] in SLOPES))

    # print(*crossings.items(), sep="\n")
    paths: list[list[(Point, int)]] = recurse_graph(crossings, start, goal)
    # print(*paths, sep="\n")
    longest = max(path[1] for path in paths)
    print(f"The longest scenic route through the forest takes {longest} steps.")


def recurse_graph(
        crossings: dict[Point, list[(Point, int)]], start: Point, goal: Point,
        path: list[Point] = None, dist: int = 0
) -> list[(list[Point], int)]:
    """
    Recursively span up a tree of all possible paths (list of node steps and each total distance) through the graph.
    :param crossings: directed graph (dict mapping nodes to lists of neighbor nodes and distances)
    :param start: start node (or current intermediate node from which to search paths)
    :param goal: final goal node
    :param path: path nodes so far
    :param dist: accumulated distance so far
    :return: list of tuples of paths (list of node steps) and each path's total distance
    """
    if path is None:
        path = []
    if start == goal:
        return [(path, dist)]

    return sum([
        recurse_graph(crossings, ncross, goal, path + [ncross], dist + ndist)
        for ncross, ndist in crossings[start] if ncross not in path
    ], [])


TEST_INPUT = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
