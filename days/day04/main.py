from hashlib import md5

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 4 - Common Part
    ###########################
    number_of_zeros: int

    def __compute_hashes(self) -> int:
        self.zeros_string = self.number_of_zeros * "0"
        number = 1
        hashed_line = self.__get_hashed_line(number)
        while not self.__is_valid_hash(hashed_line):
            number += 1
            hashed_line = self.__get_hashed_line(number)
        return number

    def __is_valid_hash(self, hashed_line: str) -> bool:
        return hashed_line[: self.number_of_zeros] == self.zeros_string

    def __get_hashed_line(self, number: int) -> str:
        line_data = f"{self.line}{str(number)}".encode()
        return md5(line_data).hexdigest()

    ###########################
    # DAY 4 - First Part
    ###########################
    def _solve_first_part(self) -> int:
        self.number_of_zeros = 5
        return self.__compute_hashes()

    ###########################
    # DAY 4 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self.number_of_zeros = 6
        return self.__compute_hashes()
