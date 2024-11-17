import re
from enum import StrEnum
from functools import cached_property
from itertools import permutations

from scripts.utils import AbstractPuzzleSolver


class GuestLineAction(StrEnum):
    GAIN = "gain"
    LOSE = "lose"


class PuzzleSolver(AbstractPuzzleSolver):
    action_values: dict[str, GuestLineAction] = {
        GuestLineAction.GAIN: 1,
        GuestLineAction.LOSE: -1,
    }
    nb_guests: int
    myself_name: str = "Myself"

    @cached_property
    def guest_line_pattern(self) -> re.Pattern:
        return re.compile(
            r"^([A-z]+) would (gain|lose) ([0-9]+) happiness units by sitting next to ([A-z]+)\.$"
        )

    def __compute_guests(self, include_myself: bool) -> list["Guest"]:
        guests: dict[str, "Guest"] = {}

        if include_myself:
            guests[self.myself_name] = Guest(name=self.myself_name)

        for line in self.lines:
            guest, action, score, other_guest = self.guest_line_pattern.match(
                line
            ).groups()

            if guest not in guests:
                guests[guest] = Guest(name=guest)
                if include_myself:
                    guests[self.myself_name].happiness[guest] = 0
                    guests[guest].happiness[self.myself_name] = 0

            guests[guest].happiness[other_guest] = (
                int(score) * self.action_values[action]
            )

        self.nb_guests = len(guests)

        return list(guests.values())

    def __get_optimal_seating_arrangement_happiness(self, guests: list["Guest"]) -> int:
        # To make permutations, as they're circular, always take the same value
        # for the first guest of the list, and make permutations of the remaining guests
        possible_seating_arrangements = [
            guests[:1] + list(perm) for perm in permutations(guests[1:])
        ]

        return max(
            self.__get_seating_arrangement_happiness(arrangement)
            for arrangement in possible_seating_arrangements
        )

    def __get_seating_arrangement_happiness(self, guests: list["Guest"]) -> int:
        return sum(
            guest.happiness[previous_guest.name] + guest.happiness[next_guest.name]
            for guest_idx, guest in enumerate(guests)
            if (
                (previous_guest := guests[(guest_idx - 1) % self.nb_guests])
                and (next_guest := guests[(guest_idx + 1) % self.nb_guests])
            )
        )

    ###########################
    # DAY 13 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        guests = self.__compute_guests(include_myself=False)
        return self.__get_optimal_seating_arrangement_happiness(guests)

    ###########################
    # DAY 13 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        guests = self.__compute_guests(include_myself=True)
        return self.__get_optimal_seating_arrangement_happiness(guests)


class Guest:
    name: str
    happiness: dict["Guest", int]

    def __init__(self, name: str):
        self.name = name
        self.happiness = {}

    def __repr__(self) -> str:
        return f"<Guest name={self.name} happiness={self.happiness}>"
