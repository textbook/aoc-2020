#!/usr/bin/env python
from unittest import TestCase


def puzzle(data: str, moves: int = 100) -> str:
    cups: list[int] = [int(char) for char in data]
    current_index = 0
    for _ in range(moves):
        current_cup = cups[current_index]
        to_move = _cups_to_move(cups, current_index)
        insert_after = _get_insert_after(cups, current_cup, to_move)
        cups = _move_to(cups, to_move, insert_after)
        current_index = (cups.index(current_cup) + 1) % len(cups)
    return "".join(str(cup) for cup in cups[cups.index(1) + 1:] + cups[:cups.index(1)])


def _cups_to_move(cups: list[int], current_index: int, number: int = 3) -> list[int]:
    to_move = cups[current_index + 1:current_index + number + 1]
    if len(to_move) < number:
        to_move = to_move + cups[:number - len(to_move)]
    return to_move


def _get_insert_after(cups: list[int], current_cup: int, to_move: list[int]) -> int:
    insert_after = (current_cup - 1) % (len(cups) + 1)
    while insert_after in to_move or insert_after not in cups:
        insert_after = (insert_after - 1) % (len(cups) + 1)
    return insert_after


def _move_to(cups: list[int], to_move: list[int], insert_after: int) -> list[int]:
    cups = [cup for cup in cups if cup not in to_move]
    insert_at = cups.index(insert_after) + 1
    cups[insert_at:insert_at] = to_move
    return cups


class PuzzleTests(TestCase):

    def test_puzzle_10_moves(self):
        self.assertEqual("92658374", puzzle("389125467", 10))

    def test_puzzle_100_moves(self):
        self.assertEqual("67384529", puzzle("389125467"))


if __name__ == "__main__":
    print(puzzle("784235916"))
