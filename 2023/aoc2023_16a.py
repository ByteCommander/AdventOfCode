# Advent Of Code 2023, day 16, part 1
# http://adventofcode.com/2023/day/16
# solution by ByteCommander, 2023-12-16
from enum import Flag, auto
from typing import TextIO

from aoc_tools.lib import run


class Dir(Flag):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


def main(file: TextIO):
    grid: list[list[str]] = [list(line.strip()) for line in file]

    start = 0, 0, Dir.E
    seen: set[(int, int, Dir)] = set()
    photons: list[(int, int, Dir)] = [start]  # stack of (y, x, direction)
    while photons:
        py, px, pd = photons.pop()
        if not (0 <= py < len(grid) and 0 <= px < len(grid[py])):
            continue  # photon left the grid
        # get output directions which haven't been processed already
        ph_dirs = shine(grid[py][px], pd)
        for ph_dir in ph_dirs:
            if (py, px, ph_dir) in seen:
                continue  # light went out of this tile in this direction already
            seen.add((py, px, ph_dir))
            match ph_dir:
                case Dir.N:
                    photons.append((py - 1, px, ph_dir))
                case Dir.S:
                    photons.append((py + 1, px, ph_dir))
                case Dir.W:
                    photons.append((py, px - 1, ph_dir))
                case Dir.E:
                    photons.append((py, px + 1, ph_dir))

    count = len(set((y, x) for y, x, d in seen))
    print(f"A total of {count} tiles have been energized.")


def shine(tile: str, dir_in: Dir) -> list[Dir]:
    match tile, dir_in:
        case [".", _] | ["|", (Dir.N | Dir.S)] | ["-", (Dir.E | Dir.W)]:
            return [dir_in]
        case ["|", (Dir.E | Dir.W)]:
            return [Dir.N, Dir.S]
        case ["-", (Dir.N | Dir.S)]:
            return [Dir.E, Dir.W]
        case ["/", Dir.E] | ["\\", Dir.W]:
            return [Dir.N]
        case ["/", Dir.W] | ["\\", Dir.E]:
            return [Dir.S]
        case ["/", Dir.N] | ["\\", Dir.S]:
            return [Dir.E]
        case ["/", Dir.S] | ["\\", Dir.N]:
            return [Dir.W]


TEST_INPUT = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
