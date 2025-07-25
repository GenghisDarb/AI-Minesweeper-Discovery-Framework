from ai_minesweeper.board import Board, State


def test_neighbors_count():
    b = Board(3, 3)
    center = list(b.neighbors(1, 1))
    assert len(center) == 8
    corner = list(b.neighbors(0, 0))
    assert len(corner) == 3


def test_reveal():
    b = Board(2, 2)
    b.reveal(0, 0, True)
    assert b.grid[0][0].state == State.REVEALED
