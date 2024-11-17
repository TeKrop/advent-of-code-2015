import re
import string
from functools import cache, cached_property
from itertools import pairwise

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    letters = list(string.ascii_lowercase)
    forbidden_letters = {"i", "o", "l"}
    password_length = 8

    @cached_property
    def forbidden_letters_regexp(self) -> re.Pattern:
        return re.compile("|".join(map(re.escape, self.forbidden_letters)))

    @cached_property
    def three_letters_groups(self) -> set[str]:
        return set(
            combination
            for i in range(len(self.letters) - 2)
            if (
                (
                    combination
                    := f"{self.letters[i]}{self.letters[i+1]}{self.letters[i+2]}"
                )
                and not self.__contains_forbidden_letter(combination)
            )
        )

    @cached_property
    def three_letters_groups_regexp(self) -> re.Pattern:
        return re.compile("|".join(map(re.escape, self.three_letters_groups)))

    def __contains_forbidden_letter(self, letters: str) -> bool:
        return bool(self.forbidden_letters_regexp.search(letters))

    def __contains_group_of_three_letters(self, letters: str) -> bool:
        return bool(self.three_letters_groups_regexp.search(letters))

    def __get_next_valid_password(self, password: str) -> str:
        # First, increment earliest located invalid char for performances
        next_password = self.__increment_earliest_invalid_char(password)

        # Next phase, we should be good with invalid char for now
        next_password = self.__get_next_password(next_password)
        while not self.__is_valid_password(next_password):
            next_password = self.__get_next_password(next_password)
        return next_password

    def __increment_earliest_invalid_char(self, password: str) -> str:
        # Find the first forbidden letter and keep reference
        for char_idx, char in enumerate(password):
            if char in self.forbidden_letters:
                break

        # Construct a new string with next password and trailing "a"
        return (
            f"{self.__get_next_password(password[:char_idx+1])}"
            f"{"a"*(self.password_length - char_idx - 1)}"
        )

    def __get_next_password(self, password: str) -> str:
        # Recursive case, we have to increment previous char and put "a" in last
        if password[-1] == "z":
            return f"{self.__get_next_password(password[:-1])}a"

        # Recursive stop case, we just have to increment last char
        return f"{password[:-1]}{self.__get_next_char(password[-1])}"

    @cache
    def __get_next_char(self, char: str) -> str:
        return chr(ord(char) + 1)

    def __is_valid_password(self, password: str) -> bool:
        return (
            not self.__contains_forbidden_letter(password)
            and self.__contains_group_of_three_letters(password)
            and self.__contains_at_least_two_pairs_of_letters(password)
        )

    def __contains_at_least_two_pairs_of_letters(self, password: str) -> bool:
        letters_pairs = pairwise(password)
        pair_positions: dict[str, int] = {}
        valid_pairs_count = 0

        # Loop over pairs to find out duplicates. Memorise every pair
        # position so we can make sure we won't find overlapping pairs
        for line_idx, letter_pair in enumerate(letters_pairs):
            # Skip pairs without identic letters
            if letter_pair[0] != letter_pair[1]:
                continue

            # If the pair has already been found, make sure
            # it's not overlapping the previous one
            if (
                letter_pair in pair_positions
                and line_idx - pair_positions[letter_pair] == 1
            ):
                # Update the last found pair information
                pair_positions[letter_pair] = line_idx
                continue

            pair_positions[letter_pair] = line_idx
            valid_pairs_count += 1

        return valid_pairs_count >= 2

    ###########################
    # DAY 11 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self.__get_next_valid_password(self.line)

    ###########################
    # DAY 11 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        next_valid_password = self.__get_next_valid_password(self.line)
        return self.__get_next_valid_password(next_valid_password)
