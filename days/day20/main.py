import math
from typing import Generator

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 20 - Common Part
    ###########################
    prime_limit = 10**6

    def solve(self) -> tuple[int, int]:
        self.primes: list[int] = list(self.get_prime_numbers(self.prime_limit))
        return super().solve()

    ###########################
    # DAY 20 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        minimum_to_reach = int(self.line)

        house_number = 0
        numbers_of_gift = 0

        while numbers_of_gift < minimum_to_reach:
            house_number += 1
            numbers_of_gift = self.get_nb_gifts_for_house(
                number=house_number, gifts_per_elf=10
            )

        return house_number

    def get_nb_gifts_for_house(self, number: int, gifts_per_elf: int) -> int:
        return self.get_sum_of_divisors(number) * gifts_per_elf

    def get_sum_of_divisors(self, number: int) -> int:
        """Calculate the sum of divisors of a number using its prime factorization."""
        sum_of_divisors = 1

        for prime in self.primes:
            # Stop condition, we can't divide the number by prime factor anymore
            if prime * prime > number:
                break

            # Number can't be divided by this prime factor, move on to the next
            if number % prime != 0:
                continue

            # Loop over the number until it can't be divided by the prime factor
            power_sum = 1
            power = 1
            while number % prime == 0:
                number //= prime  # Floor division to keep integers
                power *= prime
                power_sum += power

            sum_of_divisors *= power_sum

        # If there is any prime factor greater than sqrt(number), result here isn't 1
        # and we can multiply by its factorization (n^0 + n^1)
        if number > 1:
            sum_of_divisors *= 1 + number

        return sum_of_divisors

    def get_prime_numbers(self, limit: int) -> Generator[int, None, None]:
        """Generate a list of primes up to the given limit using
        the Sieve of Eratosthenes."""

        # Initialize the boolean list as prime until limit
        # 0 and 1 won't be of any use, keeping them for better
        # process understanding in the loop
        is_prime = [True] * (limit + 1)

        # Loop over until square root of limit we put
        for i in range(2, int(math.sqrt(limit)) + 1):
            # If number is not prime, we ignore
            if not is_prime[i]:
                continue

            # Current number is prime, yield it
            yield i

            # All his multiple aren't prime, set them as not prime
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    ###########################
    # DAY 20 - Second Part
    ###########################
    houses_per_elf = 50

    def _solve_second_part(self) -> int:
        minimum_to_reach = int(self.line)

        house_number = 0
        numbers_of_gift = 0

        while numbers_of_gift < minimum_to_reach:
            house_number += 1
            numbers_of_gift = self.get_naive_nb_gifts_for_house(
                number=house_number, gifts_per_elf=11
            )

        return house_number

    def get_naive_nb_gifts_for_house(self, number: int, gifts_per_elf: int) -> int:
        return self.get_naive_sum_of_divisors(number) * gifts_per_elf

    def get_naive_sum_of_divisors(self, number: int) -> int:
        """Get the sum of divisors in a naive way, by skipping elves
        which have already stopped and won't reach the house with given number.

        We'll use the naive approach to iterate from 1 to square root, but only
        adding values superior to the minimum (number divided by delivery limit)
        """
        total = 0
        minimum_value = number // self.houses_per_elf
        end_range = int(math.sqrt(number) + 1)

        for i in range(1, end_range):
            # Ignore values that aren't divisors
            if number % i != 0:
                continue

            # Add the current value if the minimum
            if i >= minimum_value:
                total += i

            # Same thing for the opposite factor value
            opposite_i = number // i
            if opposite_i != i and opposite_i >= minimum_value:
                total += opposite_i

        return total
