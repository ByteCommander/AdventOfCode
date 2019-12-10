# Advent Of Code 2019, day 10, part 1)
# http://adventofcode.com/2019/day/10
# solution by ByteCommander, 2019-12-10
import math
from fractions import Fraction
from itertools import combinations


def main():
    with open("inputs/aoc2019_10.txt") as file:
        grid = [[char == "#" for char in line] for line in file]

    asteroids = [(x, y) for y, row in enumerate(grid) for x, asteroid in enumerate(row) if asteroid]
    views = {}

    for (x1, y1), (x2, y2) in combinations(asteroids, 2):
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 or dy == 0:  # edge case: straight horizontal/vertical line
            dx0, dy0 = dx and 1, dy and 1
        else:  # any diagonal, representable as a x/y fraction
            dx0, dy0 = Fraction(dx, dy).as_integer_ratio()
            dx0, dy0 = math.copysign(dx0, dx), math.copysign(dy0, dy)
        # print("\nfor", (x1, y1), "dir", (dx0, dy0), "to", (x2, y2))
        f = 1
        while ((x := x1 + dx0 * f) != x2) + ((y := y1 + dy0 * f) != y2):  # non-short-circuit and
            # print("testing", (x, y))
            if (x, y) in asteroids:
                # print("block", (x1, y1), (x2, y2))
                break  # other asteroid blocking direct line of sight
            f += 1
        else:  # free sight between asteroids
            # print("line", (x1, y1), (x2, y2))
            views[(x1, y1)] = views.get((x1, y1), 0) + 1
            views[(x2, y2)] = views.get((x2, y2), 0) + 1

    # print(asteroids)
    # print(views)
    # for y in range(max(yy for xx, yy in asteroids) + 1):
    #     print("".join(views.get((x, y), ".") for x in range(max(xx for xx, yy in asteroids) + 1)))

    best_asteroid, best_views = max(views.items(), key=lambda kv: kv[1])
    print(f"The optimal asteroid at coordinates {best_asteroid} can see {best_views} others.")


if __name__ == "__main__":
    main()
