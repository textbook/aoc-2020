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
        self.assertEqual(puzzle(self.example), 11)


def puzzle(data):
    total = 0
    for group in data.split("\n\n"):
        answers = set()
        for person in group.split():
            answers.update(person)
        total += len(answers)
    return total


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
