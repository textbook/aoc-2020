#!/usr/bin/env python3
from os.path import dirname
from re import findall
from textwrap import dedent
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


def puzzle(data):
    black_tiles: set[Coordinates] = set()
    for coordinates in map(_determine_coordinates, data.split("\n")):
        if coordinates in black_tiles:
            black_tiles.remove(coordinates)
        else:
            black_tiles.add(coordinates)
    return len(black_tiles)


def _determine_coordinates(line: str) -> Coordinates:
    u, v, w = 0, 0, 0
    for direction in findall(r"ne|nw|se|sw|e|w", line):
        du, dv, dw = MOVES[direction]
        u, v, w = (u + du, v + dv, w + dw)
    return u, v, w


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
        self.assertEqual(10, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
