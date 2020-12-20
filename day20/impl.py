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
        self._flipped: Tile = None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Tile) and self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id_}, {self.borders!r})"

    def flipped(self) -> Tile:
        if self._flipped is None:
            top, right, bottom, left = self.borders
            self._flipped = Tile(
                self.id_,
                (self._flip(bottom), self._flip(left), self._flip(top), self._flip(right))
            )
        return self._flipped

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
    border_map: dict[int, list[Tile]] = defaultdict(list)
    for tile in tiles:
        for border in tile.borders:
            border_map[border].append(tile)
        for border in tile.flipped().borders:
            border_map[border].append(tile)
    connections: dict[Tile, set[Tile]] = defaultdict(set)
    for tile in tiles:
        for border in tile.borders:
            for im in border_map[border]:
                if im != tile:
                    connections[tile].add(im)
        for border in tile.flipped().borders:
            for im in border_map[border]:
                if im != tile:
                    connections[tile].add(im)
    return connections


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
