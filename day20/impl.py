#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from functools import reduce
from operator import mul
from os.path import dirname
from textwrap import dedent
from typing import Iterable, Any
from unittest import TestCase


class Tile:
    EDGE_LENGTH = 10
    ONE = "#"
    ZERO = "."

    def __init__(self, id_: int, borders: tuple[int, int, int, int]):
        self.id_ = id_
        self.borders = borders
        self._flips: dict[tuple[bool, bool], Tile] = dict()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Tile) and self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id_}, {self.borders!r})"

    def flip(self, *, vertically: bool, horizontally: bool) -> Tile:
        if not vertically and not horizontally:
            return self
        if (vertically, horizontally) not in self._flips:
            top, right, bottom, left = self.borders
            if vertically:
                top, right, bottom, left = bottom, self._flip(right), top, self._flip(left)
            if horizontally:
                top, right, bottom, left = self._flip(top), left, self._flip(bottom), right
            self._flips[vertically, horizontally] = Tile(self.id_, (top, right, bottom, left))
        return self._flips[vertically, horizontally]

    @classmethod
    def from_string(cls, data: str):
        identity, *content = data.split("\n")
        borders = (
            cls._calculate_border(content[0]),
            cls._calculate_border(row[-1] for row in content),
            cls._calculate_border(content[-1]),
            cls._calculate_border(row[0] for row in content),
        )
        return cls(int(identity.split()[1][:-1]), borders)

    @classmethod
    def _calculate_border(cls, chars: Iterable[str]):
        return int("".join("1" if char == cls.ONE else "0" for char in chars), 2)

    @classmethod
    def _flip(cls, border: int) -> int:
        """https://stackoverflow.com/a/5333563/3001761"""
        return sum(
            1 << (cls.EDGE_LENGTH - 1 - i)
            for i in range(cls.EDGE_LENGTH)
            if border >> i & 1
        )


def puzzle(data: str) -> int:
    tiles = [Tile.from_string(tile) for tile in data.split("\n\n")]
    connections = _get_connections(tiles)
    corners = [tile for tile in connections if len(connections[tile]) == 2]
    return reduce(mul, (tile.id_ for tile in corners), 1)


def _get_connections(tiles: list[Tile]) -> dict[Tile, set[Tile]]:
    border_map = _create_border_map(tiles)
    return _create_connection_map(tiles, border_map)


def _create_connection_map(
    tiles: list[Tile],
    border_map: dict[int, list[Tile]],
) -> dict[Tile, set[Tile]]:
    connections: dict[Tile, set[Tile]] = defaultdict(set)
    for tile in tiles:
        for border in tile.borders:
            for t in border_map[border]:
                if t != tile:
                    connections[tile].add(t)
        for border in tile.flip(vertically=True, horizontally=True).borders:
            for t in border_map[border]:
                if t != tile:
                    connections[tile].add(t)
    return connections


def _create_border_map(tiles: list[Tile]) -> dict[int, list[Tile]]:
    border_map: dict[int, list[Tile]] = defaultdict(list)
    for tile in tiles:
        for border in tile.borders:
            border_map[border].append(tile)
        for border in tile.flip(vertically=True, horizontally=True).borders:
            border_map[border].append(tile)
    return border_map


class PuzzleTests(TestCase):
    example = dedent("""
        Tile 2311:
        ..##.#..#.
        ##..#.....
        #...##..#.
        ####.#...#
        ##.##.###.
        ##...#.###
        .#.#.#..##
        ..#....#..
        ###...#.#.
        ..###..###
        
        Tile 1951:
        #.##...##.
        #.####...#
        .....#..##
        #...######
        .##.#....#
        .###.#####
        ###.##.##.
        .###....#.
        ..#.#..#.#
        #...##.#..
        
        Tile 1171:
        ####...##.
        #..##.#..#
        ##.#..#.#.
        .###.####.
        ..###.####
        .##....##.
        .#...####.
        #.##.####.
        ####..#...
        .....##...
        
        Tile 1427:
        ###.##.#..
        .#..#.##..
        .#.##.#..#
        #.#.#.##.#
        ....#...##
        ...##..##.
        ...#.#####
        .#.####.#.
        ..#..###.#
        ..##.#..#.
        
        Tile 1489:
        ##.#.#....
        ..##...#..
        .##..##...
        ..#...#...
        #####...#.
        #..#.#.#.#
        ...#.#.#..
        ##.#...##.
        ..##.##.##
        ###.##.#..
        
        Tile 2473:
        #....####.
        #..#.##...
        #.##..#...
        ######.#.#
        .#...#.#.#
        .#########
        .###.#..#.
        ########.#
        ##...##.#.
        ..###.#.#.
        
        Tile 2971:
        ..#.#....#
        #...###...
        #.#.###...
        ##.##..#..
        .#####..##
        .#..####.#
        #..#.#..#.
        ..####.###
        ..#.#.###.
        ...#.#.#.#
        
        Tile 2729:
        ...#.#.#.#
        ####.#....
        ..#.#.....
        ....#..#.#
        .##..##.#.
        .#.####...
        ####.#.#..
        ##.####...
        ##..#.##..
        #.##...##.
        
        Tile 3079:
        #.#.#####.
        .#..######
        ..#.......
        ######....
        ####.#..#.
        .#...#.##.
        #.#####.##
        ..#.###...
        ..#.......
        ..#.###...
    """).strip()

    def test_puzzle(self):
        self.assertEqual(20_899_048_083_289, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
