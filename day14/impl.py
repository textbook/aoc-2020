#!/usr/bin/env python3
import re
from itertools import product
from os.path import dirname
from textwrap import dedent
from unittest import TestCase

UPDATE_BUFFER = re.compile(r"^mem\[(\d+)] = (\d+)")
UPDATE_MASK = re.compile(r"^mask = ([01X]{36})")


class PuzzleTests(TestCase):

    example = dedent("""
        mask = 000000000000000000000000000000X1001X
        mem[42] = 100
        mask = 00000000000000000000000000000000X0XX
        mem[26] = 1
    """).strip()

    def test_puzzle(self):
        self.assertEqual(208, puzzle(self.example))


def apply_mask(value, mask):
    ones_mask = int("".join("1" if value == "1" else "0" for value in mask), 2)
    zeros_mask = int("".join("0" if value == "0" else "1" for value in mask), 2)
    return (value & zeros_mask) | ones_mask


def generate_addresses(initial_address, mask):
    for bits in product(*(
        ("X",) if value == "0" else ("1",) if value == "1" else ("0", "1")
        for value in mask
    )):
        yield apply_mask(initial_address, "".join(bits))


def puzzle(data):
    instructions = data.split("\n")
    buffer = dict()
    for instruction in instructions:
        if update := UPDATE_MASK.match(instruction):
            mask = update.group(1)
        else:
            initial_address, value = map(int, UPDATE_BUFFER.match(instruction).groups())
            for address in generate_addresses(initial_address, mask):
                buffer[address] = value
    return sum(value for value in buffer.values())


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
