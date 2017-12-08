# Advent Of Code 2017, day 7, part 2
# http://adventofcode.com/2017/day/7
# solution by ByteCommander, 2017-12-07

import re
from collections import Counter


class Node:
    def __init__(self, name, weight, children_names):
        self.name = name
        self.weight = weight
        self.children_names = children_names
        self.children = []

    def insert(self, ins_node):
        for child_name in self.children_names:
            if ins_node.name == child_name:
                self.children_names.remove(child_name)
                self.children.append(ins_node)
                return True
        for child in self.children:
            if child.insert(ins_node):
                return True
        return False

    def get_total_weight(self):
        return sum([child.get_total_weight() for child in self.children]) + self.weight

    def is_balanced(self):
        return len(set(child.get_total_weight() for child in self.children)) <= 1

    def get_recursive(self):
        return [self] + sum((child.get_recursive() for child in self.children), [])

    def __str__(self):
        return "{} ({}/{})".format(self.name, self.weight, self.get_total_weight())

    def __repr__(self):
        return "{} ({}/{}): [{}] <{}>".format(self.name, self.weight, self.get_total_weight(),
                                              ", ".join(map(repr, self.children)),
                                              ", ".join(map(repr, self.children_names)))


def make_trees():
    trees = set()

    for line in file:
        match = re.fullmatch(r"(\w+) \((\d+)\)(?: -> ((?:\w+(?:, )?)*))?", line.strip())
        name_, weight_, children_names_ = match.groups()
        node = Node(name_, int(weight_), children_names_.split(", ") if children_names_ else [])

        inserted = False
        # try using node as root for existing tree
        for root in list(trees):
            if root.name in node.children_names:
                node.children_names.remove(root.name)
                node.children.append(root)
                trees.remove(root)
                trees.add(node)
                inserted = True

        # try inserting node as child into a tree
        for tree in list(trees):
            if tree.insert(node):
                if node in trees:
                    trees.remove(node)
                break
        else:
            # try adding node as new separate tree root
            if not inserted:
                trees.add(node)

    return trees


if __name__ == "__main__":
    with open("inputs/aoc2017_7.txt") as file:
        my_trees = make_trees()
        if len(my_trees) != 1:
            print("ERROR! More than one root!")
        root = my_trees.pop()
        nodes = root.get_recursive()

        ws = [n.children for n in nodes if not n.is_balanced()]
        bad_nodes = ws[-1]
        weights = [ctr_item[0] for ctr_item in Counter(map(Node.get_total_weight, bad_nodes)).most_common()]
        good_weight, bad_weight = weights[0], weights[-1]
        bad_node = [bn for bn in bad_nodes if bn.get_total_weight() == bad_weight][0]

    print("Answer: {} is the correct weight."
          .format(bad_node.weight - bad_weight + good_weight))
