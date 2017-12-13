# Advent Of Code 2017, day 13, part 1
# http://adventofcode.com/2017/day/13
# solution by ByteCommander, 2017-12-13


class Layer:
    def __init__(self, depth, scan_range):
        self.depth = depth
        self.scan_range = scan_range
        self.scanner_pos = 0
        self.scan_forward = True

    def scan(self):
        if self.scan_forward and self.scanner_pos == self.scan_range - 1:
            self.scan_forward = False
        elif not self.scan_forward and self.scanner_pos == 0:
            self.scan_forward = True
        self.scanner_pos += 1 if self.scan_forward else -1

    def get_severity(self):
        return self.depth * self.scan_range


def main():
    with open("inputs/aoc2017_13.txt") as file:
        layers = {}

        for line in file:
            depth, scan_range = map(int, line.split(": "))
            layers[depth] = Layer(depth, scan_range)

        max_depth = max(layers)
        depth = -1
        severity = 0
        while depth < max_depth:
            depth += 1
            layer = layers.get(depth, None)
            if layer and layer.scanner_pos == 0:
                severity += layer.get_severity()
            for l in layers.values():
                l.scan()

        print("Answer: The trip's severity would be {}."
              .format(severity))


main()
