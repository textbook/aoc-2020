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
        self.assertEqual(8, puzzle(self.example))


def execute(program):
    """Return the value of the accumulator when the program ends.

    Return None if the program loops.

    """
    accumulator = 0
    pointer = 0
    visited = set()

    while True:
        if pointer in visited:
            return None
        if pointer >= len(program):
            return accumulator
        op = program[pointer]
        visited.add(pointer)
        if op.startswith("nop"):
            pointer += 1
        elif op.startswith("jmp"):
            pointer += int(op.split()[1])
        elif op.startswith("acc"):
            accumulator += int(op.split()[1])
            pointer += 1


def puzzle(program):
    for index, line in enumerate(program):
        if line.startswith(("nop", "jmp")):
            new_program = program[:]
            op, acc = line.split()
            new_program[index] = f"{'nop' if op == 'jmp' else 'jmp'} {acc}"
            if (result := execute(new_program)) is not None:
                return result


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip().split("\n")))
