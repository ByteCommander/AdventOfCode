# Advent Of Code $<YEAR>$, day $<DAY>$, part $<PART>$)
# http://adventofcode.com/$<YEAR>$/day/$<DAY>$
# solution by ByteCommander, $<DATE>$


def main():
    with open("inputs/aoc$<YEAR>$_$<DAY>$.txt") as file:
        s = file.read().strip()
        print(sum(int(c) for c, n in zip(s, s[1:] + s[:1]) if c == n))


if __name__ == "__main__":
    main()
