# How the B3/S26 Simulation Works

## The idea

The program models a small two-dimensional cellular automaton: a 9 × 9 board
of cells. Every cell is either **alive** or **dead**. The board changes one
generation at a time based only on each cell's eight surrounding positions
(horizontal, vertical, and diagonal neighbours).

The rule is written **B3/S26**:

| Part | Meaning |
| --- | --- |
| `B3` | A dead cell is **born** when it has exactly 3 live neighbours. |
| `S26` | A live cell **survives** when it has exactly 2 or 6 live neighbours. |

All other cells are dead in the next generation. The board does not wrap:
anything beyond an edge is treated as a dead cell.

## Project files

| File | Responsibility |
| --- | --- |
| `src/simulation/life.py` | The Python model: stores the board, counts neighbours, and calculates one new generation. |
| `src/simulation/viewer.py` | Turns an initial Python board into one self-contained HTML file with CSS and JavaScript. |
| `src/simulation/__main__.py` | Reads command-line options, writes the HTML file, and optionally opens it. |
| `src/simulation/__init__.py` | Makes the main model objects available when importing `simulation`. |

## The Python model

`LifeGrid.cells` is a tuple of rows, each containing boolean values. `True`
means alive and `False` means dead. Although the model accepts coordinates as
`(column, row)`, access to the nested grid is `cells[row][column]`.

`LifeGrid.from_alive_cells(...)` is a convenient constructor. Give it a list
of live positions, such as `[(2, 2), (3, 2)]`; it creates the other 79 cells
as dead. It validates that every supplied coordinate is inside the 9 × 9 board.

`living_neighbours(column, row)` examines the surrounding 3 × 3 area, skips
the centre, and counts its live cells. At an edge, its range is shortened so
the program never looks outside the board.

`step()` is the central method:

1. It visits all 81 cells.
2. It counts each cell's live neighbours in the current grid.
3. It applies B3 to dead cells and S26 to live cells.
4. It creates and returns a **new** `LifeGrid` for the result.

Making a new grid is important. If the program changed cells while looping,
later cells would see a mixture of old and new values. Cellular automata need
every cell to update simultaneously.

## The browser page

When `render_html()` runs, it embeds the 9 × 9 starting grid into a standalone
HTML document. No server, package, or internet connection is needed after the
file has been generated.

The JavaScript in that page keeps its own numeric grid: `1` is alive and `0`
is dead. `draw()` creates one button per cell and colours live cells green.
Clicking a button toggles that cell and pauses Play so you can edit safely.

The browser's `step()` function follows the same B3/S26 logic as
`LifeGrid.step()`. Its use of `map()` creates a new array rather than changing
the old array while it is still being read.

The buttons do the following:

- **Step** advances exactly one generation.
- **Play/Pause** advances every 450 milliseconds, or stops that timer.
- **Clear** makes every cell dead and resets the generation number.
- **Reset** restores the original starting pattern.

## Running it

From the project root:

```bash
PYTHONPATH=src python3 -m simulation --open
```

This writes `game_of_life.html` and asks your default browser to open it. To
write a page somewhere else, use `--output`, for example:

```bash
PYTHONPATH=src python3 -m simulation --output demo.html
```

You can open the generated `.html` file directly later; it works locally.
