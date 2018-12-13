# Advent Of Code 2018, day 13, part 2
# http://adventofcode.com/2018/day/13
# solution by ByteCommander, 2018-12-13

DIRECTIONS = "^>v<"
TURNS = {
    ("/", "^"): ">", ("/", "v"): "<", ("/", "<"): "v", ("/", ">"): "^",
    ("\\", "^"): "<", ("\\", "v"): ">", ("\\", "<"): "^", ("\\", ">"): "v",
}
tracks = {}
carts = {}


class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn = -1
        carts[(self.y, self.x)] = self

    def move(self):
        try:
            carts.pop((self.y, self.x))
        except KeyError:
            return  # another cart crashed into us earlier in this tick

        track = tracks[(self.y, self.x)]
        if track == "+":
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) + self.turn) % 4]
            self.turn = (self.turn + 2) % 3 - 1
        elif track in "/\\":
            self.direction = TURNS.get((track, self.direction))

        if self.direction == "^":
            self.y -= 1
        elif self.direction == "v":
            self.y += 1
        elif self.direction == "<":
            self.x -= 1
        elif self.direction == ">":
            self.x += 1

        if (self.y, self.x) in carts:
            carts.pop((self.y, self.x))
        else:
            carts[(self.y, self.x)] = self


with open("inputs/aoc2018_13.txt") as file:
    for y, line in enumerate(file):
        for x, field in enumerate(line):
            if field in DIRECTIONS:
                Cart(x, y, field)
                field = "|" if field in "^v" else "-"
            if field != " ":
                tracks[(y, x)] = field

while len(carts) > 1:
    for _, cart in sorted(carts.items()):
        cart.move()

_, cart = carts.popitem()
print(f"The last remaining car is at {cart.x},{cart.y}")
