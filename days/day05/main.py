from itertools import pairwise

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 5 - First Part
    ###########################
    vowels = {"a", "e", "i", "o", "u"}
    wrong_strings = {"ab", "cd", "pq", "xy"}

    def _solve_first_part(self) -> int:
        return len([line for line in self.lines if self.__is_nice_string(line)])

    def __is_nice_string(self, line: str) -> bool:
        return (
            self.__contains_at_least_three_vowels(line)
            and self.__contains_double_letters(line)
            and not self.__contains_at_least_one_wrong_string(line)
        )

    def __contains_at_least_three_vowels(self, line: str) -> bool:
        return len([char for char in line if char in self.vowels]) >= 3

    @staticmethod
    def __contains_double_letters(line: str) -> bool:
        return any(line[i] == line[i - 1] for i in range(1, len(line)))

    def __contains_at_least_one_wrong_string(self, line: str) -> bool:
        return any(wrong_string in line for wrong_string in self.wrong_strings)

    ###########################
    # DAY 5 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return len(
            [line for line in self.lines if self.__is_really_a_nice_string(line)]
        )

    def __is_really_a_nice_string(self, line: str) -> bool:
        return self.__contains_pair_of_double_letters(
            line
        ) and self.__contains_letter_repeating_itself_with_one_between(line)

    def __contains_pair_of_double_letters(self, line: str) -> bool:
        letters_pairs = pairwise(line)
        pair_positions: dict[str, int] = {}

        # Loop over pairs to find out duplicates. Memorise every pair
        # position so we can make sure we won't find overlapping pairs
        for line_idx, letter_pair in enumerate(letters_pairs):
            if letter_pair not in pair_positions:
                pair_positions[letter_pair] = line_idx
                continue

            # Make sure the pairs aren't overlapping
            # Else continue to search
            if line_idx - pair_positions[letter_pair] > 1:
                return True

        return False

    def __contains_letter_repeating_itself_with_one_between(self, line: str) -> bool:
        return any(line[i - 1] == line[i + 1] for i in range(1, len(line) - 1))
