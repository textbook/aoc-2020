#!/usr/bin/env python3
import re
from operator import add, mul
from os.path import dirname
from typing import Iterator
from unittest import TestCase

OPERATORS = {"+": add, "*": mul}
TOKEN = re.compile(r"[*+]|\d+|[()]")


def puzzle(expressions: str) -> int:
    return sum(
        evaluate(iter(TOKEN.findall(line)))
        for line in expressions.split("\n")
    )


def evaluate(expression: Iterator[str]) -> int:
    total = 0
    for token in expression:
        if token == ")":
            return total
        elif token == "(":
            total = evaluate(expression)
        elif token in ("+", "*"):
            operator = OPERATORS[token]
            next_token = next(expression)
            if next_token == "(":
                total = operator(total, evaluate(expression))
            else:
                total = operator(total, int(next_token))
        else:
            total = int(token)
    return total


class PuzzleTests(TestCase):

    def test_puzzle(self):
        for expression, value in [
            ("1 + 2 * 3 + 4 * 5 + 6", 71),
            ("1 + (2 * 3) + (4 * (5 + 6))", 51),
            ("2 * 3 + (4 * 5)", 26),
            ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
            ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
            ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
        ]:
            with self.subTest(expression=expression):
                self.assertEqual(value, puzzle(expression))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
