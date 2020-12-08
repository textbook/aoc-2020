#!/usr/bin/env python3
from os.path import dirname
import unittest


class PuzzleTest(unittest.TestCase):

    example = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ]

    def test_puzzle(self):
        self.assertEqual(5, puzzle(self.example))


def puzzle(program):
    accumulator = 0
    pointer = 0
    visited = set()

    while True:
        if pointer in visited:
            break
        op = program[pointer]
        visited.add(pointer)
        if op.startswith("nop"):
            pointer += 1
        elif op.startswith("jmp"):
            pointer += int(op.split()[1])
        elif op.startswith("acc"):
            accumulator += int(op.split()[1])
            pointer += 1

    return accumulator


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip().split("\n")))
