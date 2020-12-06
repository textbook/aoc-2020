#!/usr/bin/env python3
from os.path import dirname
import unittest


class PuzzleTest(unittest.TestCase):

    example = [
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc",
    ]

    def test_example(self):
        self.assertEqual(puzzle(self.example), 1)
    
    def test_validate(self):
        self.assertTrue(validate("1-3 a: abcde"))
        self.assertFalse(validate("1-3 b: cdefg"))


def validate(line):
    pattern, value = line.split(": ")
    first_second, char = pattern.split(" ")
    first, second = map(int, first_second.split("-"))
    return (value[first - 1] == char) ^ (value[second - 1] == char)


def puzzle(passwords):
    return sum(
        1 if validate(password) else 0
        for password in passwords
    )


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle([
            line.strip()
            for line in f.readlines()
        ]))
