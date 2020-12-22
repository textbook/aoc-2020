#!/usr/bin/env python3
from collections import deque
from os.path import dirname
from textwrap import dedent
from unittest import TestCase


def puzzle(data):
    p1, p2 = data.split("\n\n")
    p1_cards = deque(int(card) for card in p1.split("\n")[1:])
    p2_cards = deque(int(card) for card in p2.split("\n")[1:])
    while p1_cards and p2_cards:
        p1_card = p1_cards.popleft()
        p2_card = p2_cards.popleft()
        if p1_card > p2_card:
            p1_cards.extend([p1_card, p2_card])
        else:
            p2_cards.extend([p2_card, p1_card])
    winner_cards = list(p1_cards or p2_cards)
    return sum(index * card for index, card in enumerate(winner_cards[::-1], 1))


class PuzzleTests(TestCase):

    example = dedent("""
        Player 1:
        9
        2
        6
        3
        1
        
        Player 2:
        5
        8
        4
        7
        10
    """).strip()

    def test_puzzle(self):
        self.assertEqual(306, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
