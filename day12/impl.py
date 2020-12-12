#!/usr/bin/env python3
from os.path import dirname
from textwrap import dedent
import unittest

FORWARD, LEFT, RIGHT, NORTH, EAST, SOUTH, WEST = 'FLRNESW'


def puzzle(instructions):
    latitude, longitude = 0, 0
    waypoint = (1, 10)

    for line in instructions.split("\n"):
        instruction = line[0]
        value = int(line[1:])
        if instruction == FORWARD:
            latitude += waypoint[0] * value
            longitude += waypoint[1] * value
        elif instruction in (NORTH, EAST, SOUTH, WEST):
            waypoint = new_position(waypoint, instruction, value)
        else:
            waypoint = rotate_waypoint(waypoint, instruction, value)

    return abs(latitude) + abs(longitude)


def rotate_waypoint(position, instruction, degrees):
    latitude, longitude = position
    degrees = degrees if instruction == RIGHT else (360 - degrees)
    for _ in range((degrees // 90) % 4):
        latitude, longitude = longitude * -1, latitude
    return latitude, longitude


def new_position(position, direction, value):
    latitude, longitude = position
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
        self.assertEqual(286, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
