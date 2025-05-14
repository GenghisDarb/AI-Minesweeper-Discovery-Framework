import csv
import os

def load_csv_board(path):
    with open(path, newline="") as f:
        return [row for row in csv.reader(f)]

def test_mini_csv_dimensions():
    board_path = os.path.join("examples", "boards", "mini.csv")
    grid = load_csv_board(board_path)
    assert len(grid) == 5
    assert all(len(row) == 3 for row in grid)
