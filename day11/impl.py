#!/usr/bin/env python3
from itertools import count
from os.path import dirname
from textwrap import dedent
import unittest

DIRECTIONS = [
    (-1, -1), (-1, +0), (-1, +1),
    (+0, -1),           (+0, +1),
    (+1, -1), (+1, +0), (+1, +1),
]
EMPTY = "L"
FLOOR = "."
OCCUPIED = "#"


class PuzzleTests(unittest.TestCase):

    example = dedent("""
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL
    """).strip()

    def test_puzzle(self):
        self.assertEqual(26, puzzle(self.example))


def new_state(seat, neighbours):
    if seat == EMPTY and all(s != OCCUPIED for s in neighbours):
        return OCCUPIED
    elif seat == OCCUPIED and sum(s == OCCUPIED for s in neighbours) >= 5:
        return EMPTY
    return seat


def create_seat_getter(row_index, seat_index, seat_map):
    def get_first_seat(direction):
        row_delta, seat_delta = direction
        for factor in count(1):
            neighbour_row = row_index + (row_delta * factor)
            neighbour_seat = seat_index + (seat_delta * factor)
            if (
                neighbour_row < 0
                or neighbour_row >= len(seat_map)
                or neighbour_seat < 0
                or neighbour_seat >= len(seat_map[0])
            ):
                return None
            seat = seat_map[neighbour_row][neighbour_seat]
            if seat == FLOOR:
                continue
            return seat
    return get_first_seat


def get_neighbours(row_index, seat_index, seat_map):
    seat_getter = create_seat_getter(row_index, seat_index, seat_map)
    return [seat for seat in map(seat_getter, DIRECTIONS) if seat is not None]


def iterate(seat_map):
    return [
        [
            new_state(seat, get_neighbours(row_index, seat_index, seat_map))
            for seat_index, seat in enumerate(row)
        ]
        for row_index, row in enumerate(seat_map)
    ]


def puzzle(data):
    seat_map = [list(line) for line in data.split()]
    while (new_seat_map := iterate(seat_map)) != seat_map:
        seat_map = new_seat_map
    return sum(seat == OCCUPIED for row in seat_map for seat in row)


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
