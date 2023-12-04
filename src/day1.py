from functools import cached_property

from .utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    @cached_property
    def line(self):
        return self.lines[0]

    @staticmethod
    def __get_char_value(char: str) -> int:
        return 1 if char == "(" else (-1 if char == ")" else 0)

    ###########################
    # DAY 1 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(self.__get_char_value(char) for char in self.line)

    ###########################
    # DAY 1 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        floor = 0

        for position, char in enumerate(self.line):
            floor += self.__get_char_value(char)
            if floor == -1:
                break

        return position + 1
