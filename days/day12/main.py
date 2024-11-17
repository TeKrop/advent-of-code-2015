import json

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    exclude_red: bool

    def __compute_sum(self, content: dict | list | int | str) -> int:
        match content:
            case list():
                return sum(self.__compute_sum(subcontent) for subcontent in content)
            case dict():
                values = list(content.values())
                return (
                    0
                    if self.exclude_red and "red" in values
                    else self.__compute_sum(values)
                )
            case int():
                return content
            case _:
                return 0

    ###########################
    # DAY 12 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.exclude_red = False
        return self.__compute_sum(json.loads(self.line))

    ###########################
    # DAY 12 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self.exclude_red = True
        return self.__compute_sum(json.loads(self.line))
