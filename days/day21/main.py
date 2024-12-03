from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum, auto
from functools import cached_property
from itertools import product
from pathlib import Path

from rich import print

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    shop: "Shop"
    boss: "Boss"
    stuff_combinations: list["Stuff"]
    player_hitpoints: int = 100

    ###########################
    # DAY 21 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        # Instanciate the boss
        self.boss = Boss.from_lines(self.lines)

        # Now the shop and gather possible stuff combinations
        self._init_shop_data()
        self.stuff_combinations = self._get_stuff_combinations()

        return super().solve()

    def _init_shop_data(self) -> None:
        shop_data_file = Path(__file__).parent / "shop.txt"
        print(f"Loading {shop_data_file}...")
        if not shop_data_file.exists():
            raise FileNotFoundError

        shop_data_dict: dict[str, list["Item"]] = defaultdict(list)
        current_category = None
        with shop_data_file.open() as shop_data:
            for line in shop_data:
                line = line.rstrip("\n")
                # Empty line
                if not line:
                    continue

                # Category line
                if ":" in line:
                    current_category = line.split(":")[0].lower()
                    continue

                # Item line
                if "+" in line:
                    line = line.replace(" +", "+")

                name, cost, damage, armor = line.split()
                shop_data_dict[current_category].append(
                    Item(
                        type=ItemType(current_category[:-1]),
                        name=name,
                        cost=int(cost),
                        damage=int(damage),
                        armor=int(armor),
                    )
                )

        self.shop = Shop(**shop_data_dict)

    def _get_stuff_combinations(self) -> list["Stuff"]:
        # Gather all combination possibilities
        weapon_combinations: list[Item] = self.shop.weapons
        armor_combinations: list[Item | None] = self.shop.armors + [None]
        rings_combinations: list[Item | None] = self.shop.rings + [None]

        # List all possible stuff combinations (weapon + armor + rings)
        return list(
            Stuff(items=list(filter(None, items)))
            for items in product(
                weapon_combinations,
                armor_combinations,
                rings_combinations,
                rings_combinations,
            )
        )

    ###########################
    # DAY 21 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        # Return the minimal cost to have the same damage + armor than the boss
        # Calculated by checking if the boss remove more % of hitpoints
        # Don't forget 1 is the minimal damage
        # As we're attacking first, we'll win in that case
        return min(
            (
                stuff.cost
                for stuff in self.stuff_combinations
                if (
                    max(stuff.damage - self.boss.armor, 1) / self.boss.hitpoints
                    >= max(self.boss.damage - stuff.armor, 1) / self.player_hitpoints
                )
            ),
            default=0,
        )

    ###########################
    # DAY 21 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        # Return the max cost to have less damage + armor than the boss
        # Calculated by checking if the boss remove more % of hitpoints
        # Don't forget 1 is the minimal damage
        return max(
            (
                stuff.cost
                for stuff in self.stuff_combinations
                if (
                    max(stuff.damage - self.boss.armor, 1) / self.boss.hitpoints
                    < max(self.boss.damage - stuff.armor, 1) / self.player_hitpoints
                )
            ),
            default=0,
        )


@dataclass
class Boss:
    hitpoints: int
    damage: int
    armor: int

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Boss":
        hitpoints = int(lines[0].split(":")[1])
        damage = int(lines[1].split(":")[1])
        armor = int(lines[2].split(":")[1])
        return cls(hitpoints=hitpoints, damage=damage, armor=armor)


class ItemType(StrEnum):
    WEAPON = auto()
    ARMOR = auto()
    RING = auto()


@dataclass
class Item:
    type: ItemType
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class Stuff:
    items: list[Item]

    @cached_property
    def cost(self) -> int:
        return sum(item.cost for item in self.items)

    @cached_property
    def damage(self) -> int:
        return sum(item.damage for item in self.items)

    @cached_property
    def armor(self) -> int:
        return sum(item.armor for item in self.items)


@dataclass
class Shop:
    weapons: list[Item]
    armors: list[Item]
    rings: list[Item]
