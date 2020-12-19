#!/usr/bin/env python3
import re
from ast import literal_eval
from os.path import dirname
from textwrap import dedent
from typing import Union
from unittest import TestCase

RuleMap = dict[int, Union[list[list[int]], str]]


def puzzle(data: str) -> int:
    rules, messages = data.split("\n\n")
    rule_zero = resolve(rules.split("\n"))
    return sum(
        rule_zero.match(message) is not None
        for message in messages.split("\n")
    )


def resolve(rules: list[str]) -> re.Pattern:
    rule_map = build_map(rules)

    @memoize
    def find_rule(index: int) -> str:
        rule = rule_map[index]
        if isinstance(rule, str):
            return rule
        if len(rule) == 1:
            return "".join(find_rule(i) for i in rule[0])
        return f"(?:{'|'.join(''.join(find_rule(i) for i in part) for part in rule)})"

    return re.compile(f"^{find_rule(0)}$")


def build_map(rules: list[str]) -> RuleMap:
    rule_map: RuleMap = dict()
    for line in rules:
        index, rule = line.split(":")
        if '"' in rule:
            rule_map[int(index)] = literal_eval(rule.strip())
        else:
            rule_map[int(index)] = [
                [int(x) for x in part.split()]
                for part in rule.split("|")
            ]
    return rule_map


def memoize(func):
    def wrapper(*args):
        if args not in wrapper._cache:
            wrapper._cache[args] = func(*args)
        return wrapper._cache[args]
    wrapper._cache = dict()
    return wrapper


class PuzzleTests(TestCase):

    example = dedent("""
        0: 4 1 5
        1: 2 3 | 3 2
        2: 4 4 | 5 5
        3: 4 5 | 5 4
        4: "a"
        5: "b"
        
        ababbb
        bababa
        abbbab
        aaabbb
        aaaabbb
    """).strip()

    def test_puzzle(self):
        self.assertEqual(2, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
