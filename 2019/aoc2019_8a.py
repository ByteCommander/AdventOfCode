# Advent Of Code 2019, day 8, part 1)
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

    fewest_zeroes_layer = min(
        ("".join(layer) for layer in layers), key=lambda layer: layer.count("0")
    )
    checksum = fewest_zeroes_layer.count("1") * fewest_zeroes_layer.count("2")
    print(f"The checksum of the layer with fewest zeroes is {checksum}.")


if __name__ == "__main__":
    main()
