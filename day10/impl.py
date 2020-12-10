#!/usr/bin/env python3
from os.path import dirname
import unittest


class PuzzleTest(unittest.TestCase):

    def test_first_example(self):
        self.assertEqual(8, puzzle([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))

    def test_second_example(self):
        example = [
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
            24, 23, 49, 45, 19, 38, 39, 11, 1, 32,
            25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
        ]
        self.assertEqual(19208, puzzle(example))


def memoize(func):
    def wrapper(*args):
        if args not in wrapper.cache:
            wrapper.cache[args] = func(*args)
        return wrapper.cache[args]
    wrapper.cache = {}
    return wrapper


def puzzle(adapters):
    last = max(adapters)
    adapters = set(adapters)

    @memoize
    def paths(start=0):
        if start == last:
            return 1
        return sum((
            paths(start + step)
            for step in (1, 2, 3)
            if start + step in adapters
        ))

    return paths()


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([int(line) for line in f.read().split()]))
