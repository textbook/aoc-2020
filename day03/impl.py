#!/usr/bin/env python3
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

    def test_puzzle(self):
        self.assertEqual(puzzle(self.example, (3, 1)), 7)


def puzzle(map, slope):
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


if __name__ == "__main__":
    import sys
    x, y = map(int, sys.argv[1:])
    with open("input.txt") as f:
        print(puzzle(f.read().strip(), (x, y)))

