"""Command-line entry point for creating the local HTML simulation viewer."""

from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from .viewer import write_viewer


def main() -> None:
    # argparse supplies a helpful ``--help`` screen and validates the options.
    parser = argparse.ArgumentParser(description="Create a local B3/S26 simulation viewer.")
    parser.add_argument("--output", type=Path, default=Path("game_of_life.html"), help="HTML file to create (default: game_of_life.html)")
    parser.add_argument("--open", action="store_true", help="Open the generated page in your default browser")
    arguments = parser.parse_args()
    # Writing first means the browser receives a real local file to display.
    output = write_viewer(arguments.output)
    print(f"Created {output}")
    if arguments.open:
        # as_uri() produces a file:// URL that browsers understand.
        webbrowser.open(output.as_uri())


if __name__ == "__main__":
    main()
