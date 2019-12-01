# Advent Of Code 2018, day 24, part 1
# http://adventofcode.com/2018/day/24
# solution by ByteCommander, 2018-12-24
import itertools
import re

groups = []


class Group:
    def __init__(self, group_id, party, boost, number, health, immunities, weaknesses, attack, attack_type, initiative):
        self.group_id = group_id
        self.party = party
        self.number = int(number)
        self.health = int(health)
        self.immunities = immunities.split(", ") if immunities else []
        self.weaknesses = weaknesses.split(", ") if weaknesses else []
        self.attack = int(attack) + (boost if party == "Immune System" else 0)
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
    lines = file.readlines()
alines = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".strip().splitlines()

for boost in itertools.count():
    groups.clear()
    party = ""
    group_id = None
    for line in lines:
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
            groups.append(Group(group_id, party, boost, *match.groups()))
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

        if not matched:
            print("No more attacks possible, this is a tie.")
            break

        while matched:
            attacker = max(matched.keys(), key=lambda group: group.initiative)
            defender = matched.pop(attacker)
            if defender:
                damage = defender.calculate_damage(attacker.effective_power, attacker.attack_type)
                # print(f"{attacker} attacks {defender} for {damage} damage ({damage // defender.health} kills).")
                defender.take_damage(damage)
            # else: print(f"{attacker} skips a turn")

        # print("Combat round over...\n")

    winning_party = next(group.party for group in groups)
    if winning_party == "Immune System":
        break
    elif boost % 1 == 0:
        remaining_units = sum(group.number for group in groups)
        print(f"Battle lost with a boost of {boost}, the {winning_party} has {remaining_units} units left.")

print(f"After the battle with a boost of {boost}, the {winning_party} has {remaining_units} units left.")
