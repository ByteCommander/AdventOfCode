# Advent Of Code 2023, day 22, part 1
# http://adventofcode.com/2023/day/22
# solution by ByteCommander, 2023-12-22
from itertools import product
from typing import TextIO

from aoc_tools.lib import run

type Xyz = (int, int, int)


def main(file: TextIO):
    snapshot: list[(int, Xyz, Xyz)] = []  # (brick id, ends...) snapshot of falling bricks suspended in the air
    for _id, line in enumerate(file):
        snapshot.append((_id, *[(tuple(map(int, _xyz.split(",")))) for _xyz in line.strip().split("~")]))

    # inventory of normalized, fallen down bricks, with IDs of bricks supporting and supported by each
    bricks: dict[int, (Xyz, Xyz, set[int], set[int])] = {}  # id -> (end0, end1, foundation ids, dependent ids)
    height_map: dict[(int, int), (int, int)] = {}  # (x, y) -> (highest z on stack, id of highest brick)

    # loop over bricks sorted from lowest z to highest, letting them all fall down and stack up
    for bid, (x0, y0, z0), (x1, y1, z1) in sorted(snapshot, key=lambda b: min(b[1][2], b[2][2])):
        xmin, xmax = min(x0, x1), max(x0, x1)
        ymin, ymax = min(y0, y1), max(y0, y1)
        zmin, zmax = min(z0, z1), max(z0, z1)
        fz = 0  # foundation height
        foundation: set[int] = set()  # set of brick ids directly below the current brick

        # loop over the cubes making up each brick, looking at their xy projection to find the new target height
        for cx, cy in product(range(xmin, xmax + 1), range(ymin, ymax + 1)):
            mz, mfid = height_map.get((cx, cy), (-1, -1))
            if mz > fz:
                fz = mz
                foundation = {mfid}
            elif mz == fz:
                foundation.add(mfid)

        nzmin, nzmax = fz + 1, fz + (zmax - zmin) + 1
        bricks[bid] = ((xmin, ymin, nzmin), (xmax, ymax, nzmax), foundation, set())
        for cx, cy in product(range(xmin, xmax + 1), range(ymin, ymax + 1)):
            height_map[cx, cy] = (nzmax, bid)

    # update depending brick ids on top of each brick
    for bid, (xyz0, xyz1, foundation, dependent) in bricks.items():
        for fid in foundation:
            bricks[fid][3].add(bid)

    # find "redundant" bricks, for which all dependent bricks have at least one other foundation
    redundant_count = 0
    for bid, (xyz0, xyz1, foundation, dependent) in sorted(bricks.items(), key=lambda it: it[1][0][::-1]):
        if all(len(bricks[did][2]) > 1 for did in dependent):
            redundant_count += 1
        #     print(bid, xyz0, xyz1, "laying on", [*foundation], "supporting", [*dependent], "can be disintegrated")
        # else:
        #     print(bid, xyz0, xyz1, "laying on", [*foundation], "supporting", [*dependent], "is essential")

    print(f"A total of {redundant_count} individual bricks could be safely disintegrated.")


TEST_INPUT = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
