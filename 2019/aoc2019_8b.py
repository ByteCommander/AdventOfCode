# Advent Of Code 2019, day 8, part 2)
# http://adventofcode.com/2019/day/8
# solution by ByteCommander, 2019-12-08

WIDTH = 25
HEIGHT = 6


def main():
    with open("inputs/aoc2019_8.txt") as file:
        data = file.read().strip()
        layers = [[
            data[(offset := l * WIDTH * HEIGHT + h * WIDTH): offset + WIDTH]
            for h in range(HEIGHT)]
            for l in range(len(data) // WIDTH // HEIGHT)
        ]

    pixels = [list(zip(*row)) for row in zip(*layers)]

    print("Below is the decoded pixel message:\n")
    for row in pixels:
        print("".join(next(" #"[int(layer)] for layer in col if layer != "2") for col in row))


if __name__ == "__main__":
    main()
