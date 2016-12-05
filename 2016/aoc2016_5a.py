# Advent Of Code 2016, day 5, part 1
# http://adventofcode.com/2016/day/5
# solution by ByteCommander, 2016-12-05

import hashlib

data = open("inputs/aoc2016_5.txt").read().strip()

md5 = hashlib.md5()
md5.update(data.encode())

keycode = ""
i = -1
while len(keycode) < 8:
    print("# char {}/8 ".format(len(keycode) + 1), end="", flush=True)
    while True:
        i += 1
        if i % 1000000 == 0:
            print(".", end="", flush=True)
        hasher = md5.copy()
        hasher.update(str(i).encode())
        digest = hasher.hexdigest()
        if digest.startswith("00000"):
            print("\nhashing '{}' gives '{}', so the key char is '{}'".format(
                data + str(i), digest, digest[5]))
            keycode += digest[5]
            break

print()
print("Answer: the door's key code is {}".format(keycode))
