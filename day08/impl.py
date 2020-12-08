#!/usr/bin/env python3
from collections import namedtuple
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


class InfiniteLoop(Exception):

    def __init__(self, visited):
        super().__init__("infinite loop detected")
        self.visited = visited


Operation = namedtuple("Operation", ("accumulate", "jump"))


def create_operation(op, val):
    if op == "acc":
        return Operation(accumulate=val, jump=1)
    elif op == "jmp":
        return Operation(accumulate=0, jump=val)
    return Operation(accumulate=0, jump=1)


CHANGES = dict(jmp="nop", nop="jmp")


def execute(program):
    """Return the value of the accumulator when the program ends."""
    accumulator = 0
    pointer = 0
    visited = set()

    while True:
        if pointer in visited:
            raise InfiniteLoop(visited)
        if pointer >= len(program):
            return accumulator
        visited.add(pointer)
        op = create_operation(*program[pointer])
        accumulator += op.accumulate
        pointer += op.jump


def get_visited(lines):
    """Get the set of indices visited before the loop."""
    try:
        execute(lines)
    except InfiniteLoop as loop:
        return loop.visited
    raise ValueError("no loop found")


def puzzle(program):
    lines = [(op, int(val)) for op, val in map(str.split, program)]
    visited = get_visited(lines)
    for index, (op, val) in enumerate(lines):
        if index in visited and op in CHANGES:
            new_program = lines[:]
            new_program[index] = CHANGES[op], val
            try:
                return execute(new_program)
            except InfiniteLoop:
                continue


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip().split("\n")))
