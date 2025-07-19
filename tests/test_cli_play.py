import os
import sys
from typer.testing import CliRunner
from ai_minesweeper.cli import app


def test_cli_play_dry_run():
    # Use an example board CSV
    sample_board = "examples/boards/sample.csv"
    assert os.path.exists(sample_board), "Sample board CSV is missing"

    # Use the CliRunner for more reliable testing
    runner = CliRunner()
    result = runner.invoke(app, ["play", sample_board, "--dry-run"])

    # The dry-run should report that the board is valid (or inconsistencies if any)
    assert "The board is valid." in result.output, (
        "Dry-run did not validate the board as expected"
    )
