#!/usr/bin/env python3
import re
from os.path import dirname
from textwrap import dedent
from unittest import TestCase

RANGES = re.compile(r"(\d+)-(\d+)")


def puzzle(example):
    rules, _, nearby = example.split("\n\n")
    valid_numbers = extract_valid_numbers(rules)
    return sum(
        value
        for value in map(lambda g: int(g.group(0)), re.finditer(r"\d+", nearby))
        if value not in valid_numbers
    )


def extract_valid_numbers(rules):
    valid_numbers = set()
    for rule in RANGES.finditer(rules):
        start, end = map(int, rule.groups())
        valid_numbers.update(range(start, end + 1))
    return valid_numbers


class PuzzleTests(TestCase):

    example = dedent("""
        class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50
        
        your ticket:
        7,1,14
        
        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12
    """).strip()

    def test_puzzle(self):
        self.assertEqual(71, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
