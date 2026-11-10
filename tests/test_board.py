import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_move import main, parse_board


def board(*rows: str) -> str:
    return "\n".join(rows) + "\n"


def run_check(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    previous: str,
    current: str,
    symbol: str,
) -> int:
    board_path = tmp_path / "BOARD.txt"
    board_path.write_text(current)
    monkeypatch.setattr("scripts.check_move.BOARD_PATH", board_path)
    monkeypatch.setattr(
        "scripts.check_move.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, stdout=previous, stderr=""
        ),
    )
    monkeypatch.setattr(sys, "argv", ["check_move.py", symbol])
    return main()


def test_parse_board_accepts_three_rows_of_three_cells() -> None:
    assert parse_board(board(". X O", "O . X", "X O ."), "board") == [
        ".",
        "X",
        "O",
        "O",
        ".",
        "X",
        "X",
        "O",
        ".",
    ]


@pytest.mark.parametrize(
    "contents",
    [
        ". .\n. . .\n. . .\n",
        ". . .\n. . .\n",
        ". . .\n. . .\n. . .\n\n",
        ".  . .\n. . .\n. . .\n",
        ".\t. .\n. . .\n. . .\n",
        ". . .\n. . .\n. . Z\n",
        ". . .\n. . .\n. . x\n",
    ],
)
def test_parse_board_rejects_malformed_layout_or_cells(contents: str) -> None:
    with pytest.raises(ValueError):
        parse_board(contents, "board")


def test_accepts_a_legal_move_by_x(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    result = run_check(
        monkeypatch, tmp_path, board(". . .", ". . .", ". . ."),
        board("X . .", ". . .", ". . ."), "X"
    )

    assert result == 0
    assert "Valid move" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("previous", "current", "symbol"),
    [
        (board(". . .", ". . .", ". . ."), board("O . .", ". . .", ". . ."), "O"),
        (board("O . .", ". . .", ". . ."), board("O X .", ". . .", ". . ."), "X"),
        (board("X X .", ". . .", ". . ."), board("X X O", ". . .", ". . ."), "O"),
    ],
)
def test_rejects_wrong_turn_or_invalid_move_counts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    previous: str,
    current: str,
    symbol: str,
) -> None:
    assert run_check(monkeypatch, tmp_path, previous, current, symbol) != 0


@pytest.mark.parametrize(
    ("previous", "current", "symbol"),
    [
        (" . .\n. . .\n. . .\n", board(". X .", ". . .", ". . ."), "X"),
        (board(". . .", ". . .", ". . ."), ".  X .\n. . .\n. . .\n", "X"),
        (board(". . .", ". . .", ". . ."), board(". . .", ". . .", ". . Z"), "X"),
    ],
)
def test_rejects_malformed_previous_or_updated_board(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    previous: str,
    current: str,
    symbol: str,
) -> None:
    assert run_check(monkeypatch, tmp_path, previous, current, symbol) != 0


def test_rejects_move_when_previous_board_has_a_winner(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X X X", "O O .", ". . .")
    current = board("X X X", "O O O", ". . .")

    assert run_check(monkeypatch, tmp_path, previous, current, "O") != 0


def test_rejects_a_board_where_both_players_have_winning_lines(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X X X", "O O O", ". . .")
    current = board("X X X", "O O O", "X . .")

    assert run_check(monkeypatch, tmp_path, previous, current, "X") != 0


def test_accepts_a_legal_winning_move(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X X .", "O O .", ". . .")
    current = board("X X X", "O O .", ". . .")

    assert run_check(monkeypatch, tmp_path, previous, current, "X") == 0


def test_accepts_a_legal_draw_move(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X O X", "X O O", "O X .")
    current = board("X O X", "X O O", "O X X")

    assert run_check(monkeypatch, tmp_path, previous, current, "X") == 0


def test_rejects_a_move_after_the_game_is_already_won(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X X X", "O O .", ". . .")
    current = board("X X X", "O O O", ". . .")

    assert run_check(monkeypatch, tmp_path, previous, current, "O") != 0


def test_rejects_a_move_after_a_full_draw(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X O X", "X O O", "O X X")
    current = board("X O X", "X O O", "O X X")

    assert run_check(monkeypatch, tmp_path, previous, current, "O") != 0


@pytest.mark.parametrize(
    ("current", "symbol"),
    [
        (board("X X .", ". . .", ". . ."), "X"),
        (board("X . .", ". O .", ". . ."), "O"),
    ],
)
def test_rejects_changes_to_more_than_one_cell(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    current: str,
    symbol: str,
) -> None:
    assert run_check(
        monkeypatch, tmp_path, board(". . .", ". . .", ". . ."), current, symbol
    ) != 0


def test_rejects_a_move_that_overwrites_an_occupied_cell(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    previous = board("X . .", ". . .", ". . .")
    current = board("O . .", ". . .", ". . .")

    assert run_check(monkeypatch, tmp_path, previous, current, "O") != 0
