#!/usr/bin/env python3
from __future__ import annotations

import re
from operator import add, mul
from os.path import dirname
from typing import Iterator, Union
from unittest import TestCase

OPERATORS = {"+": add, "*": mul}
TOKEN = re.compile(r"[*+]|\d+|[()]")

Expression = list[Union[int, str, "Expression"]]
SimpleExpression = list[Union[int, str]]


def puzzle(expressions: str) -> int:
    return sum(
        evaluate(iter(TOKEN.findall(line)))
        for line in expressions.split("\n")
    )


def evaluate(tokens: Iterator[str]) -> int:
    expression = group(tokens)
    return resolve(expression)


def group(tokens: Iterator[str]) -> Expression:
    expression = []
    for token in tokens:
        if token == ")":
            return expression
        elif token == "(":
            expression.append(group(tokens))
        elif token in ("+", "*"):
            expression.append(token)
        else:
            expression.append(int(token))
    return expression


def resolve(expression: Expression) -> int:
    layer: SimpleExpression = [
        resolve(part) if isinstance(part, list) else part
        for part in expression
    ]
    apply(layer, "+")
    apply(layer, "*")
    return layer[0]


def apply(expression: SimpleExpression, op: str) -> None:
    index = 0
    while index < len(expression):
        part = expression[index]
        if part == op:
            expression[index - 1:index + 2] = [OPERATORS[op](
                expression[index - 1],
                expression[index + 1],
            )]
        else:
            index += 1


class PuzzleTests(TestCase):

    def test_puzzle(self):
        for expression, value in [
            ("1 + 2 * 3 + 4 * 5 + 6", 231),
            ("1 + (2 * 3) + (4 * (5 + 6))", 51),
            ("2 * 3 + (4 * 5)", 46),
            ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
            ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
            ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
        ]:
            with self.subTest(expression=expression):
                self.assertEqual(value, puzzle(expression))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
