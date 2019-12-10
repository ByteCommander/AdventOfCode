# Advent Of Code 2019, day 10, part 2)
# http://adventofcode.com/2019/day/10
# solution by ByteCommander, 2019-12-10
import math
from fractions import Fraction

x1, y1 = 20, 20  # coordinates taken from output of part 1


def main():
    with open("inputs/aoc2019_10.txt") as file:
        grid = [[char == "#" for char in line] for line in file]

    asteroids = [(x, y) for y, row in enumerate(grid) for x, asteroid in enumerate(row) if asteroid]
    asteroids.remove((x1, y1))  # our location
    counter = 0

    while asteroids:
        visible = scan(asteroids)
        for angle, (x, y) in sorted(visible.items()):
            asteroids.remove((x, y))
            counter += 1
            # print(counter, angle, (x, y))
            if counter == 200:
                print(f"The 200th asteroid to eliminate is at {(x, y)}, resulting in code {x * 100 + y}.")
                break
        else:
            continue
        break


def scan(asteroids):
    visible = {}  # angle: coords

    for x2, y2 in asteroids:
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 or dy == 0:  # edge case: straight horizontal/vertical line
            dx0, dy0 = dx and 1, dy and 1
        else:  # any diagonal, representable as a x/y fraction
            dx0, dy0 = Fraction(dx, dy).as_integer_ratio()
        dx0, dy0 = int(math.copysign(dx0, dx)), int(math.copysign(dy0, dy))  # fix signs
        # print("\nfor", (x1, y1), "dir", (dx0, dy0), "to", (x2, y2))
        f = 1
        while ((x := x1 + dx0 * f) != x2) + ((y := y1 + dy0 * f) != y2):  # non-short-circuit and
            # print("testing", (x, y))
            if (x, y) in asteroids:
                # print("block", (x1, y1), (x2, y2))
                break  # other asteroid blocking direct line of sight
            f += 1
            if f > 100: raise RuntimeError()
        else:  # free sight between asteroids
            # print("line", (x1, y1), (x2, y2))
            visible[math.degrees(math.atan2(dx0, -dy0)) % 360] = (x2, y2)

    return visible


if __name__ == "__main__":
    main()
