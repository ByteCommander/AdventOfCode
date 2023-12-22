# Advent Of Code 2023, day 22, part 2
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

    # find how many dependent bricks would fall as chain reaction when disintegrating each single brick
    fall_count = 0
    for bid, (_xyz0, _xyz1, _fnds, _deps) in bricks.items():
        falling: set[int] = {bid}
        fallen: set[int] = set()
        while falling:
            fall_id = falling.pop()
            fallen.add(fall_id)
            for dep_id in bricks[fall_id][3]:  # loop over immediately dependent brick ids
                if not bricks[dep_id][2] - fallen:  # check if dependent brick has no intact foundations left
                    falling.add(dep_id)
        fall_count += len(fallen) - 1  # count other fallen bricks in the chain reaction, excluding the initial one
        # print(bid, _xyz0, _xyz1, "supporting", [*_deps], "causes a chain reaction of", len(fallen) - 1)

    print(f"The sum of other bricks falling as chain reaction of removing any single brick is {fall_count}.")


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
