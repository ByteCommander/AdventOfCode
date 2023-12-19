# Advent Of Code 2023, day 19, part 2
# http://adventofcode.com/2023/day/19
# solution by ByteCommander, 2023-12-18
from math import prod
from re import fullmatch
from typing import TextIO

from aoc_tools.lib import run

type Workflow = (int | None, bool | None, int | None, str)  # var index (xmas), greater?, value, jump target
type XmasRange = ((int, int), (int, int), (int, int), (int, int))  # (x min-max), (m min-max), (a min-max), (s min-max)


def main(file: TextIO):
    workflows: dict[str, list[Workflow]] = {}  # name -> wf
    while line := file.readline().strip():  # read workflows until blank line
        name, wf_ = line.split("{")
        checks: list[Workflow] = []
        *ch_strs, default = wf_[:-1].split(",")
        for ch_str in ch_strs:
            var_, gt_, val_, jmp = fullmatch(r"(\w+)([<>])(\d+):(\w+)", ch_str).groups()
            var = "xmas".index(var_)
            gt = gt_ == ">"
            val = int(val_)
            checks.append((var, gt, val, jmp))
        checks.append((None, None, None, default))
        workflows[name] = checks

    branches: list[(str, XmasRange)] = [("in", ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))]
    accepted = 0
    while branches:
        branch = branches.pop()
        # print(branch)
        wf, xmas_range = branch
        if wf == "A":
            accepted += (acc := prod(b - a + 1 for a, b in xmas_range))
            # print("accepted", xmas_range, acc)
        elif wf != "R":
            for var, gt, val, jmp in workflows[wf]:
                # print("checking", (var, gt, val, jmp), "against", xmas_range)
                if var is None:  # unconditional jump i.e. end of this workflow's checks reached
                    branches.append((jmp, xmas_range))
                    break
                else:
                    split_val = val + 1 if gt else val  # first inclusive index of higher range
                    lower_range, higher_range = split_range(xmas_range, var, split_val)
                    true_range, false_range = (higher_range, lower_range) if gt else (lower_range, higher_range)
                    if true_range:  # add branch for matching range segment at jump target
                        branches.append((jmp, true_range))
                        # print("true ->", jmp, true_range)
                    if false_range:  # continue evaluating checks of this workflow with the remaining range segment
                        xmas_range = false_range
                        # print("false ->", false_range)
                    else:  # no range segment left for remaining checks, so this workflow step is finished
                        break
        # else:
        #     print("rejected")

    print(f"A total number of {accepted} distinct parts can be accepted.")


def split_range(old_range: XmasRange, var_index: int, value: int) -> (XmasRange | None, XmasRange | None):
    """
    Split an XmasRange into zero to two segments (lower, higher), based on the split value for the given var_index.
    :param old_range: the input XmasRange to split up
    :param var_index: index of the variable range to operate on (0 to 3 matching x,m,a,s)
    :param value: the value at which to split the range, so that lower < value and higher >= value
    :return: tuple of lower range and higher range, where either of them could be None
    """
    vmin, vmax = old_range[var_index]
    var_ranges = (
        (vmin, min(vmax, value - 1)) if vmin < value else None,  # range segment below value (exclusive)
        (max(vmin, value), vmax) if vmax >= value else None  # range segment above value (inclusive)
    )
    return tuple(
        tuple(v_range if i == var_index else old_range[i] for i in range(4)) if v_range else None
        for v_range in var_ranges
    )


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
