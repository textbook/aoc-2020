#!/usr/bin/env python3
from collections import defaultdict
from os.path import dirname
import re
from textwrap import dedent
import unittest


class PuzzleTest(unittest.TestCase):

    example = dedent("""
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
    """.strip())

    def test_puzzle(self):
        self.assertEqual(puzzle(self.example, "shiny gold"), 4)


def puzzle(rules, start):
    containers = create_container_map(rules)
    valid = set()
    to_visit = [start]
    while to_visit:
        for container in containers[to_visit.pop()]:
            if container not in valid:
                valid.add(container)
                to_visit.append(container)
    return len(valid)


def create_container_map(rules):
    """Create mapping from bags to the bags that can contain them."""
    containers = defaultdict(set)
    for rule in rules.split("\n"):
        bags = re.findall(r"(\w+ \w+) bags?", rule)
        for bag in bags[1:]:
            containers[bag].add(bags[0])
    return containers


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip(), "shiny gold"))
