#!/usr/bin/env python3
from collections import defaultdict
from os.path import dirname
from textwrap import dedent
from unittest import TestCase


def puzzle(data: str) -> int:
    all_allergens: dict[str, list[list[str]]] = defaultdict(list)
    all_ingredients: list[str] = list()
    for row in data.split("\n"):
        ingredients, allergens = row.strip().split("(contains ")
        new_ingredients = ingredients.strip().split()
        all_ingredients.extend(new_ingredients)
        for allergen in allergens[:-1].split(", "):
            all_allergens[allergen].append(new_ingredients)
    allergen_map: dict[str, set[str]] = {
        allergen: set(ingredients[0]).intersection(*ingredients[1:])
        for allergen, ingredients in all_allergens.items()
    }
    allergenic_ingredients = set(
        ingredient
        for ingredients in allergen_map.values()
        for ingredient in ingredients
    )
    return sum(ingredient not in allergenic_ingredients for ingredient in all_ingredients)


class PuzzleTests(TestCase):

    example = dedent("""
        mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
        trh fvjkl sbzzf mxmxvkd (contains dairy)
        sqjhc fvjkl (contains soy)
        sqjhc mxmxvkd sbzzf (contains fish)
    """).strip()

    def test_puzzle(self):
        self.assertEqual(5, puzzle(self.example))


if __name__ == "__main__":
    with open(f"{dirname(__file__)}/input.txt") as f:
        print(puzzle(f.read().strip()))
