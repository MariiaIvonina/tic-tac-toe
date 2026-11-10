# AGENTS.md

Use `docs/PRD.md` as the source of truth for board validity and move acceptance. Treat it as the normative specification for this repository.

## Required rules

- `BOARD.txt` must contain exactly three rows and three columns.
- Rows must use single spaces between cells.
- Only `X`, `O`, and `.` are allowed in a cell.
- `X` starts first and turns alternate.
- The count of `X` cells must equal the count of `O` cells, or exceed it by exactly one.
- A board is invalid if both players have winning lines.
- A valid win must be reachable through legal play and must stop immediately on the first win.
- A full board without a winner is a valid draw.
- A finished board cannot accept another move.

## Move requirements

Before accepting a move:

- confirm the current board in `HEAD` is valid and unfinished
- confirm the symbol matches the player whose turn it is
- confirm the move is on an empty cell
- confirm exactly one cell changes from `.` to the active player's symbol
- confirm the resulting board is still valid
- write the updated board to `BOARD.txt` before any push is considered complete

## Working constraints

- Do not change any tests. The existing test suite defines the expected behavior.
- Do not relax or bypass the PRD rules.
- When modifying code or board state, match the acceptance checks in `docs/PRD.md` exactly.
- If the repo requires a board update, implement only the minimal change needed to make the board legal and valid.
