from itertools import combinations

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    liters_to_eggnog: int = 150

    def __get_containers(self) -> list[int]:
        return [int(line) for line in self.lines]

    def __get_nb_combinations(self, containers: list[int], nb_containers: int) -> int:
        range_combinations = combinations(containers, nb_containers)
        return sum(
            1
            for combination in range_combinations
            if sum(combination) == self.liters_to_eggnog
        )

    ###########################
    # DAY 17 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        containers = self.__get_containers()
        return self.__get_nb_possible_combinations(containers)

    def __get_nb_possible_combinations(self, containers: list[int]) -> int:
        return sum(
            self.__get_nb_combinations(containers=containers, nb_containers=i + 1)
            for i in range(len(containers))
        )

    ###########################
    # DAY 17 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        containers = self.__get_containers()
        return self.__get_minimum_possible_combinations(containers)

    def __get_minimum_possible_combinations(self, containers: list[int]) -> int | None:
        minimum_combinations = None

        for i in range(len(containers)):
            nb_combinations = self.__get_nb_combinations(
                containers=containers, nb_containers=i + 1
            )
            if nb_combinations > 0:
                minimum_combinations = nb_combinations
                break

        return minimum_combinations
