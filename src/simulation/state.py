"""Stateful session wrapper around :class:`~src.simulation.life.LifeGrid`.

This is the one piece of mutable bookkeeping (history, current rule) that
sits on top of the immutable ``LifeGrid`` model. ``index.html`` calls it
directly from the browser via Pyodide, so the GitHub Pages build runs this
exact file instead of a JavaScript port of it.
"""

from __future__ import annotations

import random

from .life import HEIGHT, WIDTH, LifeGrid, _BIRTH_COUNTS, _SURVIVAL_COUNTS


class SimulationState:
    """In-memory session state for a single interactive board."""

    def __init__(self) -> None:
        self.birth_counts = set(_BIRTH_COUNTS)
        self.survival_counts = set(_SURVIVAL_COUNTS)
        self.history: list[LifeGrid] = [LifeGrid.from_alive_cells([])]
        self.gen_index = 0

    @property
    def grid(self) -> LifeGrid:
        return self.history[self.gen_index]

    def reset(self) -> None:
        """Blank the board and return to step 0, keeping the current rule."""
        self.history = [LifeGrid.from_alive_cells([])]
        self.gen_index = 0

    def step_forward(self) -> None:
        # Reuse an already-computed future state (e.g. after stepping back)
        # rather than recomputing it, so redo after undo is instant.
        if self.gen_index + 1 < len(self.history):
            self.gen_index += 1
            return
        next_grid = self.grid.step(
            birth_counts=frozenset(self.birth_counts),
            survival_counts=frozenset(self.survival_counts),
        )
        self.history.append(next_grid)
        self.gen_index += 1

    def step_back(self) -> None:
        if self.gen_index > 0:
            self.gen_index -= 1

    def toggle(self, column: int, row: int) -> None:
        if not (0 <= column < WIDTH and 0 <= row < HEIGHT):
            return
        alive = {
            (c, r)
            for r, cols in enumerate(self.grid.as_numbers())
            for c, value in enumerate(cols)
            if value
        }
        alive.symmetric_difference_update({(column, row)})
        # Editing invalidates any redo states, matching a fresh branch in history.
        self.history = self.history[: self.gen_index + 1]
        self.history[self.gen_index] = LifeGrid.from_alive_cells(alive)

    def randomize(self, density: float = 0.25) -> None:
        alive = [
            (column, row)
            for row in range(HEIGHT)
            for column in range(WIDTH)
            if random.random() < density
        ]
        self.history = [LifeGrid.from_alive_cells(alive)]
        self.gen_index = 0

    def set_rule(self, birth: list[int], survival: list[int]) -> None:
        self.birth_counts = {n for n in birth if 0 <= n <= 8}
        self.survival_counts = {n for n in survival if 0 <= n <= 8}

    def as_json(self) -> dict:
        cells = self.grid.as_numbers()
        return {
            "cells": cells,
            "generation": self.gen_index,
            "livingCells": sum(sum(row) for row in cells),
            "birth": sorted(self.birth_counts),
            "survival": sorted(self.survival_counts),
            "width": WIDTH,
            "height": HEIGHT,
        }
