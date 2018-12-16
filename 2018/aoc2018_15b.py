# Advent Of Code 2018, day 15, part 2
# http://adventofcode.com/2018/day/15
# solution by ByteCommander, 2018-12-15

print("#### WARNING - solution is not correct, work in progress #### #")  # FIXME

from collections import deque
from itertools import chain, count
from typing import Iterable, List, Set, Tuple

world: List[List["Field"]]
units: Set["Unit"]
DEBUG = False


def main():
    global world, units, DEBUG # todo

    with open("inputs/aoc2018_15.txt") as file:
        raw_world = file.readlines()

    xraw_world = [line.strip().split()[0] for line in """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
""".strip().splitlines()]

    for elf_strength in count(3): # todo
        print(f"Simulating combat with {elf_strength} strength points per elf...")

        world = []
        units = set()

        for y, line in enumerate(raw_world):
            row = []
            world.append(row)

            for x, char in enumerate(line):
                if char in "#.":
                    row.append(Field(char, x, y))
                elif char == "E":
                    row.append(Unit(char, x, y, elf_strength))
                elif char == "G":
                    row.append(Unit(char, x, y))

        r = None
        try:
            for r in count():
                # print_world("Round", r)
                for unit in sorted(units, key=lambda field: (field.y, field.x)):
                    if unit.hp:
                        unit.turn()

        except ElfDied:
            print_world("Lost map:")
            goblins = [unit for unit in units if unit.kind == "G"]
            goblin_hps = sum(goblin.hp for goblin in goblins)
            print(f"The first elf died after {r} rounds. There are {len(goblins)} "
                  f"goblins left with a total of {goblin_hps} health points.\n")

        except CombatEnded:
            print_world("Final map:")
            hps = sum(unit.hp for unit in units)
            print(f"With {elf_strength} strength points, the elves can just barely defeat "
                  f"the goblins without any losses.")
            print(f"It took them {r} rounds and they have a total of {hps} health points left.")
            print(f"Therefore the result is {r * hps}.")
            break
        break # todo


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


def compute_paths(target_adjacents: Iterable["Unit"]):
    # flood-fill free fields from all targets with minimal distance to self
    queue = deque()
    for field in target_adjacents:
        if not field:
            field.distance = 0
            field.closest = {field}
            queue.append(field)

    while queue:
        current: Field = queue.popleft()
        for field in current.adjacent:
            if not field:
                if field.distance is None or current.distance + 1 < field.distance:
                    field.distance = current.distance + 1
                    field.closest = current.closest
                    queue.append(field)
                elif field.distance == current.distance + 1:
                    field.closest.update(current.closest)
    if DEBUG: print_world()

def clear_paths():
    for row in world[1:-1]:
        for field in row[1:-1]:
            field.distance = None
            field.closest = None


class CombatEnded(Exception):
    pass


class ElfDied(Exception):
    pass


class Field:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.distance = None
        self.closest = None

    def __str__(self):
        return str(self.distance or self.kind)

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
    def __init__(self, kind: str, x: int, y: int, strength: int = 3):
        super().__init__(kind, x, y)
        self.hp = 200
        self.strength = strength
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
            # if self.kind == "E": # todo
            #    raise ElfDied()

    def turn(self):
        if DEBUG: print("My turn!", repr(self))
        # find targets
        targets: List[Unit] = [unit for unit in units if unit.kind != self.kind]
        if not targets:
            raise CombatEnded()

        # try to move if no target in own range
        if not any(self.is_enemy(adj) for adj in self.adjacent):

            compute_paths(chain(*(target.adjacent for target in targets)))
            # for a in self.adjacent:
            #     print("ADJ:", repr(a), a.distance, *map(repr, a.closest or ()))

            distance = min(
                (adj.distance for adj in self.adjacent if adj.distance is not None),
                default=None
            )
            # print(distance, *map(repr, set(chain(*(adj.closest or () for adj in self.adjacent)))))
            closest = set(chain(*(adj.closest or () for adj in self.adjacent if adj.distance == distance)))

            if DEBUG: print("Closest", *map(repr, closest))

            target_field: Field = min(
                closest,
                key=lambda field: (field.y, field.x),
                default=None
            )
            if DEBUG: print("Target field", repr(target_field))
            if target_field is None:
                clear_paths()
                return

            if DEBUG:
                for a in self.adjacent:
                    print("ADJ:", repr(a), a.distance, *map(repr, a.closest or ()))

            next_step: Field = min(
                (adj for adj in self.adjacent if adj.closest and target_field in adj.closest),
                key=lambda field: (field.distance, field.y, field.x)
            )
            if DEBUG: print("Next step", repr(next_step))

            self.swap_with(next_step)
            clear_paths()

        # attack if in range of enemy
        target: Unit = min(
            (adj for adj in self.adjacent if self.is_enemy(adj)),
            key=lambda enemy: (enemy.hp, enemy.y, enemy.x),
            default=None
        )
        if target:
            # print("Attacking", repr(target))
            target.take_damage(self.strength)


main()
