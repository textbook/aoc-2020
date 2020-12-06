#!/usr/bin/env python3
from os.path import dirname
from textwrap import dedent
import unittest


class PuzzleTest(unittest.TestCase):
    example = dedent("""
        abc
    
        a
        b
        c
        
        ab
        ac
        
        a
        a
        a
        a
        
        b
    """.strip())

    def test_puzzle(self):
        self.assertEqual(puzzle(self.example), 6)


def puzzle(data):
    total = 0
    for group in data.split("\n\n"):
        people = group.split()
        answers = set(people[0])
        for person in people[1:]:
            answers.intersection_update(person)
        total += len(answers)
    return total


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
