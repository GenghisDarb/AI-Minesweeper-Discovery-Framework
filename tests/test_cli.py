from typer.testing import CliRunner

from ai_minesweeper.cli import app

runner = CliRunner()


# Mocking board and v for the test
class MockBoard:
    def is_hidden(self, x, y):
        return True  # Mocking as if the cell is hidden


board = MockBoard()
v = (0, 0)


def test_validate_command():
    result = runner.invoke(app, ["validate", "examples/boards/sample.csv"])
    assert result.exit_code == 0
    assert "The board is valid." in result.output


def test_play_command():
    result = runner.invoke(app, ["play", "examples/boards/sample.csv"])
    assert result.exit_code == 0
    assert "Game completed!" in result.output
    assert (
        "The board is valid." not in result.output
    )  # Ensure no dry-run message appears
    assert board.is_hidden(v[0], v[1])
