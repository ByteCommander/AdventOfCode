# Advent Of Code 2023, day 23, part 2
# http://adventofcode.com/2023/day/23
# solution by ByteCommander, 2023-12-23
from typing import TextIO

from aoc_tools.lib import run

type Point = (int, int)

PATH, FOREST, SLOPE_UP, SLOPE_DOWN, SLOPE_LEFT, SLOPE_RIGHT = ".#^v<>"
SLOPES = (SLOPE_UP, SLOPE_DOWN, SLOPE_LEFT, SLOPE_RIGHT)


# Note: This part takes around 15s on the real input.

def main(file: TextIO):
    grid = [list(line.strip()) for line in file]
    start = (0, grid[0].index(PATH))
    goal = (len(grid) - 1, grid[-1].index(PATH))

    # Idea: convert grid map into a directional graph first (crossroads as nodes, whole path length between crossroads
    # as edge weights), then only span up a tree of all possible ways through the graph, rather than having to
    # walk the whole maze over and over.

    crossings: dict[Point, list[(Point, int)]] = {start: []}  # (y, x) -> [(connected_cross(y, x), distance)...]
    # heads: ((y, x), prev(y, x), prev crossing, distance)
    heads: list[(Point, Point, Point, int)] = [(start, start, start, 0)]
    while heads:
        (y, x), (py, px), p_cross, dist = heads.pop()

        neighbors: list[Point] = []
        if (ny := y - 1) >= 0 and (ny, x) != (py, px) and grid[ny][x] != FOREST:  # walk up
            neighbors.append((ny, x))
        if (ny := y + 1) < len(grid) and (ny, x) != (py, px) and grid[ny][x] != FOREST:  # down
            neighbors.append((ny, x))
        if (nx := x - 1) >= 0 and (y, nx) != (py, px) and grid[y][nx] != FOREST:  # left
            neighbors.append((y, nx))
        if (nx := x + 1) < len(grid[y]) and (y, nx) != (py, px) and grid[y][nx] != FOREST:  # right
            neighbors.append((y, nx))

        if len(neighbors) == 1:  # simple path segment -> add distance to current edge
            ny, nx = neighbors[0]
            heads.append(((ny, nx), (y, x), p_cross, dist + 1))
        elif len(neighbors) > 1 or (y, x) == goal:  # crossroad (or goal) -> create new node
            crossings[p_cross].append(((y, x), dist))  # add this crossing to list of previous crossing's connections
            if (y, x) not in crossings:  # first time seeing a new crossing, otherwise end search head here (cycle)
                crossings[y, x] = [(p_cross, dist)]  # new crossing, add path back
                for ny, nx in neighbors:
                    heads.append(((ny, nx), (y, x), (y, x), 1))

    # print(*crossings.items(), sep="\n")
    longest = recurse_graph(crossings, start, goal)
    print(f"The longest scenic route through the forest (ignoring slopes) takes {longest} steps.")


def recurse_graph(
        crossings: dict[Point, list[(Point, int)]], start: Point, goal: Point,
        path: set[Point] = None, dist: int = 0
) -> int:
    """
    Recursively search all possible routes between start and goal through the graph and return the length of the
    longest possible route.

    See recurse_graph(...) in part 1 for a more flexible/verbose but much slower version which also returns
    a list of all paths (ordered list of nodes) and their respective lengths. This is optimized away here.
    :param crossings: directed graph (dict mapping nodes to lists of neighbor nodes and distances)
    :param start: start node (or current intermediate node from which to search paths)
    :param goal: final goal node
    :param path: path nodes so far (unordered set for runtime optimization)
    :param dist: accumulated distance so far
    :return: total distance of the longest path between start and goal
    """
    # Replacing the path list with a set for faster "in" lookups cut the runtime in half (~60s to ~30s).
    # Modifying the path set in place instead of copying it each time cut it in half again (~30s to ~15s).

    if path is None:
        path = set()
    if start == goal:
        # print("found", dist, path)
        return dist

    longest = -1
    for ncross, ndist in crossings[start]:
        if ncross not in path:
            # Modify path nodes set in place instead of copying by adding each visited node before recursing deeper
            # and removing it again afterward before trying the next candidate. This saves time and memory.
            path.add(ncross)
            longest = max(longest, recurse_graph(crossings, ncross, goal, path, dist + ndist))
            path.remove(ncross)
    return longest


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
