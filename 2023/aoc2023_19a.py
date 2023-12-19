# Advent Of Code 2023, day 19, part 1
# http://adventofcode.com/2023/day/19
# solution by ByteCommander, 2023-12-18
import re
from collections.abc import Callable
from operator import gt, lt
from re import fullmatch
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    workflows: dict[str, list[(int, Callable[[int, int], bool], int, str)]] = {}  # name -> (var, comp, value, jump to)
    while line := file.readline().strip():  # read workflows until blank line
        name, wf_ = line.split("{")
        checks: list[(int, Callable[[int, int], bool], int, str)] = []
        *ch_strs, default = wf_[:-1].split(",")
        for ch_str in ch_strs:
            var_, comp_, val_, jmp = fullmatch(r"(\w+)([<>])(\d+):(\w+)", ch_str).groups()
            var = "xmas".index(var_)
            comp = gt if comp_ == ">" else lt
            val = int(val_)
            checks.append((var, comp, val, jmp))
        checks.append((None, None, None, default))
        workflows[name] = checks

    parts: list[(int, int, int, int)] = []  # [(x, m, a, s), ...]
    while line := file.readline().strip():  # read remaining part specs
        parts.append(tuple(map(int, re.fullmatch(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line).groups())))

    part_sum = 0
    for part in parts:
        wf = "in"
        while wf not in ("A", "R"):
            for var, comp, val, jmp in workflows[wf]:
                if var is None or comp(part[var], val):
                    wf = jmp
                    break
        if wf == "A":
            part_sum += sum(part)

    print(f"The sum of all accepted parts' ratings is {part_sum}.")


TEST_INPUT = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
