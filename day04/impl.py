#!/usr/bin/env python3
from textwrap import dedent
import unittest

REQUIRED = ("ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt")


class PuzzleTest(unittest.TestCase):

    example = dedent("""
        ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm
        
        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929
        
        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm
        
        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in
    """.strip())

    def test_example(self):
        self.assertEqual(puzzle(self.example, REQUIRED), 2)


def parse(data):
    return dict(s.split(":") for s in data.split())


def is_valid(passport, required):
    return all(field in passport for field in required)


def puzzle(data, required):
    return sum(
        is_valid(parse(passport), required)
        for passport in data.split("\n\n")
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        print(puzzle(f.read().strip(), REQUIRED))
