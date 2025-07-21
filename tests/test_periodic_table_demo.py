from ai_minesweeper.board import State
from ai_minesweeper.board_builder import BoardBuilder


def test_periodic_table_integration():
    """
    Test that BoardBuilder.from_csv correctly parses the periodic table demo CSV
    and marks blank or unknown elements as mines.
    """
    # Simulate a CSV input for the periodic table
    csv_content = """H,He
Li,Be
Na, 
"""
    with open("elements.csv", "w") as f:
        f.write(csv_content)

    board = BoardBuilder.from_csv("elements.csv")

    # Assert that the board contains mines for blank or unknown elements
    assert board.grid[2][1].is_mine  # Blank cell
    assert board.grid[0][0].state == State.HIDDEN  # Valid element
    assert board.grid[0][1].state == State.HIDDEN  # Valid element
