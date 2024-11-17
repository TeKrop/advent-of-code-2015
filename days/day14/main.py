import re
from enum import Enum, auto
from functools import cached_property
from typing import Iterable

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    race_duration: int = 2503

    ###########################
    # DAY 14 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return max(
            reindeer.get_distance_traveled(seconds=self.race_duration)
            for line in self.lines
            if (reindeer := Reindeer(line))
        )

    ###########################
    # DAY 14 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        reindeers = [Reindeer(line) for line in self.lines]
        return max(
            score
            for score in self.__compute_race_scorings(
                reindeers=reindeers, seconds=self.race_duration
            )
        )

    def __compute_race_scorings(
        self, reindeers: list["Reindeer"], seconds: int
    ) -> Iterable[int]:
        states: dict[Reindeer, ReindeerState] = {
            reindeer: ReindeerState(reindeer) for reindeer in reindeers
        }

        remaining_time = seconds
        while remaining_time > 0:
            # Update reindeers states and gather current distance
            distances = {}
            for reindeer in reindeers:
                states[reindeer].update()
                distances[reindeer] = states[reindeer].distance_traveled

            # Give a point to the first reindeer(s)
            max_distance = max(distances.values())
            for reindeer in reindeers:
                if states[reindeer].distance_traveled == max_distance:
                    states[reindeer].score += 1

            # Decrease time second per second
            remaining_time -= 1

        yield from (states[reindeer].score for reindeer in reindeers)


class Reindeer:
    def __init__(self, line: str):
        name, speed, duration, resting_time = self.reindeer_line_pattern.match(
            line
        ).groups()

        self.name = name
        self.speed = int(speed)
        self.duration = int(duration)
        self.resting_time = int(resting_time)

    @cached_property
    def reindeer_line_pattern(self) -> re.Pattern:
        return re.compile(
            r"^([A-z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds\.$"
        )

    def get_distance_traveled(self, seconds: int) -> int:
        distance_traveled = 0
        remaining_time = seconds

        while remaining_time > 0:
            # Now the reindeer can fly. We're making sure it doesn't fly
            # too much if there isn't enough remaining time
            flying_time = min(remaining_time, self.duration)
            distance_traveled += flying_time * self.speed
            remaining_time -= flying_time

            # Now the reindeer can rest
            remaining_time -= self.resting_time

        return distance_traveled


class ReindeerStatus(Enum):
    FLYING = auto()
    RESTING = auto()


class ReindeerState:
    def __init__(self, reindeer: Reindeer):
        self.reindeer = reindeer

        self.status: ReindeerStatus = ReindeerStatus.FLYING
        self.flying_duration_remaining: int = self.reindeer.duration
        self.resting_time_remaining: int = 0

        self.score: int = 0
        self.distance_traveled: int = 0

    def update(self):
        """Update method triggered for each second"""

        # Update reindeer depending on his status
        match self.status:
            case ReindeerStatus.FLYING:
                # Update his distance traveled
                self.distance_traveled += self.reindeer.speed

                # Update his flying state if accurate
                self.flying_duration_remaining -= 1
                if self.flying_duration_remaining == 0:
                    self.status = ReindeerStatus.RESTING
                    self.resting_time_remaining = self.reindeer.resting_time

            case ReindeerStatus.RESTING:
                # Update his resting state if accurate
                self.resting_time_remaining -= 1
                if self.resting_time_remaining == 0:
                    self.status = ReindeerStatus.FLYING
                    self.flying_duration_remaining = self.reindeer.duration
