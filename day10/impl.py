#!/usr/bin/env python3
from collections import Counter
from itertools import islice
from os.path import dirname
import unittest


class PuzzleTest(unittest.TestCase):

    def test_first_example(self):
        self.assertEqual(35, puzzle([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))

    def test_second_example(self):
        example = [
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
            24, 23, 49, 45, 19, 38, 39, 11, 1, 32,
            25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
        ]
        self.assertEqual(220, puzzle(example))


def puzzle(adapters):
    jumps = [0] + sorted(adapters)
    jumps.append(jumps[-1] + 3)
    counts = Counter(
        higher - lower
        for lower, higher in zip(jumps, islice(jumps, 1, len(jumps)))
    )
    return counts[1] * counts[3]


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([int(line) for line in f.read().split()]))
