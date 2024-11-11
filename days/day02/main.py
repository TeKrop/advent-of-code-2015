from functools import cached_property

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    def solve(self) -> tuple[int, int]:
        self.boxes = [Box(line) for line in self.lines]
        return super().solve()

    ###########################
    # DAY 2 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(box.total_surface + box.smallest_area for box in self.boxes)

    ###########################
    # DAY 2 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(box.smallest_perimeter + box.volume for box in self.boxes)


class Box:
    length: int
    width: int
    height: int

    def __init__(self, line: str):
        self.length, self.width, self.height = [
            int(dimension) for dimension in line.split("x")
        ]

    @cached_property
    def surfaces(self) -> list[int]:
        return [
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        ]

    @cached_property
    def total_surface(self):
        return sum(2 * surface for surface in self.surfaces)

    @cached_property
    def smallest_area(self):
        return min(self.surfaces)

    @cached_property
    def smallest_perimeter(self):
        sorted_dimensions = sorted([self.length, self.width, self.height])
        return sorted_dimensions[0] * 2 + sorted_dimensions[1] * 2

    @cached_property
    def volume(self):
        return self.length * self.width * self.height
