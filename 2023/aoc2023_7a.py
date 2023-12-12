# Advent Of Code 2023, day 7, part 1
# http://adventofcode.com/2023/day/7
# solution by ByteCommander, 2023-12-12
from collections import Counter
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    games: list[(int, int)] = []  # [(hand, bid), ...]
    for line in file:
        _hand, _bid = line.split()
        games.append((_hand, int(_bid)))

    games.sort(key=lambda g: (get_hand_type(g[0]), [get_card_value(c) for c in g[0]]))

    total = 0
    for rank, (hand, bid) in enumerate(games, 1):
        # print(f"{rank}: {hand} ({get_hand_type(hand)}, {[get_card_value(c) for c in hand]}), {bid} -> {rank * bid}")
        total += rank * bid

    print(f"The total winnings are {total} points.")


def get_hand_type(h: str) -> int:
    counts = Counter(h).most_common(2)  # [("card letter", count number), ...]
    match [count for _, count in counts]:
        case (5, ):
            return 6  # five of a kind
        case 4, _:
            return 5  # four of a kind
        case 3, 2:
            return 4  # full house
        case 3, _:
            return 3  # three of a kind
        case 2, 2:
            return 2  # two pairs
        case 2, _:
            return 1  # one pair
        case _:
            return 0  # high card


def get_card_value(c: str) -> int:
    if c.isdigit():
        return int(c)
    else:
        return "TJQKA".index(c) + 10


TEST_INPUT = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
