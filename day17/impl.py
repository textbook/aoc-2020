#!/usr/bin/env python3
from __future__ import annotations

from itertools import product
from textwrap import dedent
from typing import Generator
from unittest import TestCase

Location = tuple[int, ...]


class State:
    """Represents the current state of the pocket dimension.

    State is stored sparsely, only the coordinate of active cells are
    retained.

    """

    ACTIVE: str = "#"
    DIMENSIONS: int = None
    INACTIVE: str = "."
    NEIGHBOURS: list[Location] = None

    def __init__(self, active_cells: set[Location]):
        self._active_cells = active_cells

    def __str__(self):
        (min_x, max_x), (min_y, max_y), *higher = [
            (
                min(location[dimension] for location in self._active_cells),
                max(location[dimension] for location in self._active_cells),
            )
            for dimension in range(self.DIMENSIONS)
        ]
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
        may_change = self._active_cells.union(
            neighbour
            for active_cell in self._active_cells
            for neighbour in self._neighbours(active_cell)
        )
        return type(self)({
            location
            for location in may_change
            if self._will_be_active(location)
        })

    @property
    def active_cell_count(self) -> int:
        return len(self._active_cells)

    def _will_be_active(self, location: Location) -> bool:
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
    def create(cls, dimensions: int, initial_state: str) -> State:
        """Create instance of State subclass with appropriate dimensions."""
        return type(f"{cls.__name__}{dimensions}d", (cls,), dict(
            DIMENSIONS=dimensions,
            NEIGHBOURS=cls._neighbour_offsets(dimensions),
        ))({
            (x, y, *(0 for _ in range(dimensions - 2)))
            for y, row in enumerate(initial_state.split("\n"))
            for x, value in enumerate(row)
            if value == cls.ACTIVE
        })

    @classmethod
    def _neighbours(cls, location: Location) -> Generator[Location, None, None]:
        for neighbour in cls.NEIGHBOURS:
            yield tuple(n + dn for n, dn in zip(location, neighbour))

    @staticmethod
    def _neighbour_offsets(dimensions: int) -> list[Location]:
        return [
            location
            for location in product((-1, 0, 1), repeat=dimensions)
            if any(value != 0 for value in location)
        ]


def puzzle(initial_state: str, *, cycles: int, dimensions: int) -> int:
    state = State.create(dimensions, initial_state)
    for _ in range(cycles):
        state = state.cycle()
    return state.active_cell_count


class PuzzleTests(TestCase):

    example = dedent("""
        .#.
        ..#
        ###
    """).strip()

    def test_puzzle_4d(self):
        self.assertEqual(848, puzzle(self.example, cycles=6, dimensions=4))

    def test_puzzle_3d(self):
        self.assertEqual(112, puzzle(self.example, cycles=6, dimensions=3))


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
    """).strip(), cycles=6, dimensions=4))
