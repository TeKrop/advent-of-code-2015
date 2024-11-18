import re
from functools import cached_property
from typing import Iterable

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 15 - Common code
    ###########################
    def solve(self) -> tuple[int, int]:
        self.ingredients = list(self.__compute_ingredients())
        self.possible_cookies = list(self.__get_possible_cookies(self.ingredients))
        return super().solve()

    def __compute_ingredients(self) -> Iterable["Ingredient"]:
        yield from (Ingredient(line) for line in self.lines)

    def __get_possible_cookies(
        self, ingredients: list["Ingredient"]
    ) -> Iterable["Cookie"]:
        combinations = self.__get_combinations(
            nb_ingredients=len(ingredients), total=self.teaspoons_of_ingredients
        )
        for combination in combinations:
            yield Cookie(
                ingredients={
                    ingredient: combination[idx]
                    for idx, ingredient in enumerate(ingredients)
                }
            )

    def __get_combinations(
        self, nb_ingredients: int, total: int
    ) -> Iterable[list[int]]:
        if nb_ingredients == 1:
            yield [total]
            return

        for i in range(total):
            for combination in self.__get_combinations(nb_ingredients - 1, total - i):
                yield [i] + combination

    ###########################
    # DAY 15 - First Part
    ###########################
    teaspoons_of_ingredients: int = 100

    def _solve_first_part(self) -> int:
        return max(cookie.score for cookie in self.possible_cookies)

    ###########################
    # DAY 15 - Second Part
    ###########################
    calories_target: int = 500

    def _solve_second_part(self) -> int:
        return max(
            cookie.score
            for cookie in self.possible_cookies
            if cookie.calories == self.calories_target
        )


class Ingredient:
    def __init__(self, line: str):
        name, capacity, durability, flavor, texture, calories = self.line_pattern.match(
            line
        ).groups()

        self.name: str = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)

    @cached_property
    def line_pattern(self) -> re.Pattern:
        return re.compile(
            r"^([A-z]+): capacity (-?[0-9]+), durability (-?[0-9]+), flavor (-?[0-9]+), texture (-?[0-9]+), calories (-?[0-9]+)$"
        )

    def __repr__(self) -> str:
        return (
            f"<Ingredient name={self.name} capacity={self.capacity} "
            f"durability={self.durability} flavor={self.flavor} "
            f"texture={self.texture} calories={self.calories}>"
        )


class Cookie:
    def __init__(self, ingredients: dict[Ingredient, int]):
        self.ingredients = ingredients

    @property
    def calories(self) -> int:
        return sum(
            quantity * ingredient.calories
            for ingredient, quantity in self.ingredients.items()
        )

    @property
    def score(self) -> int:
        # Initialize totals
        total_capacity = total_durability = total_flavor = total_texture = 0

        # Make the additions
        for ingredient, quantity in self.ingredients.items():
            total_capacity += quantity * ingredient.capacity
            total_durability += quantity * ingredient.durability
            total_flavor += quantity * ingredient.flavor
            total_texture += quantity * ingredient.texture

        # When calculating total score, ensure each value if positive or null
        return (
            max(0, total_capacity)
            * max(0, total_durability)
            * max(0, total_flavor)
            * max(0, total_texture)
        )

    def __repr__(self) -> str:
        return f"<Cookie calories={self.calories} score={self.score}>"
