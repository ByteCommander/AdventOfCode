# Advent Of Code 2017, day 7, part 1
# http://adventofcode.com/2017/day/7
# solution by ByteCommander, 2017-12-07

import re


class Node:
    def __init__(self, name, weight, children_names):
        self.name = name
        self.weigth = weight
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

    def __str__(self):
        return "{} ({})".format(self.name, self.weigth)

    def __repr__(self):
        return "{} ({}): [{}] <{}>".format(
            self.name, self.weigth, ", ".join(map(repr, self.children)), ", ".join(map(repr, self.children_names)))


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

    print("Answer: {} is the root program."
          .format([str(tree) for tree in my_trees]))
