#!/usr/bin/env python3
from __future__ import annotations
from textwrap import dedent
from typing import Generator
from unittest import TestCase

Location = tuple[int, int, int]


class State:
    """Represents the current state of the pocket dimension.

    State is stored sparsely, only the coordinate of active cells are
    retained.

    """

    ACTIVE = "#"
    INACTIVE = "."
    NEIGHBOURS = [
        (-1, -1, -1), (+0, -1, -1), (+1, -1, -1),
        (-1, +0, -1), (+0, +0, -1), (+1, +0, -1),
        (-1, +1, -1), (+0, +1, -1), (+1, +1, -1),

        (-1, -1, +0), (+0, -1, +0), (+1, -1, +0),
        (-1, +0, +0), (+1, +0, +0),
        (-1, +1, +0), (+0, +1, +0), (+1, +1, +0),

        (-1, -1, +1), (+0, -1, +1), (+1, -1, +1),
        (-1, +0, +1), (+0, +0, +1), (+1, +0, +1),
        (-1, +1, +1), (+0, +1, +1), (+1, +1, +1),
    ]

    def __init__(self, active_cells: set[Location]):
        self._active_cells = active_cells
        self._bounds = (
            (min(x for x, _, _ in active_cells), max(x for x, _, _ in active_cells)),
            (min(y for _, y, _ in active_cells), max(y for _, y, _ in active_cells)),
            (min(z for _, _, z in active_cells), max(z for _, _, z in active_cells)),
        )

    def __str__(self):
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = self._bounds
        return "\n\n".join(
            "\n".join([f"z={z}"] + [
                "".join(
                    self.ACTIVE
                    if (x, y, z) in self._active_cells
                    else self.INACTIVE
                    for x in range(min_x, max_x + 1)
                )
                for y in range(min_y, max_y + 1)
            ])
            for z in range(min_z, max_z + 1)
        )

    def cycle(self) -> State:
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = self._bounds
        return type(self)({
            (x, y, z)
            for z in range(min_z - 1, max_z + 2)
            for y in range(min_y - 1, max_y + 2)
            for x in range(min_x - 1, max_x + 2)
            if self._is_active((x, y, z))
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
            (x, y, 0)
            for y, row in enumerate(initial_state.split("\n"))
            for x, value in enumerate(row)
            if value == cls.ACTIVE
        })

    @classmethod
    def _neighbours(cls, location: Location) -> Generator[Location, None, None]:
        x, y, z = location
        for dx, dy, dz in cls.NEIGHBOURS:
            yield x + dx, y + dy, z + dz


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
