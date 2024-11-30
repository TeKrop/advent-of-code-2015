from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    right_sue_values = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    ###########################
    # DAY 16 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return next(
            sue.number
            for sue in (Sue(line) for line in self.lines)
            if sue.is_the_one(self.right_sue_values)
        )

    ###########################
    # DAY 16 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return next(
            sue.number
            for sue in (Sue(line) for line in self.lines)
            if sue.is_really_the_one(self.right_sue_values)
        )


class Sue:
    greather_than_values: set[str] = {"cats", "trees"}
    fewer_than_values: set[str] = {"pomeranians", "goldfish"}

    def __init__(self, line: str):
        split_str = line.split(": ")
        self.number = int(split_str[0].split()[1])
        self.properties = {
            prop_split[0]: int(prop_split[1])
            for prop in ": ".join(split_str[1:]).split(", ")
            if (prop_split := prop.split(": "))
        }

    def __repr__(self):
        return f"<Sue number={self.number} properties={self.properties}>"

    def is_the_one(self, right_sue_values: dict) -> bool:
        return self.properties.items() <= right_sue_values.items()

    def is_really_the_one(self, right_sue_values: dict) -> bool:
        properties_to_check = self.properties.copy()

        # First check for stop conditions and remove already checked properties
        for value in self.greather_than_values:
            if (
                value in properties_to_check
                and properties_to_check[value] <= right_sue_values[value]
            ):
                return False
            else:
                properties_to_check.pop(value, None)

        for value in self.fewer_than_values:
            if (
                value in properties_to_check
                and properties_to_check[value] >= right_sue_values[value]
            ):
                return False
            else:
                properties_to_check.pop(value, None)

        # Make sure the remaining items are a subpart of right values
        return properties_to_check.items() <= right_sue_values.items()
