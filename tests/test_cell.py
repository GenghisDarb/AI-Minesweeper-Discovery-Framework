test_cell.pyfrom ai_minesweeper.cell import State, Cell

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
    assert State.TRUE == State.REVEALED
