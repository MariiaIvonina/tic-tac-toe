# Tic-Tac-Toe Board Rules

This project is a Git-based tic-tac-toe game. Players update the shared `BOARD.txt` and must follow the legal game rules defined in `docs/PRD.md`.

## Required board format

`BOARD.txt` must contain exactly three rows of three cells:

- each row must have exactly three entries
- entries are separated by single spaces
- cells may only be `X`, `O`, or `.`
- there must be no extra content or blank lines

Example:

```text
X . O
. O .
. . X
```

## Valid game states

A board is valid only if it follows the game rules below:

- `X` starts and turns alternate
- the number of `X` cells is either equal to the number of `O` cells or exactly one more
- if counts are equal, it is `X`'s turn; if `X` has one extra, it is `O`'s turn
- a board in progress has no winner and at least one empty cell
- a finished winning board has exactly one winner
- an `X` win requires exactly one more `X` than `O`; an `O` win requires equal counts
- the winning state must be reachable through legal play that stops immediately on the first win
- a full board with no winner is a valid draw
- boards with both players winning or with inconsistent win counts are rejected

## Legal move rules

Before applying a move:

- confirm the previous board is valid and not already finished
- confirm the requested symbol is the player whose turn it is
- confirm the selected cell is empty

A valid move replaces exactly one `.` with the current player's symbol. Every other cell stays unchanged. The updated board must be written to `BOARD.txt` before any push or commit is considered complete.

## Acceptance checks

The acceptance rules are:

1. malformed layouts or invalid symbols are rejected
2. invalid move counts, both players winning, or inconsistent wins are rejected
3. a winning board that cannot arise from legal play is rejected
4. valid in-progress boards are accepted and the next turn is computed from the counts
5. valid winning boards are recognized as finished and no further move is accepted
6. full boards with no winner are recognized as draws and no further move is accepted
7. wrong-symbol or occupied-cell moves are rejected without changing the board
8. a valid move changes exactly one empty cell to the current player's symbol
9. every accepted move writes the updated board to `BOARD.txt` before any push

## How to play

1. pull the latest board state from the shared branch
2. edit exactly one `.` to your symbol
3. run `python3 scripts/check_move.py X` or `python3 scripts/check_move.py O`
4. verify the diff only shows the single legal move
5. stage, commit, and push the updated `BOARD.txt`

## Do not

- do not change the tests
- do not make a move after the board is already won or drawn
- do not overwrite an occupied square
- do not submit a board that violates the rules in `docs/PRD.md`
