"""Randomly samples 100 rule combinations from the Cartesian product of the power set of all Life birth and survival rules."""

import random
import itertools


def power_set(iterable) -> list[tuple]:
    """Finds the power set of any iterable."""
    s = list(iterable)
    return list(
        itertools.chain.from_iterable(
            # Finds all possible r-length combinations of the iterable, for r in range 0 to the length of the iterable.
            itertools.combinations(s, r)
            for r in range(len(s) + 1)
        )
    )


def cartesian_product(*iterables) -> list[tuple]:
    """Finds the Cartesian product of any number of iterables."""
    return list(itertools.product(*iterables))


def sample_rules(n: int = 100, seed: int | None = None) -> list[tuple]:
    """Randomly samples n rule combinations from the Cartesian product of the power set of all Life birth and survival rules."""
    rules = cartesian_product(
        power_set(
            [0, 1, 2, 3, 4, 5, 6, 7, 8]
        ),  # The power set of all Life birth rules.
        power_set(
            [0, 1, 2, 3, 4, 5, 6, 7, 8]
        ),  # The power set of all Life survival rules.
    )
    sample = random.Random(seed).sample(rules, n)
    for i, (birth, survival) in enumerate(sample, start=1):
        birth_digits = "".join(str(n) for n in birth)
        survival_digits = "".join(str(n) for n in survival)
        print(f"{i:>3}. B{birth_digits}/S{survival_digits}")
    return sample


if __name__ == "__main__":
    sample_rules()
