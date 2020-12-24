#!/usr/bin/env python3
from os.path import dirname
from re import findall
from textwrap import dedent
from typing import Generator
from unittest import TestCase

Coordinates = tuple[int, int, int]

MOVES: dict[str, Coordinates] = dict(
    e=(1, -1, 0),
    se=(1, 0, -1),
    sw=(0, 1, -1),
    w=(-1, 1, 0),
    nw=(-1, 0, 1),
    ne=(0, -1, 1),
)


def puzzle(initial_state: str, days: int) -> int:
    black_tiles = _get_initial_state(initial_state)
    for _ in range(days):
        black_tiles = _iterate(black_tiles)
    return len(black_tiles)


def _get_initial_state(initial_state: str) -> set[Coordinates]:
    black_tiles: set[Coordinates] = set()
    for coordinates in map(_determine_coordinates, initial_state.split("\n")):
        if coordinates in black_tiles:
            black_tiles.remove(coordinates)
        else:
            black_tiles.add(coordinates)
    return black_tiles


def _determine_coordinates(line: str) -> Coordinates:
    u, v, w = 0, 0, 0
    for direction in findall("|".join(MOVES.keys()), line):
        du, dv, dw = MOVES[direction]
        u, v, w = (u + du, v + dv, w + dw)
    return u, v, w


def _iterate(black_tiles: set[Coordinates]) -> set[Coordinates]:
    might_change = black_tiles.union(
        neighbour
        for tile in black_tiles
        for neighbour in _neighbours(tile)
    )
    return set(tile for tile in might_change if _will_be_black(tile, black_tiles))


def _neighbours(tile: Coordinates) -> Generator[Coordinates, None, None]:
    u, v, w = tile
    for du, dv, dw in MOVES.values():
        yield u + du, v + dv, w + dw


def _will_be_black(tile: Coordinates, black_tiles: set[Coordinates]) -> bool:
    black_neighbours = sum(neighbour in black_tiles for neighbour in _neighbours(tile))
    if tile in black_tiles:
        return 0 < black_neighbours <= 2
    else:
        return black_neighbours == 2


class PuzzleTests(TestCase):

    example = dedent("""
        sesenwnenenewseeswwswswwnenewsewsw
        neeenesenwnwwswnenewnwwsewnenwseswesw
        seswneswswsenwwnwse
        nwnwneseeswswnenewneswwnewseswneseene
        swweswneswnenwsewnwneneseenw
        eesenwseswswnenwswnwnwsewwnwsene
        sewnenenenesenwsewnenwwwse
        wenwwweseeeweswwwnwwe
        wsweesenenewnwwnwsenewsenwwsesesenwne
        neeswseenwwswnwswswnw
        nenwswwsewswnenenewsenwsenwnesesenew
        enewnwewneswsewnwswenweswnenwsenwsw
        sweneswneswneneenwnewenewwneswswnese
        swwesenesewenwneswnwwneseswwne
        enesenwswwswneneswsenwnewswseenwsese
        wnwnesenesenenwwnenwsewesewsesesew
        nenewswnwewswnenesenwnesewesw
        eneswnwswnwsenenwnwnwwseeswneewsenese
        neswnwewnwnwseenwseesewsenwsweewe
        wseweeenwnesenwwwswnew
    """).strip()

    def test_puzzle(self):
        for days, black_tiles in [
            (0, 10),
            (1, 15),
            (2, 12),
            (3, 25),
            (4, 14),
            (5, 23),
            (6, 28),
            (7, 41),
            (8, 37),
            (9, 49),
            (10, 37),
            (20, 132),
            (30, 259),
            (40, 406),
            (50, 566),
            (60, 788),
            (70, 1106),
            (80, 1373),
            (90, 1844),
            (100, 2208),
        ]:
            with self.subTest(days=days):
                self.assertEqual(black_tiles, puzzle(self.example, days))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip(), 100))
