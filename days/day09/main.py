from itertools import permutations
from typing import Callable

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    distances: dict[frozenset, int]
    locations: set[str]

    def __compute_distances(self):
        self.distances = {}
        self.locations = set()

        for line in self.lines:
            distance = Distance(line)
            self.distances[distance.locations] = distance.length
            self.locations |= distance.locations

    def __compute_path(self, path: list[str]) -> int:
        return sum(
            self.distances[frozenset({path[i], path[i + 1]})]
            for i in range(len(path) - 1)
        )

    def _solve(self, get_result_func: Callable) -> int:
        # Compute references of distances and set of locations
        # Fills self.distances and self.locations
        self.__compute_distances()

        # Gather a list of possible paths
        possible_paths = permutations(self.locations)

        # Loop over possible paths and find the min or max length
        return get_result_func(self.__compute_path(path) for path in possible_paths)

    ###########################
    # DAY 09 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self._solve(get_result_func=min)

    ###########################
    # DAY 09 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return self._solve(get_result_func=max)


class Distance:
    locations: frozenset[str]
    length: int

    def __init__(self, line: str):
        first_location, _, second_location, _, length = line.split()
        self.locations = frozenset({first_location, second_location})
        self.length = int(length)

    def __repr__(self) -> str:
        return f"<Distance locations={self.locations} length={self.length} />"
