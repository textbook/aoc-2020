#!/usr/bin/env python3
import re
from os.path import dirname
from textwrap import dedent
from unittest import TestCase

UPDATE_BUFFER = re.compile(r"^mem\[(\d+)] = (\d+)")
UPDATE_MASK = re.compile(r"^mask = ([01X]{36})")


class PuzzleTests(TestCase):

    example = dedent("""
        mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
        mem[8] = 11
        mem[7] = 101
        mem[8] = 0
    """).strip()

    def test_puzzle(self):
        self.assertEqual(165, puzzle(self.example))


def puzzle(data):
    instructions = data.split("\n")
    buffer = dict()
    for instruction in instructions:
        if update := UPDATE_MASK.match(instruction):
            ones_mask = int("".join(
                "1" if value == "1" else "0"
                for value in update.group(1)
            ), 2)
            zeros_mask = int("".join(
                "0" if value == "0" else "1"
                for value in update.group(1)
            ), 2)
        else:
            address, value = map(int, UPDATE_BUFFER.match(instruction).groups())
            buffer[address] = (value & zeros_mask) | ones_mask
    return sum(value for value in buffer.values())


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
