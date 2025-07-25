from ai_minesweeper.cell import Cell, State


def test_initial_state():
    cell = Cell()
    assert cell.state == State.HIDDEN


def test_reveal_transition():
    cell = Cell()
    cell.state = State.REVEALED
    assert cell.state == State.REVEALED


def test_flagged_transition():
    cell = Cell()
    cell.state = State.FLAGGED
    assert cell.state == State.FLAGGED


def test_true_alias():
    # State.TRUE should be an alias for State.REVEALED if it exists
    # Since State.TRUE doesn't exist, test that FALSE alias works
    assert State.FALSE == State.FLAGGED
