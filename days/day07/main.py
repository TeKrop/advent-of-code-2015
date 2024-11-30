from enum import StrEnum
from functools import cache

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 07 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        booklet = Booklet(lines=self.lines)
        return booklet["a"]

    ###########################
    # DAY 07 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        booklet = Booklet(lines=self.lines)
        booklet["b"] = booklet["a"]
        booklet.reset()
        return booklet["a"]


class Operator(StrEnum):
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    NOT = "NOT"


class Signal:
    first: str | None = None
    operator: Operator | None = None
    second: str | None = None

    def __init__(self, signal_str: str):
        split_str = signal_str.split(" ")
        if len(split_str) == 1:
            self.first = split_str[0]
        elif len(split_str) == 2:
            self.operator, self.second = Operator(split_str[0]), split_str[1]
        else:
            self.first, operator_str, self.second = split_str
            self.operator = Operator(operator_str)


class Instruction:
    signal: Signal
    wire: str

    def __init__(self, line: str):
        signal_str, wire_str = map(str.strip, line.split("->"))
        self.wire, self.signal = wire_str, Signal(signal_str)


class Booklet:
    instructions: list[Instruction]
    signals: dict[str, Signal]
    signal_limit: int = 65535  # 2^16 - 1

    def __init__(self, lines: list[str]):
        self.signals = {
            instruction.wire: instruction.signal
            for line in lines
            if (instruction := Instruction(line))
        }

    def __getitem__(self, wire_key: str) -> int:
        return self.get(wire_key)

    def __setitem__(self, wire_key: str, value: int | str) -> int:
        self.signals[wire_key] = Signal(str(value))

    @cache
    def compute(self, key: str) -> int:
        try:
            return int(key)
        except ValueError:
            return self.get(key)

    @cache
    def get(self, wire_key: str) -> int:
        signal = self.signals[wire_key]
        match signal.operator:
            case None:
                return self.compute(signal.first)
            case Operator.AND:
                return self.compute(signal.first) & self.compute(signal.second)
            case Operator.OR:
                return self.compute(signal.first) | self.compute(signal.second)
            case Operator.LSHIFT:
                return self.compute(signal.first) << self.compute(signal.second)
            case Operator.RSHIFT:
                return self.compute(signal.first) >> self.compute(signal.second)
            case Operator.NOT:
                return ~self.compute(signal.second) & self.signal_limit
        raise ValueError

    def reset(self) -> None:
        self.compute.cache_clear()
        self.get.cache_clear()
