# Advent Of Code 2018, day 23, part 2
# http://adventofcode.com/2018/day/23
# solution by ByteCommander, 2018-12-23

import re
from itertools import combinations_with_replacement, combinations
from math import log

bots = []

with open("inputs/aoc2018_23.txt") as file:
    xfile = """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""".strip().splitlines()
    for line in file:
        x, y, z, r = map(int, re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line).groups())
        bots.append((r, x, y, z))

rmin, *_, rmax = sorted(r for r, x, y, z in bots)
xmin, *_, xmax = sorted(x for r, x, y, z in bots)
ymin, *_, ymax = sorted(y for r, x, y, z in bots)
zmin, *_, zmax = sorted(z for r, x, y, z in bots)


def count_in_range(*xyz):
    return sum(1 for br, *bxyz in bots if sum(abs(c1 - c2) for c1, c2 in zip(xyz, bxyz)) <= br)


def coords_in_sphere(x, y, z, max_r):
    yield x, y, z
    for r in range(1, max_r + 1):
        for dx, dy, dz in combinations_with_replacement((-r, 0, r), 3):
            yield x + dx, y + dy, z + dz


# for w, r, x, y, z in sorted((r/rsum, r, x, y, z) for r, x, y, z in bots):
#    print(f"x={w*x:10.0f},  y={w*y:10.0f},  z={w*z:10.0f},  r={w*r:10.0f},  w={w*1000:5.2f}m")

# center of mass, assuming sqrt(radius) == mass
rsum = sum(log(r) for r, x, y, z in bots)
xm, ym, zm = [int(round(sum(bot[coord] * log(bot[0]) / rsum for bot in bots))) for coord in (1, 2, 3)]
print(xm, ym, zm)

# unweighted center/average
xc, yc, zc = [int(round(sum(bot[coord] for bot in bots) / len(bots))) for coord in (1, 2, 3)]
print(xc, yc, zc)

# print(*list(coords_in_sphere(0, 0, 0, 3)), sep="\n")

yes, no = [], []
for (r1, *xyz1), (r2, *xyz2) in combinations(bots, 2):
    if sum(abs(c1 - c2) for c1, c2 in zip(xyz1, xyz2)) <= r1 + r2:
        yes.append((r1, *xyz1, r2, *xyz2))
    else:
        no.append((r1, *xyz1, r2, *xyz2))

print(len(yes), len(no))