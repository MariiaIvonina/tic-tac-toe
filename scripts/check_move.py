#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOARD_PATH = ROOT / "BOARD.txt"
WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def parse_board(contents: str, name: str) -> list[str]:
    rows = contents.splitlines()
    if len(rows) != 3:
        raise ValueError(f"{name} must contain exactly 3 rows.")

    cells = []
    for row in rows:
        tokens = row.split(" ")
        if len(tokens) != 3 or any(token not in {".", "X", "O"} for token in tokens):
            raise ValueError(f"{name} must have 3 cells per row, separated by single spaces.")
        cells.extend(tokens)
    return cells


def has_winner(cells: list[str]) -> bool:
    return any(
        cells[a] != "." and cells[a] == cells[b] == cells[c]
        for a, b, c in WINNING_LINES
    )


def is_valid_board(cells: list[str]) -> bool:
    x_count = cells.count("X")
    o_count = cells.count("O")
    if x_count not in {o_count, o_count + 1}:
        return False

    x_wins = any(
        cells[a] == cells[b] == cells[c] == "X"
        for a, b, c in WINNING_LINES
    )
    o_wins = any(
        cells[a] == cells[b] == cells[c] == "O"
        for a, b, c in WINNING_LINES
    )
    if x_wins and o_wins:
        return False
    if x_wins and x_count != o_count + 1:
        return False
    if o_wins and x_count != o_count:
        return False

    return is_reachable(cells)


def is_reachable(target: list[str]) -> bool:
    initial = tuple("." for _ in range(9))
    states = {initial}

    for _ in range(9):
        next_states = set()
        for state in states:
            if list(state) == target:
                return True
            if has_winner(list(state)):
                continue

            x_count = state.count("X")
            o_count = state.count("O")
            symbol = "X" if x_count == o_count else "O"
            for index, cell in enumerate(state):
                if cell == ".":
                    next_state = list(state)
                    next_state[index] = symbol
                    next_states.add(tuple(next_state))
        states = next_states

    return tuple(target) in states


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that BOARD.txt contains one legal move for your symbol."
    )
    parser.add_argument("symbol", choices=("X", "O"), help="your mark")
    args = parser.parse_args()
    symbol = args.symbol.upper()

    try:
        previous = subprocess.run(
            ["git", "show", "HEAD:BOARD.txt"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError as error:
        print("Error: could not read BOARD.txt from HEAD; make sure this is a Git repository with a committed board.", file=sys.stderr)
        if error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
        return 1

    try:
        current = BOARD_PATH.read_text()
    except OSError as error:
        print(f"Error: could not read {BOARD_PATH.name}: {error}", file=sys.stderr)
        return 1

    try:
        old_cells = parse_board(previous, "BOARD.txt in HEAD")
        new_cells = parse_board(current, "working BOARD.txt")
    except ValueError as error:
        print(f"Invalid board: {error}", file=sys.stderr)
        return 1

    if not is_valid_board(old_cells):
        print("Invalid board: BOARD.txt in HEAD is not a valid game state.", file=sys.stderr)
        return 1
    if has_winner(old_cells) or "." not in old_cells:
        print("Invalid move: the game was already finished in the previous board.", file=sys.stderr)
        return 1

    expected_symbol = "X" if old_cells.count("X") == old_cells.count("O") else "O"
    if symbol != expected_symbol:
        print(
            f"Invalid move: it is {expected_symbol}'s turn, not {symbol}'s.",
            file=sys.stderr,
        )
        return 1

    if old_cells == new_cells:
        print("No move found: BOARD.txt has not changed from HEAD.", file=sys.stderr)
        return 1

    changes = [
        (before, after)
        for before, after in zip(old_cells, new_cells)
        if before != after
    ]
    if len(changes) != 1 or changes[0][0] != "." or changes[0][1] != symbol:
        print(
            f"Invalid move: change exactly one empty cell to your symbol ({symbol}).",
            file=sys.stderr,
        )
        return 1

    if not is_valid_board(new_cells):
        print("Invalid board: the updated board is not a valid game state.", file=sys.stderr)
        return 1

    print(f"Valid move: one {symbol} was added.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
