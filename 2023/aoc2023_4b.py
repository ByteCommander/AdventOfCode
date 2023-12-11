# Advent Of Code 2023, day 4, part 2
# http://adventofcode.com/2023/day/4
# solution by ByteCommander, 2023-12-11
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    cards: list[(int, int)] = []  # [amount of winning numbers on this card, how often this card gets copied]

    for line in file:
        _card_num, _all_nums = line.strip().split(":")
        _win_nums, _own_nums = _all_nums.strip().split("|")
        win_nums = set(map(int, _win_nums.split()))
        own_nums = set(map(int, _own_nums.split()))
        cards.append([len(win_nums & own_nums), 1])

    for i, card in enumerate(cards):
        wins, count = card
        if wins:
            for j in range(i + 1, i + 1 + wins):
                cards[j][1] += count

    total = sum(count for _, count in cards)
    print(f"You end up with {total} scratchcards in total.")


TEST_INPUT = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
