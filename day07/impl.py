#!/usr/bin/env python3
from collections import defaultdict
from os.path import dirname
import re
from textwrap import dedent
import unittest


class PuzzleTest(unittest.TestCase):

    def test_example_1(self):
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
        self.assertEqual(puzzle(example, "shiny gold"), 32)

    def test_example_2(self):
        example = dedent("""
            shiny gold bags contain 2 dark red bags.
            dark red bags contain 2 dark orange bags.
            dark orange bags contain 2 dark yellow bags.
            dark yellow bags contain 2 dark green bags.
            dark green bags contain 2 dark blue bags.
            dark blue bags contain 2 dark violet bags.
            dark violet bags contain no other bags.
        """.strip())
        self.assertEqual(puzzle(example, "shiny gold"), 126)


def puzzle(rules, start):
    containers = create_container_map(rules)
    total = 0
    to_visit = [start]
    while to_visit:
        visiting = to_visit.pop()
        for container, count in containers[visiting].items():
            total += count
            to_visit.extend([container] * count)
    return total


def create_container_map(rules):
    """Create mapping from bags to the bags that they can contain."""
    containers = defaultdict(dict)
    for rule in rules.split("\n"):
        start, = re.findall(r"(\w+ \w+) bags contain", rule)
        contained = re.findall(r"(\d+) (\w+ \w+) bags?", rule)
        for number, bag in contained:
            containers[start][bag] = int(number)
    return containers


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip(), "shiny gold"))
