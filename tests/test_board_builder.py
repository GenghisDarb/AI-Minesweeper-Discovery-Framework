import tempfile

from ai_minesweeper.board import Board
from ai_minesweeper.board_builder import BoardBuilder


def test_from_csv():
    # Mock CSV input
    csv_data = "1,0,0\n0,1,0\n0,0,1"
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as temp_csv:
        temp_csv.write(csv_data)
        temp_csv.close()
        board = BoardBuilder.from_csv(temp_csv.name, header=False)
    assert board.n_rows == 3
    assert board.n_cols == 3
    assert sum(cell.is_mine for row in board.grid for cell in row) == 0


def test_from_relations():
    # Mock relations input
    relations = [(0, 1), (1, 2)]
    board = BoardBuilder.from_relations(relations)
    assert isinstance(board, Board)
    assert len(board.grid) > 0


def test_from_text():
    # Mock text input
    text_data = "HIDDEN HIDDEN\nHIDDEN MINE"
    board = BoardBuilder.from_text(text_data)
    assert isinstance(board, Board)
    assert len(board.grid) == 2


def test_from_pdf():
    # Mock PDF input
    pdf_bytes = (
        b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n"
        b"<< /Root 1 0 R >>\nstartxref\n0\n%%EOF"
    )
    with tempfile.NamedTemporaryFile(
        delete=False, mode="wb", suffix=".pdf"
    ) as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf.close()
        board = BoardBuilder.from_pdf(temp_pdf.name)
    assert isinstance(board, Board)


def test_random_board():
    board = BoardBuilder.random_board(5, 5, 10)
    assert isinstance(board, Board)
    assert len(board.grid) == 5
    assert sum(cell.is_mine for row in board.grid for cell in row) == 10


def test_fixed_board():
    layout = [[0, 1], [1, 0]]
    mines = [(0, 1), (1, 0)]
    board = BoardBuilder.fixed_board(layout, mines)
    assert isinstance(board, Board)
    assert len(board.grid) == 2
    assert board.grid[0][1].is_mine
    assert board.grid[1][0].is_mine
