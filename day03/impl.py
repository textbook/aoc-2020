#!/usr/bin/env python3
from functools import reduce
from operator import mul
from os.path import dirname
from textwrap import dedent
import unittest


class PuzzleTest(unittest.TestCase):

    example = dedent("""
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#
    """).strip()

    def test_check_slope(self):
        self.assertEqual(check_slope(self.example, (3, 1)), 7)


def product(values):
    return reduce(mul, values, 1)


def check_slope(map, slope):
    x, y = 0, 0
    dx, dy = slope
    lines = map.split()
    width = len(lines[0])
    height = len(lines)
    trees = 0
    while y < height:
        trees += lines[y][x] == "#"
        x = (x + dx) % width
        y = (y + dy)
    return trees


def puzzle(map, slopes):
    return product(check_slope(map, slope) for slope in slopes)


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(
            f.read().strip(),
            [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)],
        ))

