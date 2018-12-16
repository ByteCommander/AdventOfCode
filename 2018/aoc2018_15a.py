# Advent Of Code 2018, day 15, part 1
# http://adventofcode.com/2018/day/15
# solution by ByteCommander, 2018-12-15

print("#### WARNING - solution is not correct, work in progress #### #")  # FIXME

from collections import deque
from itertools import count
from math import inf
from typing import List, Set, Tuple

world: List[List["Field"]] = []
units: Set["Unit"] = set()


def main():
    with open("inputs/aoc2018_15.txt") as file:
        file = """
######
#.G..#
#...E#
#E...#
######
""".strip().splitlines()
        for y, line in enumerate(file):
            row = []
            world.append(row)

            for x, char in enumerate(line):
                if char in "#.":
                    row.append(Field(char, x, y))
                elif char in "EG":
                    row.append(Unit(char, x, y))

    r = None
    try:
        for r in count():
            print_world("Round", r)
            for unit in sorted(units, key=lambda field: (field.y, field.x)):
                if unit.hp:
                    unit.turn()

    except CombatEnded:
        print_world("Final map:")
        hps = sum(unit.hp for unit in units)
        print(f"Combat ended after {r} rounds. There are {len(units)} surviving",
              "elves" if next(iter(units)).kind == "E" else "goblins",
              f"left, with a total of {hps} health points.")
        print(f"Therefore the result is {r * hps}.")


def print_world(*args):
    if args:
        print(*args)
    for row in world:
        print(
            "".join(str(field) for field in row),
            ", ".join(f"{unit.kind}({unit.hp})" for unit in row if isinstance(unit, Unit)),
            sep="\t\t"
        )
    print()


def flood_distances(targets: List["Unit"]):
    # flood-fill free fields from all targets with minimal distance to self
    queue = deque()
    for target in targets:
        target.temp_distance = 0
        queue.append(target)

    while queue:
        current: Field = queue.popleft()
        for field in current.adjacent:
            if not field:
                if field.temp_distance is None:
                    field.temp_distance = current.temp_distance + 1
                    queue.append(field)
                elif field.temp_distance > current.temp_distance + 1:
                    field.temp_distance = current.temp_distance + 1


def clear_distances():
    for row in world[1:-1]:
        for field in row[1:-1]:
            field.temp_distance = None


class CombatEnded(Exception):
    pass


class Field:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.temp_distance = None

    def __str__(self):
        return str(self.temp_distance or self.kind)

    def __repr__(self):
        return f"<|{self.kind}| (x={self.x} y={self.y})>"

    def __bool__(self):
        return self.kind != "."

    @property
    def adjacent(self) -> Tuple["Field", "Field", "Field", "Field"]:
        return (
            world[self.y - 1][self.x],
            world[self.y][self.x - 1],
            world[self.y][self.x + 1],
            world[self.y + 1][self.x]
        )


class Unit(Field):
    def __init__(self, kind: str, x: int, y: int):
        super().__init__(kind, x, y)
        self.hp = 200
        units.add(self)

    def __repr__(self):
        return super().__repr__()[:-1] + f" HP={self.hp:3} adj=({''.join(map(str, self.adjacent))})>"

    def is_enemy(self, field: Field):
        return isinstance(field, Unit) and self.kind != field.kind

    def swap_with(self, field: Field):
        world[field.y][field.x] = self
        world[self.y][self.x] = field
        field.x, field.y, self.x, self.y = self.x, self.y, field.x, field.y

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            # print(repr(self), "died!")
            self.hp = 0
            units.discard(self)
            world[self.y][self.x] = Field(".", self.x, self.y)

    def turn(self):
        # print(repr(self), "My turn!")

        # find targets
        targets: List[Unit] = [unit for unit in units if unit.kind != self.kind]
        if not targets:
            raise CombatEnded()
        # print("Targets:", targets)

        # if not in range of an enemy: try to move
        if not any(self.is_enemy(adj) for adj in self.adjacent):
            # calculate the minimum distance of each field to its closest target
            flood_distances(targets)

            # find field adjacent to self on shortest path to next target
            next_step: Unit = min(
                filter(lambda field: field.temp_distance is not None, self.adjacent),
                key=lambda field: (field.temp_distance or inf, field.y, field.x),
                default=None
            )
            clear_distances()

            if next_step is not None:
                # print("Moving to:", repr(next_step))
                self.swap_with(next_step)

        # attack if in range of enemy
        target: Unit = min(
            (adj for adj in self.adjacent if self.is_enemy(adj)),
            key=lambda enemy: (enemy.hp, enemy.y, enemy.x),
            default=None
        )
        if target:
            # print("Attacking", repr(target))
            target.take_damage(3)


main()
