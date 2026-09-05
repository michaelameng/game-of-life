"""Simulation rules for a 27 by 27 outer-totalistic cellular automaton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# Coordinates use (column, row), while the nested list is accessed as [row][column].
WIDTH = 27
HEIGHT = 27
RULE = "B3/S26"
# Keep the rule in sets so ``neighbours in ...`` reads like the rule definition.
_BIRTH_COUNTS = frozenset({3})
_SURVIVAL_COUNTS = frozenset({2, 6})


@dataclass(frozen=True)
class LifeGrid:
    """An immutable 27 by 27 grid whose cells are either alive or dead."""

    cells: tuple[tuple[bool, ...], ...]

    def __post_init__(self) -> None:
        if len(self.cells) != HEIGHT or any(len(row) != WIDTH for row in self.cells):
            raise ValueError(f"A LifeGrid must be exactly {WIDTH} by {HEIGHT} cells.")

    @classmethod
    def from_alive_cells(cls, alive_cells: Iterable[tuple[int, int]]) -> "LifeGrid":
        """Build a grid from zero-indexed ``(column, row)`` live-cell positions."""
        # Start with every cell dead, then turn on only the supplied coordinates.
        grid = [[False] * WIDTH for _ in range(HEIGHT)]
        for column, row in alive_cells:
            if not (0 <= column < WIDTH and 0 <= row < HEIGHT):
                raise ValueError(
                    f"Cell ({column}, {row}) is outside the {WIDTH} by {HEIGHT} grid."
                )
            grid[row][column] = True
        # Tuples make the returned grid immutable, so a generation cannot be
        # accidentally changed while calculating the next one.
        return cls(tuple(tuple(row) for row in grid))

    def living_neighbours(self, column: int, row: int) -> int:
        """Count live Moore-neighbours; cells beyond an edge are dead."""
        # Clamp the ranges at the edges. This treats locations outside the grid
        # as dead rather than wrapping the grid around like a torus.
        return sum(
            self.cells[neighbour_row][neighbour_column]
            for neighbour_row in range(max(0, row - 1), min(HEIGHT, row + 2))
            for neighbour_column in range(max(0, column - 1), min(WIDTH, column + 2))
            if (neighbour_column, neighbour_row) != (column, row)
        )

    def step(
        self,
        birth_counts: frozenset[int] = _BIRTH_COUNTS,
        survival_counts: frozenset[int] = _SURVIVAL_COUNTS,
    ) -> "LifeGrid":
        """Advance one generation.

        Defaults to the B3/S26 rule, but a caller (such as the local server's
        interactive rule picker) can pass different neighbour-count sets to
        play a different outer-totalistic variant without editing this file.
        """
        next_alive = []
        for row in range(HEIGHT):
            for column in range(WIDTH):
                neighbours = self.living_neighbours(column, row)
                alive = self.cells[row][column]
                if (not alive and neighbours in birth_counts) or (
                    alive and neighbours in survival_counts
                ):
                    next_alive.append((column, row))
        # Build a new grid only after every decision used the old grid. This is
        # essential: all cells in one generation change simultaneously.
        return LifeGrid.from_alive_cells(next_alive)

    def as_numbers(self) -> list[list[int]]:
        """Return cells in a JSON-friendly 0 (dead) / 1 (alive) representation."""
        return [[int(alive) for alive in row] for row in self.cells]
