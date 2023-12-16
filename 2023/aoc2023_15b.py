# Advent Of Code 2023, day 15, part 2
# http://adventofcode.com/2023/day/15
# solution by ByteCommander, 2023-12-16
from functools import reduce
from operator import setitem
from re import fullmatch
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    boxes: list[dict[str, int]] = [{} for _ in range(256)]

    for step in file.read().strip().split(","):
        label, op_sign, focal_str = fullmatch(r"(\w+)([=-])(\d?)", step).groups()
        if op_sign == "=":
            box_op = lambda bx, lbl, f=int(focal_str): setitem(bx, lbl, f)
        else:
            box_op = lambda bx, lbl: bx.pop(lbl) if lbl in bx else None

        box_num = reduce(lambda n, ch: ((n + ord(ch)) * 17) % 256, label, 0)
        box = boxes[box_num]
        box_op(box, label)
        # print(f"After '{step}':", *[f"Box {bi}: {b}" for bi, b in enumerate(boxes) if b], "", sep="\n")

    foc_power = sum(bn1 * ln1 * f for bn1, box in enumerate(boxes, 1) for ln1, f in enumerate(box.values(), 1))

    print(f"The total focusing power of the lens configuration is {foc_power}.")


TEST_INPUT = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
