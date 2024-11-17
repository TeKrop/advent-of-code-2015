from io import StringIO

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    def __look_and_say(self, number: str, iterations: int) -> int:
        """Recursive method for look and say"""

        # Recursive stop condition
        if iterations == 0:
            return number

        # Process the numbers into a new one
        result_number = self.__process_chars(number)

        # Apply principle recursively
        return self.__look_and_say(result_number, iterations - 1)

    def __process_chars(self, number: str) -> str:
        buffer = StringIO()

        # Initialize with values of first char
        previous_char: str = number[0]
        nb_previous_char: int = 1

        for char in number[1:]:
            # If we stopped having the same char, stop counting
            if previous_char != char:
                buffer.write(f"{nb_previous_char}{previous_char}")
                nb_previous_char = 0

            # Store the information about future previous char
            nb_previous_char += 1
            previous_char = char

        # Last step after iteration
        if nb_previous_char > 0:
            buffer.write(f"{nb_previous_char}{previous_char}")

        return buffer.getvalue()

    ###########################
    # DAY 10 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return len(self.__look_and_say(number=self.line, iterations=40))

    ###########################
    # DAY 10 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return len(self.__look_and_say(number=self.line, iterations=50))
