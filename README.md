# Initial Emergent Complexity Assignment

Initial Emergent Complexity assignment looking into (i) _Game of Life_-like simulations, (ii) **outer-totalistic rules**, and (iii) \[the additional option\].

## Overview

This project implements a 9 × 9, two-dimensional cellular automaton using the
outer-totalistic **B3/S26** rule. A dead cell becomes alive with exactly three
live neighbours; a live cell remains alive with exactly two or six neighbours.
Cells beyond the grid edge are considered dead.

## View the simulation

The interactive, standalone page is already included at
[`index.html`](index.html). Open that file directly in a browser; no
Python command or local server is needed.

### Publish with GitHub Pages

In the GitHub repository, open **Settings → Pages**. Under **Build and
deployment**, select **Deploy from a branch**, choose `main`, and select
`/(root)`. Save the setting. GitHub will then publish `index.html`
as the project website.

The page has Step, Play/Pause, Clear, and Reset controls, and every cell can be
toggled by clicking it.

## Optional Python generator

The Python files remain as a reference implementation of the same rule and can
regenerate an HTML viewer if you make changes to the Python starting pattern:

```bash
PYTHONPATH=src python3 -m simulation --output path/to/viewer.html
```

## Structure
