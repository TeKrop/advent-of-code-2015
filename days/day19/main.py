import re
from collections import defaultdict
from functools import cache


from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    replacements: dict[str, set[str]]
    input_molecule: str

    ###########################
    # DAY 19 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self._process_input()
        return super().solve()

    def _process_input(self) -> None:
        self.input_molecule = ""
        self.replacements = defaultdict(set)

        is_input_molecule = False

        for line in self.lines:
            # Input molecule is the last line we process
            if is_input_molecule:
                self.input_molecule = line
                break

            # If line is empty, next line is input molecule
            if not line:
                is_input_molecule = True
                continue

            # Classic case, replacement line
            left, right = line.split(" => ")
            self.replacements[left].add(right)

        self.replacements = dict(self.replacements)

    def _fabricate_molecules(
        self, input_molecule: str, replacements: dict[str, set[str]]
    ) -> set[str]:
        """Fabricate new molecules given an input molecule and list of replacements"""
        return {
            (
                f"{input_molecule[:index.start()]}"
                f"{replacement}"
                f"{input_molecule[index.start() + len(search) :]}"
            )
            for search, replacements in replacements.items()
            for index in self._get_possible_substrings(search, input_molecule)
            for replacement in replacements
        }

    @cache
    def _get_possible_substrings(
        self, search: str, input_string: str
    ) -> list[re.Match]:
        return list(re.finditer(search, input_string))

    ###########################
    # DAY 19 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self._get_nb_distinct_molecules()

    def _get_nb_distinct_molecules(self) -> int:
        return len(
            self._fabricate_molecules(
                input_molecule=self.input_molecule, replacements=self.replacements
            )
        )

    ###########################
    # DAY 19 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        """Naive solution working because of the way the input is produced.
        Only clever solution is here, taking advantage of input format analysis :
        https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/
        """
        nb_steps = 0

        start_molecule: set[str] = {"e"}
        molecule = self.input_molecule

        # We'll reduce the input molecule until we only have a list of "e" remaining
        while set(molecule) != start_molecule:
            for search, replacements in self.replacements.items():
                for replacement in replacements:
                    if replacement in molecule:
                        molecule = molecule.replace(replacement, search, 1)
                        nb_steps += 1

        return nb_steps
