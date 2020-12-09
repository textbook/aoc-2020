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
        self.assertEqual(62, puzzle(self.example, 5))


def is_valid(target, window):
    """Whether target is the sum of any two numbers in the window."""
    return any(a + b == target for a, b in combinations(window, 2))


def invalid_value(data, preamble):
    """Get the first invalid value in data."""
    for index in range(len(data)):
        value = data[index + preamble]
        if not is_valid(value, islice(data, index, index + preamble)):
            return value


def puzzle(data, preamble):
    target = invalid_value(data, preamble)
    for index in range(len(data)):
        for length in range(0, len(data) - index):
            if sum(data[i] for i in range(index, index + length)) == target:
                return (
                    min(data[i] for i in range(index, index + length))
                    + max(data[i] for i in range(index, index + length))
                )


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([int(line) for line in f.read().split()], 25))
