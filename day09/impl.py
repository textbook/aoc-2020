#!/usr/bin/env python3
from itertools import combinations, islice
from os.path import dirname
import unittest


class PuzzleTest(unittest.TestCase):

    example = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
    ]

    def test_puzzle(self):
        self.assertEqual(127, puzzle(self.example, 5))


def is_valid(target, window):
    """Whether target is the sum of any two numbers in the window."""
    return any(a + b == target for a, b in combinations(window, 2))


def puzzle(data, preamble):
    index = 0
    while True:
        value = data[index + preamble]
        if not is_valid(value, islice(data, index, index + preamble)):
            return value
        index += 1


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([int(line) for line in f.read().split()], 25))
