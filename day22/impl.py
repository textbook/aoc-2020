#!/usr/bin/env python3
from collections import deque
from os.path import dirname
from textwrap import dedent
from unittest import TestCase

State = tuple[tuple[int, ...], tuple[int, ...]]


class RecursiveGameError(Exception):
    pass


def puzzle(data):
    p1_cards, p2_cards = map(_create_deck, data.split("\n\n"))
    winner_cards = p1_cards if _recursive_combat(p1_cards, p2_cards) else p2_cards
    return sum(index * card for index, card in enumerate(list(winner_cards)[::-1], 1))


def _recursive_combat(p1_cards: deque[int], p2_cards: deque[int]) -> bool:
    """Returns whether p1 wins."""
    seen = set()
    while p1_cards and p2_cards:
        state = tuple(p1_cards), tuple(p2_cards)
        if state in seen:
            return True
        seen.add(state)
        p1_card = p1_cards.popleft()
        p2_card = p2_cards.popleft()
        p1_wins = (
            p1_card > p2_card
            if len(p1_cards) < p1_card or len(p2_cards) < p2_card
            else _recursive_combat(_slice_deck(p1_cards, p1_card), _slice_deck(p2_cards, p2_card))
        )
        if p1_wins:
            p1_cards.extend([p1_card, p2_card])
        else:
            p2_cards.extend([p2_card, p1_card])
    return bool(p1_cards)


def _slice_deck(deck: deque[int], end: int) -> deque[int]:
    return deque(list(deck)[:end])


def _create_deck(cards: str) -> deque[int]:
    return deque(int(card) for card in cards.split("\n")[1:])


class PuzzleTests(TestCase):

    def test_puzzle(self):
        self.assertEqual(291, puzzle(dedent("""
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
        """).strip()))

    def test_handles_recursion(self):
        self.assertIsInstance(puzzle(dedent("""
            Player 1:
            43
            19
            
            Player 2:
            2
            29
            14
        """).strip()), int)


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
