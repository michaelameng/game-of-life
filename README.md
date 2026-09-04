# Initial Emergent Complexity Assignment

Initial Emergent Complexity assignment looking into (i) _Game of Life_-like simulations, (ii) **outer-totalistic rules**, and (iii) \[the additional option\].

## Overview

This project implements a 9 × 9, two-dimensional cellular automaton using the
outer-totalistic **B3/S26** rule. A dead cell becomes alive with exactly three
live neighbours; a live cell remains alive with exactly two or six neighbours.
Cells beyond the grid edge are considered dead.

## Run it

From the project root, generate and open the standalone visual simulation:

```bash
PYTHONPATH=src python3 -m simulation --open
```

This creates `game_of_life.html` in the project root. You can also open that
file directly in any browser. The page has Step, Play/Pause, Clear, and Reset
controls, and every cell can be toggled by clicking it.

To choose another output location:

```bash
PYTHONPATH=src python3 -m simulation --output path/to/viewer.html
```

## Structure
