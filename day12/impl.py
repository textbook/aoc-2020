#!/usr/bin/env python3
from os.path import dirname
from textwrap import dedent
import unittest

FORWARD, LEFT, RIGHT, NORTH, EAST, SOUTH, WEST = 'FLRNESW'


def puzzle(instructions):
    latitude, longitude = 0, 0
    direction = EAST

    for line in instructions.split("\n"):
        instruction = line[0]
        value = int(line[1:])
        if instruction in (LEFT, RIGHT):
            direction = new_direction(direction, instruction, value)
            continue
        if instruction == FORWARD:
            instruction = direction
        latitude, longitude = new_position(latitude, longitude, instruction, value)

    return abs(latitude) + abs(longitude)


def new_direction(direction, instruction, value):
    ordered = [NORTH, EAST, SOUTH, WEST]
    index = ordered.index(direction)
    shift = (value // 90) * (1 if instruction == RIGHT else -1)
    return ordered[(index + shift) % 4]


def new_position(latitude, longitude, direction, value):
    if direction == NORTH:
        return latitude + value, longitude
    elif direction == SOUTH:
        return latitude - value, longitude
    elif direction == EAST:
        return latitude, longitude + value
    elif direction == WEST:
        return latitude, longitude - value


class PuzzleTests(unittest.TestCase):

    example = dedent("""
        F10
        N3
        F7
        R90
        F11
    """).strip()

    def test_puzzle(self):
        self.assertEqual(25, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
