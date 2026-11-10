# Tic-Tac-Toe Board Update Requirements

## Purpose

Define which `BOARD.txt` states are valid and how a move must be applied before
the updated board is pushed.

## Board format

`BOARD.txt` must contain exactly three rows of three cells. Cells are separated
by single spaces, and the file must contain no extra content. A cell may contain
only `X`, `O`, or `.` (`.` represents an empty cell).

## Valid board states

- X starts, and turns alternate.
- The number of X cells must equal the number of O cells, or exceed it by
  exactly one.
- Equal counts mean X is next; one extra X means O is next.
- An in-progress board has no winner and at least one empty cell.
- A finished winning board has exactly one winner. An X win requires one more X
  than O; an O win requires equal counts.
- A winning board must be reachable through legal play that stopped immediately
  when the first win occurred. No moves may follow a win.
- A full board with no winner is a valid draw.
- Reject boards that do not meet these rules, including boards where both
  players have winning lines.

## Move and board update

Before making a move:

- Confirm the board is valid and is not already finished (won or drawn).
- Confirm the requested symbol is the player whose turn it is.
- Confirm the selected cell is empty.

For an accepted move, replace exactly the selected `.` with the requested
symbol. Leave every other cell unchanged. Write the updated board to
`BOARD.txt` before pushing.

## Acceptance checks

1. A board with a malformed layout or a cell outside `X`, `O`, and `.` is
   rejected.
2. A board with invalid move counts, both players winning, or a win inconsistent
   with the last move is rejected.
3. A winning board that cannot result from legal play stopping at the first win
   is rejected.
4. An in-progress board with valid counts, no winner, and an empty cell is
   accepted; the next player is computed from the counts.
5. A valid winning board is recognized as finished, and no move is accepted on
   it.
6. A full board with no winner is recognized as a draw, and no move is accepted
   on it.
7. A move requested with the wrong symbol or on a non-empty cell is rejected
   without changing the board.
8. A valid move changes only the selected empty cell to the current player's
   symbol.
9. After an accepted move, the updated board is written to `BOARD.txt` before
   any push.
