#!/usr/bin/env python3
import unittest
from os.path import dirname


class PuzzleTests(unittest.TestCase):

    def test_puzzle(self):
        self.assertEqual(295, puzzle(939, [7, 13, 59, 31, 19]))


def puzzle(arrival, schedule):
    next_bus, shortest_wait = None, None
    for bus in schedule:
        wait = (bus * ((arrival // bus) + 1)) - arrival
        if shortest_wait is None or wait < shortest_wait:
            next_bus = bus
            shortest_wait = wait
    return next_bus * shortest_wait


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        arrival = int(next(f))
        buses = next(f)
    schedule = [int(bus) for bus in buses.split(",") if bus != "x"]
    print(puzzle(arrival, schedule))
