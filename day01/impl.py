#!/usr/bin/env python3
from functools import reduce
from itertools import combinations
from operator import mul
from os.path import dirname
import unittest


class PuzzleTests(unittest.TestCase):

    input = [1721, 979, 366, 299, 675, 1456]

    def test_example_pairs(self):
        self.assertEqual(puzzle(self.input, 2), 514579)

    def test_example_triples(self):
        self.assertEqual(puzzle(self.input, 3), 241861950)


def product(values):
    """Calculate the product of the values."""
    return reduce(mul, values, 1)


def puzzle(numbers, count):
    """Find the product of the numbers that sum to 2020."""
    for combination in combinations(numbers, count):
        if sum(combination) == 2020:
            return product(combination)
    raise ValueError("no combination found")


if __name__ == "__main__":
    import sys
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([
            int(line.strip())
            for line in f.readlines()
        ], int(sys.argv[1])))

