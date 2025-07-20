from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.cell import State


def test_choose_move_returns_valid_hidden_cell():
    board = BoardBuilder.from_csv("tests/data/test_grid.csv")
    move = RiskAssessor().choose_move(board)
    assert move is not None
    r, c = move
    cell = board.grid[r][c]
    assert cell.is_hidden()


def test_estimate_risk_map_structure():
    board = BoardBuilder.random_board(rows=4, cols=4, mines=2)
    risk_map = RiskAssessor.estimate(board)

    assert isinstance(risk_map, dict)
    assert all(isinstance(key, tuple) and len(key) == 2 for key in risk_map.keys())
    assert all(isinstance(value, float) for value in risk_map.values())


def test_estimate_risk_map_variance():
    board = BoardBuilder.random_board(rows=4, cols=4, mines=2)
    risk_map = RiskAssessor.estimate(board)

    assert len(set(risk_map.values())) > 1, "Risk map should have variance in probabilities"


def test_estimate_empty_board():
    board = BoardBuilder.empty_board(rows=4, cols=4)
    risk_map = RiskAssessor.estimate(board)

    assert len(risk_map) == 0, "Risk map should be empty for an empty board"


def test_estimate_fully_revealed_board():
    board = BoardBuilder.random_board(rows=4, cols=4, mines=2)
    for row in board.grid:
        for cell in row:
            cell.state = State.REVEALED

    risk_map = RiskAssessor.estimate(board)
    assert len(risk_map) == 0, "Risk map should be empty for a fully revealed board"
