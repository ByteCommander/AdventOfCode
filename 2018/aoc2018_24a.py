# Advent Of Code 2018, day 24, part 1
# http://adventofcode.com/2018/day/24
# solution by ByteCommander, 2018-12-24

import re

groups = []


class Group:
    def __init__(self, group_id, party, number, health, immunities, weaknesses, attack, attack_type, initiative):
        self.group_id = group_id
        self.party = party
        self.number = int(number)
        self.health = int(health)
        self.immunities = immunities.split(", ") if immunities else []
        self.weaknesses = weaknesses.split(", ") if weaknesses else []
        self.attack = int(attack)
        self.attack_type = attack_type
        self.initiative = int(initiative)

    def __repr__(self):
        return f"<{self.party} [{self.group_id}] ({self.number} units)"

    @property
    def effective_power(self):
        return self.number * self.attack

    def calculate_damage(self, power, attack_type):
        if attack_type in self.immunities:
            return 0
        elif attack_type in self.weaknesses:
            return power * 2
        else:
            return power

    def take_damage(self, damage):
        self.number -= damage // self.health
        if self.number <= 0:
            self.number = 0
            # print(self, "got defeated!")
            groups.remove(self)


with open("inputs/aoc2018_24.txt") as file:
    party = ""
    group_id = None
    for line in file:
        line = line.strip()
        if line in ("Immune System:", "Infection:"):
            party = line.rstrip(":")
            group_id = 1
        elif line:
            match = re.match(
                r"(\d+) units each with (\d+) hit points "
                r"(?:\((?:immune to ([\w, ]+)(?:; )?|weak to ([\w, ]+)(?:; )?)+\) )?"
                r"with an attack that does (\d+) (\w+) damage at initiative (\d+)",
                line
            )
            groups.append(Group(group_id, party, *match.groups()))
            group_id += 1

while len(set(group.party for group in groups)) > 1:
    matched = {}

    for challenger in sorted(groups, key=lambda group: (group.effective_power, group.initiative), reverse=True):
        challenged = max(
            (group for group in groups if group.party != challenger.party and group not in matched.values()),
            key=lambda group: (
                group.calculate_damage(challenger.effective_power, challenger.attack_type),
                group.effective_power,
                group.initiative
            ),
            default=None
        )
        if challenged and challenged.calculate_damage(challenger.effective_power, challenger.attack_type) > 0:
            matched[challenger] = challenged

    while matched:
        attacker = max(matched.keys(), key=lambda group: group.initiative)
        defender = matched.pop(attacker)
        if defender:
            damage = defender.calculate_damage(attacker.effective_power, attacker.attack_type)
            # print(f"{attacker} attacks {defender} for {damage} damage ({damage // defender.health} kills).")
            defender.take_damage(damage)
        # else: print(f"{attacker} skips a turn")

    # print("Round over...\n")

winning_party = next(group.party for group in groups)
remaining_units = sum(group.number for group in groups)

print(f"After the battle, the {winning_party} has {remaining_units} units left.")
