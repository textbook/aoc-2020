#!/usr/bin/env python3
import unittest


class PuzzleTest(unittest.TestCase):

    example = [
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc",
    ]

    def test_example(self):
        self.assertEqual(puzzle(self.example), 2)
    
    def test_validate(self):
        self.assertTrue(validate("1-3 a: abcde"))
        self.assertFalse(validate("1-3 b: cdefg"))


def validate(line):
    pattern, value =line.split(": ")
    min_max, char = pattern.split(" ")
    min_, max_ = min_max.split("-")
    return int(min_) <= value.count(char) <= int(max_)


def puzzle(passwords):
    return sum(
        1 if validate(password) else 0
        for password in passwords
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        print(puzzle([
            line.strip()
            for line in f.readlines()
        ]))
