# Advent Of Code ${year}, day ${day}, part ${part}
# http://adventofcode.com/${year}/day/${day}
# solution by ByteCommander, ${date}
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    count = 0
    for line in file:
        if line.strip():
            count += 1
    print(f"The input contains {count} non-empty lines.")


TEST_INPUT = """
foo
bar
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
