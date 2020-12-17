#!/usr/bin/env python3
from __future__ import annotations

from itertools import product
from textwrap import dedent
from typing import Generator
from unittest import TestCase

DIMENSIONS = 3
Location = tuple[int, int, int]


class State:
    """Represents the current state of the pocket dimension.

    State is stored sparsely, only the coordinate of active cells are
    retained.

    """

    ACTIVE = "#"
    INACTIVE = "."
    NEIGHBOURS = [
        location
        for location in product((-1, 0, 1), repeat=DIMENSIONS)
        if any(value != 0 for value in location)
    ]

    def __init__(self, active_cells: set[Location]):
        self._active_cells = active_cells
        self._bounds = [
            (
                min(location[dimension] for location in active_cells),
                max(location[dimension] for location in active_cells),
            )
            for dimension in range(DIMENSIONS)
        ]

    def __str__(self):
        (min_x, max_x), (min_y, max_y), *higher = self._bounds
        return "\n\n".join(
            "\n".join([", ".join(f"{label}={value}" for label, value in zip("zw", location))] + [
                "".join(
                    self.ACTIVE
                    if (x, y, *location) in self._active_cells
                    else self.INACTIVE
                    for x in range(min_x, max_x + 1)
                )
                for y in range(min_y, max_y + 1)
            ])
            for location in product(*(range(min_, max_ + 1) for min_, max_ in higher))
        )

    def cycle(self) -> State:
        return type(self)({
            location
            for location in product(*(range(min_ - 1, max_ + 2) for min_, max_ in self._bounds))
            if self._is_active(location)
        })

    @property
    def active_cell_count(self) -> int:
        return len(self._active_cells)

    def _is_active(self, location: Location) -> bool:
        cell = self.ACTIVE if location in self._active_cells else self.INACTIVE
        active_neighbours = sum(
            neighbour in self._active_cells
            for neighbour in self._neighbours(location)
        )
        return (
            (cell == self.INACTIVE and active_neighbours == 3)
            or (cell == self.ACTIVE and active_neighbours in (2, 3))
        )

    @classmethod
    def from_string(cls, initial_state: str) -> State:
        return cls({
            (x, y, *(0 for _ in range(DIMENSIONS - 2)))
            for y, row in enumerate(initial_state.split("\n"))
            for x, value in enumerate(row)
            if value == cls.ACTIVE
        })

    @classmethod
    def _neighbours(cls, location: Location) -> Generator[Location, None, None]:
        for neighbour in cls.NEIGHBOURS:
            yield tuple(n + dn for n, dn in zip(location, neighbour))


def puzzle(initial_state: str, rounds: int) -> int:
    state = State.from_string(initial_state)
    for _ in range(rounds):
        state = state.cycle()
    return state.active_cell_count


class PuzzleTests(TestCase):

    example = dedent("""
        .#.
        ..#
        ###
    """).strip()

    def test_puzzle(self):
        self.assertEqual(112, puzzle(self.example, 6))


if __name__ == "__main__":
    print(puzzle(dedent("""
        ##...#.#
        #..##..#
        ..#.####
        .#..#...
        ########
        ######.#
        .####..#
        .###.#..
    """).strip(), 6))
