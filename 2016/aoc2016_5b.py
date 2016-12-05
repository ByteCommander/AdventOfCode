# Advent Of Code 2016, day 5, part 2
# http://adventofcode.com/2016/day/5
# solution by ByteCommander, 2016-12-05

import hashlib

data = open("inputs/aoc2016_5.txt").read().strip()

md5 = hashlib.md5()
md5.update(data.encode())

keycode = ["-"] * 8
i = -1
while "-" in keycode:
    print("key: [{}]".format("".join(keycode)))
    print("calculating", end="", flush=True)
    while True:
        i += 1
        if i % 1000000 == 0:
            print(".", end="", flush=True)
        hasher = md5.copy()
        hasher.update(str(i).encode())
        digest = hasher.hexdigest()
        if digest.startswith("00000"):
            pos = int(digest[5], 16)
            if pos < 8 and keycode[pos] == "-":
                print(
                    "\nhashing '{}' gives '{}', so the key char at position {} is '{}'"
                    .format(data + str(i), digest, pos, digest[6]))
                keycode[pos] = digest[6]
                break
            else:
                print("x" if pos < 8 else "X", end="", flush=True)

print()
print("Answer: the door's key code is {}".format("".join(keycode)))
