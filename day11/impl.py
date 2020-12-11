#!/usr/bin/env python3
from os.path import dirname
from textwrap import dedent
import unittest

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
        self.assertEqual(37, puzzle(self.example))


def new_state(seat, neighbours):
    if seat == EMPTY and all(s != OCCUPIED for s in neighbours):
        return OCCUPIED
    elif seat == OCCUPIED and sum(s == OCCUPIED for s in neighbours) >= 4:
        return EMPTY
    return seat


def get_neighbours(row_index, seat_index, seat_map):
    return [
        seat_map[row_index + row_delta][seat_index + seat_delta]
        for row_delta, seat_delta in [
            (-1, -1), (-1, +0), (-1, +1),
            (+0, -1),           (+0, +1),
            (+1, -1), (+1, +0), (+1, +1),
        ]
        if all((
            row_index + row_delta >= 0,
            row_index + row_delta < len(seat_map),
            seat_index + seat_delta >= 0,
            seat_index + seat_delta < len(seat_map[0]),
        ))
    ]


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
