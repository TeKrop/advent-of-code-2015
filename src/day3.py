from .utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    houses: set[tuple[int, int]] = set()

    def __visit_houses(self, line: str):
        # Give the initial gift
        position = (0, 0)
        self.houses.add(position)
        # Now move and give the gifts
        for char in line:
            movement = self.__move(char)
            position = position[0] + movement[0], position[1] + movement[1]
            self.houses.add(position)

    @staticmethod
    def __move(char: str) -> tuple[int, int]:
        match char:
            case "^":
                return (0, -1)
            case "v":
                return (0, 1)
            case ">":
                return (1, 0)
            case "<":
                return (-1, 0)

    ###########################
    # DAY 3 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.houses = set()
        self.__visit_houses(self.line)
        return len(self.houses)

    ###########################
    # DAY 3 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self.houses = set()
        santa_line, robot_line = self.__split_delivery(self.line)
        self.__visit_houses(santa_line)
        self.__visit_houses(robot_line)
        return len(self.houses)

    @staticmethod
    def __split_delivery(line: str) -> tuple[str, str]:
        return line[::2], line[1::2]
