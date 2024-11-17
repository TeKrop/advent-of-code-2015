import re
from functools import cached_property

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 08 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(
            string.nb_char_of_code - string.nb_char_in_memory
            for line in self.lines
            if (string := SantaString(line))
        )

    ###########################
    # DAY 08 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(
            string.nb_char_in_encoded_string - string.nb_char_of_code
            for line in self.lines
            if (string := SantaString(line))
        )


class SantaString:
    def __init__(self, line: str):
        self.line = line

    @cached_property
    def nb_char_of_code(self) -> int:
        return len(self.line)

    @cached_property
    def nb_char_in_memory(self) -> int:
        # First replace \xNN with one character
        computed_str = re.sub(r"\\x[a-f0-9]{2}", "'", self.line[1:-1])
        # Then replace the backslashes
        computed_str = computed_str.replace("\\\\", "\\").replace('\\"', '"')
        return len(computed_str)

    @cached_property
    def nb_char_in_encoded_string(self) -> int:
        nb_quotes = self.line.count('"')
        nb_backslashes = self.line.count("\\")
        return self.nb_char_of_code + nb_quotes + nb_backslashes + 2
