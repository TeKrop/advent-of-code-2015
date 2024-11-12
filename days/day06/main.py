from enum import StrEnum

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 06 - Common Part
    ###########################
    lights_grid: "LightsGrid"
    grid_size: int = 1_000

    def _solve(self, brightness: bool = False) -> None:
        self.lights_grid = LightsGrid(size=self.grid_size, brightness=brightness)
        for line in self.lines:
            self.lights_grid.apply_instruction_line(InstructionLine(line))
        return self.lights_grid.lights_on

    ###########################
    # DAY 06 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self._solve(brightness=False)

    ###########################
    # DAY 06 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return self._solve(brightness=True)


class Instruction(StrEnum):
    TURN_ON = "turn on"
    TOGGLE = "toggle"
    TURN_OFF = "turn off"


class InstructionLine:
    instruction: Instruction
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]

    def __init__(self, line: str):
        line_parts = line.split()
        if len(line_parts) == 5:
            instruction_start, instruction_end, start_pos, _, end_pos = line_parts
            instruction = f"{instruction_start} {instruction_end}"
        else:
            instruction, start_pos, _, end_pos = line_parts

        self.instruction = Instruction(instruction)
        self.start_pos = tuple(int(value) for value in start_pos.split(","))
        self.end_pos = tuple(int(value) for value in end_pos.split(","))

    def __repr__(self) -> str:
        return (
            f"InstructionLine({self.instruction} -> {self.start_pos}..{self.end_pos})"
        )

    def apply(self, source_value: int, brightness: bool) -> int:
        if not brightness:
            return self._apply_on_off(source_value)
        else:
            return self._apply_brightness(source_value)

    def _apply_on_off(self, source_value: int) -> int:
        match self.instruction:
            case Instruction.TURN_ON:
                return 1
            case Instruction.TURN_OFF:
                return 0
            case Instruction.TOGGLE:
                return 1 if source_value == 0 else 0

    def _apply_brightness(self, source_value: int) -> int:
        match self.instruction:
            case Instruction.TURN_ON:
                return source_value + 1
            case Instruction.TURN_OFF:
                return max(source_value - 1, 0)
            case Instruction.TOGGLE:
                return source_value + 2


class LightsGrid:
    grid: list[list[int]]
    size: int
    brightness: bool

    def __init__(self, size: int, brightness: bool = False):
        self.size = size
        self.grid = [[0 for j in range(self.size)] for i in range(self.size)]
        self.brightness = brightness

    def apply_instruction_line(self, line: InstructionLine) -> None:
        for i in range(line.start_pos[0], line.end_pos[0] + 1):
            for j in range(line.start_pos[1], line.end_pos[1] + 1):
                self.grid[i][j] = line.apply(
                    source_value=self.grid[i][j], brightness=self.brightness
                )

    @property
    def lights_on(self) -> int:
        return sum(self.grid[i][j] for i in range(self.size) for j in range(self.size))
