#!/usr/bin/env python3
from unittest import TestCase


def puzzle(start, target):
    *series, next_spoken = start
    seen = {value: index for index, value in enumerate(series)}
    for turn in range(len(series), target - 1):
        last_index = seen.get(next_spoken)
        seen[next_spoken] = turn
        next_spoken = turn - last_index if last_index is not None else 0
    return next_spoken


class PuzzleTests(TestCase):

    def test_puzzle_short(self):
        for start, expected in [
            ([0, 3, 6], 436),
            ([1, 3, 2], 1),
            ([2, 1, 3], 10),
            ([1, 2, 3], 27),
            ([2, 3, 1], 78),
            ([3, 2, 1], 438),
            ([3, 1, 2], 1836),
        ]:
            with self.subTest(start=start):
                self.assertEqual(expected, puzzle(start, 2020))

    def test_puzzle_long(self):
        for start, expected in [
            ([0, 3, 6], 175594),
            ([1, 3, 2], 2578),
            ([2, 1, 3], 3544142),
            ([1, 2, 3], 261214),
            ([2, 3, 1], 6895259),
            ([3, 2, 1], 18),
            ([3, 1, 2], 362),
        ]:
            with self.subTest(start=start):
                self.assertEqual(expected, puzzle(start, 30_000_000))


if __name__ == "__main__":
    print(puzzle([1, 0, 18, 10, 19, 6], 30_000_000))
