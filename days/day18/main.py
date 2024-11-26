from dataclasses import dataclass
from enum import StrEnum
from functools import cache, cached_property

from rich import print

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 06 - Common Part
    ###########################
    lights_grid: "LightsGrid"
    nb_steps: int = 100

    ###########################
    # DAY 06 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.lights_grid = LightsGrid(lines=self.lines)
        for i in range(self.nb_steps):
            self.lights_grid.apply_next_step(corners_stuck=False)
        return self.lights_grid.get_nb_lights_on()

    ###########################
    # DAY 06 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self.lights_grid = LightsGrid(lines=self.lines)
        self.lights_grid.set_corners_on()
        for i in range(self.nb_steps):
            self.lights_grid.apply_next_step(corners_stuck=True)
        return self.lights_grid.get_nb_lights_on()


class LightState(StrEnum):
    ON = "#"
    OFF = "."


@dataclass
class Light:
    state: LightState


class LightsGrid:
    grid: list[list[Light]]
    size: int

    def __init__(self, lines: list[str]):
        self.size = len(lines)
        self.grid = [[Light(state) for state in line] for line in lines]

    @cached_property
    def corners_coordinates(self) -> set[tuple[int, int]]:
        return {
            (0, 0),
            (0, self.size - 1),
            (self.size - 1, 0),
            (self.size - 1, self.size - 1),
        }

    def set_corners_on(self) -> None:
        for corner_line, corner_column in self.corners_coordinates:
            self.grid[corner_line][corner_column].state = LightState.ON

    def apply_next_step(self, corners_stuck: bool = False) -> None:
        self.grid = [
            [
                self.get_light_next_state(
                    idx_line, idx_column, corners_stuck=corners_stuck
                )
                for idx_column in range(self.size)
            ]
            for idx_line in range(self.size)
        ]

    def get_light_next_state(
        self, idx_line: int, idx_column: int, corners_stuck: bool = False
    ) -> Light:
        light = self.grid[idx_line][idx_column]

        if corners_stuck and self.is_corner_light(idx_line, idx_column):
            return light

        nb_neighbors_on = self.get_nb_neighbors_on(idx_line, idx_column)
        if light.state == LightState.ON:
            # First case : ON and 2 o 3 neighbors on, stay ON, else OFF
            new_state = LightState.ON if nb_neighbors_on in (2, 3) else LightState.OFF
        elif light.state == LightState.OFF:
            # Second case : OFF and 3 neighbors on, turn it on
            new_state = LightState.ON if nb_neighbors_on == 3 else LightState.OFF

        return Light(state=new_state)

    @cache
    def is_corner_light(self, idx_line: int, idx_column: int) -> bool:
        return (idx_line, idx_column) in self.corners_coordinates

    def get_nb_neighbors_on(self, idx_line: int, idx_column: int) -> int:
        return sum(
            1
            for (i_line, i_column) in self.get_neighbors_coordinates(
                idx_line, idx_column
            )
            if (self.grid[i_line][i_column].state == LightState.ON)
        )

    @cache
    def get_neighbors_coordinates(
        self, idx_line: int, idx_column: int
    ) -> set[tuple[int, int]]:
        min_line = max(idx_line - 1, 0)
        max_line = min(idx_line + 1, self.size - 1)
        min_column = max(idx_column - 1, 0)
        max_column = min(idx_column + 1, self.size - 1)

        return {
            (i_line, i_column)
            for i_line in range(min_line, max_line + 1)
            for i_column in range(min_column, max_column + 1)
            if (i_line, i_column) != (idx_line, idx_column)
        }

    def get_nb_lights_on(self) -> int:
        return sum(
            (1 if self.grid[i][j].state == LightState.ON else 0)
            for i in range(self.size)
            for j in range(self.size)
        )

    def __repr__(self) -> str:
        return (
            "\n".join("".join(light.state for light in line) for line in self.grid)
            + "\n"
        )
