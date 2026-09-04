# B3/S26 Cellular Automaton

A small, interactive 9 × 9 cellular automaton built for an Emergent
Complexity assignment. It uses the outer-totalistic **B3/S26** rule: a variant
of Conway's Game of Life.

## Try it

Open the interactive page at [michaelameng.github.io/ecs-initial](https://michaelameng.github.io/ecs-initial/), or open
[`index.html`](index.html) directly in a browser after cloning this repository.
No installation, Python command, or local server is required to use the page.

The viewer lets you:

- Click a cell to make it alive or dead.
- Advance one generation with **Step**.
- Run or pause the simulation with **Play**.
- Start over with **Clear** or restore the example with **Reset**.

## The rule: B3/S26

Every cell checks its eight adjacent positions: horizontal, vertical, and
diagonal. Cells beyond the edge of the 9 × 9 board are treated as dead.

| Cell state now | Live neighbours | Cell state next generation |
| --- | --- | --- |
| Dead | Exactly 3 | Alive — **B3** (birth) |
| Alive | Exactly 2 or 6 | Alive — **S26** (survival) |
| Any | Any other count | Dead |

Each generation is calculated simultaneously: a cell always uses the previous
generation when deciding its next state.

## Project structure

```text
index.html                 Interactive site published with GitHub Pages
src/simulation/life.py     Python model and B3/S26 rule implementation
src/simulation/__init__.py Package exports for the Python rule model
```

## GitHub Pages

This repository is configured for a project page from the `main` branch root.
In GitHub, use **Settings → Pages**, choose **Deploy from a branch**, then
select `main` and `/(root)`. GitHub serves `index.html` as the site entry point.
