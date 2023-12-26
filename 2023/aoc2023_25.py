# Advent Of Code 2023, day 25, single part
# http://adventofcode.com/2023/day/25
# solution by ByteCommander, 2023-12-25
from itertools import combinations
from typing import TextIO

from networkx import Graph, minimum_cut

from aoc_tools.lib import run


def main(file: TextIO):
    graph = Graph()
    for line in file:
        left, _right = line.strip().split(": ")
        for right in _right.split():
            graph.add_edge(left, right, capacity=1)

    print(graph)
    # try to find the minimum cut between two arbitrary nodes until we find a cut of size 3
    cut_val, set1, set2 = 0, set(), set()
    for a, b in combinations(graph.nodes(), 2):
        cut_val, (set1, set2) = minimum_cut(graph, a, b)
        if cut_val == 3:
            break

    print(f"Found a cut of size {cut_val} in the graph, dividing it into groups of {len(set1)} and {len(set2)},",
          f"nodes, resulting in a sizes product of {len(set1) * len(set2)}.")


TEST_INPUT = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
