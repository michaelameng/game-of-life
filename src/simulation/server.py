"""A dependency-free local HTTP server that runs the LifeGrid simulation.

Run it with::

    python3 -m src.simulation.server

then open http://localhost:8000/. Every step, cell toggle, randomize, and
rule change is computed by :class:`~src.simulation.life.LifeGrid` itself, so
this is the Python model actually driving a UI rather than sitting unused
next to the browser's own JavaScript implementation.
"""

from __future__ import annotations

import json
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .life import HEIGHT, WIDTH, LifeGrid, _BIRTH_COUNTS, _SURVIVAL_COUNTS

_PAGE_PATH = Path(__file__).with_name("server_page.html")


class _SimulationState:
    """In-memory session state for the single local user this server serves."""

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
        # rather than recomputing it, mirroring the browser's undo/redo stack.
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
        # Editing invalidates any redo states, same as clicking a cell in the browser.
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


_state = _SimulationState()


class SimulationRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            body = _PAGE_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/state":
            self._send_json(_state.as_json())
        else:
            self.send_error(404, "Not found")

    def do_POST(self) -> None:
        if self.path == "/api/step":
            _state.step_forward()
        elif self.path == "/api/step-back":
            _state.step_back()
        elif self.path == "/api/random":
            _state.randomize()
        elif self.path == "/api/reset":
            _state.reset()
        elif self.path == "/api/toggle":
            data = self._read_json()
            try:
                _state.toggle(int(data["column"]), int(data["row"]))
            except (KeyError, TypeError, ValueError):
                self.send_error(400, "Expected integer 'column' and 'row'")
                return
        elif self.path == "/api/rule":
            data = self._read_json()
            _state.set_rule(data.get("birth", []), data.get("survival", []))
        else:
            self.send_error(404, "Not found")
            return
        self._send_json(_state.as_json())


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), SimulationRequestHandler)
    print(f"Serving the Game of Life simulation at http://{host}:{port}/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
