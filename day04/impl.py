#!/usr/bin/env python3
import re
from textwrap import dedent
import unittest

VALID_EYE_COLOURS = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def valid_year(min_, max_):
    def valid(s):
        return re.match(r"^\d{4}$", s) is not None and min_ <= int(s) <= max_
    return valid


def valid_height(s):
    if re.match(r"^\d{3}cm$", s):
        return 150 <= int(s[:-2]) <= 193
    elif re.match(r"^\d{2}in$", s):
        return 59 <= int(s[:-2]) <= 76
    return False


RULES = dict(
    byr=valid_year(1920, 2002),
    ecl=lambda s: s in VALID_EYE_COLOURS,
    eyr=valid_year(2020, 2030),
    hcl=re.compile(r"^#[0-9a-f]{6}$").match,
    hgt=valid_height,
    iyr=valid_year(2010, 2020),
    pid=re.compile(r"^\d{9}$").match,
)


class PuzzleTest(unittest.TestCase):

    example = dedent("""
        eyr:1972 cid:100
        hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
        
        iyr:2019
        hcl:#602927 eyr:1967 hgt:170cm
        ecl:grn pid:012533040 byr:1946
        
        hcl:dab227 iyr:2012
        ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
        
        hgt:59cm ecl:zzz
        eyr:2038 hcl:74454a iyr:2023
        pid:3556412378 byr:2007
        
        pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
        hcl:#623a2f
        
        eyr:2029 ecl:blu cid:129 byr:1989
        iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
        
        hcl:#888785
        hgt:164cm byr:2001 iyr:2015 cid:88
        pid:545766238 ecl:hzl
        eyr:2022
        
        iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """.strip())

    def test_example(self):
        self.assertEqual(puzzle(self.example, RULES), 4)

    def test_byr_valid(self):
        for byr in range(1920, 2003):
            with self.subTest(byr=byr):
                self.assertTrue(RULES["byr"](str(byr)))

    def test_byr_invalid(self):
        for byr in (1918, 1919, 2003, 2004, "foo"):
            with self.subTest(byr=byr):
                self.assertFalse(RULES["byr"](str(byr)))

    def test_ecl_valid(self):
        for ecl in VALID_EYE_COLOURS:
            with self.subTest(ecl=ecl):
                self.assertTrue(RULES["ecl"](ecl))

    def test_ecl_invalid(self):
        self.assertFalse(RULES["ecl"]("foo"))

    def test_eyr_valid(self):
        for eyr in range(2020, 2031):
            with self.subTest(eyr=eyr):
                self.assertTrue(RULES["eyr"](str(eyr)))

    def test_eyr_invalid(self):
        for eyr in (2018, 2019, 2031, 2032, "foo"):
            with self.subTest(eyr=eyr):
                self.assertFalse(RULES["eyr"](str(eyr)))

    def test_hcl_valid(self):
        for hcl in ("#abc123", "#000000"):
            with self.subTest(hcl=hcl):
                self.assertTrue(RULES["hcl"](hcl))

    def test_hcl_invalid(self):
        for hcl in ("#abg123", "foo"):
            with self.subTest(hcl=hcl):
                self.assertFalse(RULES["hcl"](hcl))

    def test_hgt_valid(self):
        for hgt in range(150, 194):
            with self.subTest(hgt=f"{hgt}cm"):
                self.assertTrue(RULES["hgt"](f"{hgt}cm"))
        for hgt in range(59, 77):
            with self.subTest(hgt=f"{hgt}in"):
                self.assertTrue(RULES["hgt"](f"{hgt}in"))

    def test_hgt_invalid(self):
        for hgt in (148, 149, 194, 195):
            with self.subTest(hgt=f"{hgt}cm"):
                self.assertFalse(RULES["hgt"](f"{hgt}cm"))
        for hgt in (57, 58, 77, 78):
            with self.subTest(hgt=f"{hgt}in"):
                self.assertFalse(RULES["hgt"](f"{hgt}in"))
        self.assertFalse(RULES["hgt"]("foo"))

    def test_iyr_valid(self):
        for iyr in range(2010, 2021):
            with self.subTest(iyr=iyr):
                self.assertTrue(RULES["iyr"](str(iyr)))

    def test_iyr_invalid(self):
        for iyr in (2008, 2009, 2021, 2022, "foo"):
            with self.subTest(iyr=iyr):
                self.assertFalse(RULES["iyr"](str(iyr)))

    def test_pid_valid(self):
        for pid in ("896056539", "000000001"):
            with self.subTest(pid=pid):
                self.assertTrue(RULES["pid"](pid))

    def test_pid_invalid(self):
        for pid in ("8960565390", "foo"):
            with self.subTest(pid=pid):
                self.assertFalse(RULES["pid"](pid))


def parse(data):
    return dict(s.split(":") for s in data.split())


def is_valid(passport, rules):
    return all(
        field in passport and valid(passport[field])
        for field, valid in rules.items()
    )


def puzzle(data, rules):
    return sum(
        is_valid(parse(passport), rules)
        for passport in data.split("\n\n")
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        print(puzzle(f.read().strip(), RULES))
