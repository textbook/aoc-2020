#!/usr/bin/env python
from os.path import dirname
from textwrap import dedent
import unittest


class PuzzleTest(unittest.TestCase):

    def test_examples(self):
        for in_, out in [
            ("FBFBBFFRLR", 357),
            ("FBFBBFFRRL", 358),
            ("FBFBBFFRRR", 359),
            ("FBFBBFBLLL", 360),
            ("FBFBBFBLLR", 361),
            ("FBFBBFBLRL", 362),
            ("BFFFBBFRRR", 567),
            ("FFFBBBFRRR", 119),
            ("BBFFBBFRLL", 820),
        ]:
            with self.subTest(in_=in_, out=out):
                self.assertEqual(seat_id(in_), out)

    def test_puzzle(self):
        self.assertEqual(puzzle(dedent("""
            FBFBBFFRLR
            FBFBBFFRRL
            FBFBBFBLLL
            FBFBBFBLLR
            FBFBBFBLRL
        """.strip())), 359)


def bisect(code, front):
    options = list(range(2 ** len(code)))
    for char in code:
        if char == front:
            options = options[:len(options)//2]
        else:
            options = options[len(options)//2:]
    return options[0]


def seat_id(seat):
    return (bisect(seat[:7], "F") * 8) + bisect(seat[7:], "L")


def puzzle(data):
    present = sorted(seat_id(seat) for seat in data.split())
    for index in range(1, len(present)):
        if present[index - 1] != present[index] - 1:
            return present[index] - 1


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
