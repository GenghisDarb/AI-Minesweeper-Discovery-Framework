from typer.testing import CliRunner
from src.ai_minesweeper.cli import app

runner = CliRunner()

def test_validate_command():
    result = runner.invoke(app, ["validate", "examples/boards/sample.csv"])
    assert result.exit_code == 0
    assert "The board is valid." in result.output

def test_play_command():
    result = runner.invoke(app, ["play", "examples/boards/sample.csv"])
    assert result.exit_code == 0
    assert "Game completed!" in result.output
