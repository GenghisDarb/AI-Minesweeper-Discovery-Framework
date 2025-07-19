import os
import sys
import subprocess


def test_cli_play_dry_run():
    # Use an example board CSV (copy to a tmp path to avoid any state issues)
    sample_board = "examples/boards/sample.csv"
    assert os.path.exists(sample_board), "Sample board CSV is missing"

    # Construct the command: python -m ai_minesweeper.cli play sample.csv --dry-run
    cmd = [
        sys.executable,
        "-m",
        "ai_minesweeper.cli",
        "play",
        sample_board,
        "--dry-run",
    ]

    # Ensure the src directory is in PYTHONPATH for the subprocess
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "src")

    # Run the CLI command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    # Combine stdout and stderr to catch all output
    output = result.stdout + result.stderr

    # The dry-run should report that the board is valid (or inconsistencies if any)
    assert "The board is valid." in output, (
        "Dry-run did not validate the board as expected"
    )
