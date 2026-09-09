# Game of Life

A 27×27 outer-totalistic cellular automaton, playable in the browser at
[michaelameng.github.io/game-of-life](https://michaelameng.github.io/game-of-life/).

Defaults to standard Conway rules, **B3/S23** — a dead cell is born with
exactly 3 live neighbours, and a live cell survives with 2 or 3. The rule
is fully configurable from the page itself via the birth/survival
checkboxes.

## How it runs

`index.html` holds no simulation logic of its own. It loads
[Pyodide](https://pyodide.org/) (CPython compiled to WebAssembly), fetches
the actual files under `src/game_of_life/`, and drives them directly from
JavaScript. There's no build step and no server — GitHub Pages serves the
static files, and the browser runs the real Python.

## Package layout

- `src/game_of_life/life.py` — `LifeGrid`, the immutable grid model and the
  `step()` rule evaluation (birth/survival neighbour-count sets).
- `src/game_of_life/state.py` — `SimulationState`, the mutable session
  wrapper (generation history, undo/redo, randomize, rule selection) that
  `index.html` calls into.
- `src/game_of_life/sample.py` — a standalone script that randomly samples
  rule combinations from the full space of Life-like B/S rules, printed in
  `B.../S...` notation.

## Running the sampler

```sh
python -m src.game_of_life.sample
```

## Running locally

Since it's all static files, any local web server works, e.g.:

```sh
python -m http.server
```

then open `http://localhost:8000`.
