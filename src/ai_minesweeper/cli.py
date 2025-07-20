import logging
import typer
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="AI Minesweeper CLI – play or validate boards via the command line."
)


@app.command()
def validate(csv_path: str = typer.Argument(..., help="Path to the board CSV file")):
    """Validate the integrity of a CSV board."""
    try:
        board = BoardBuilder.from_csv(csv_path)
        if board.is_valid():
            message = "The board is valid."
            logger.info(message)
            print(message)
        else:
            message = "The board has inconsistencies."
            logger.warning(message)
            print(message)
    except FileNotFoundError:
        message = f"Error: File '{csv_path}' not found."
        logger.error(message)
        print(message)
    except Exception as e:
        message = f"An error occurred during validation: {e}"
        logger.exception(message)
        print(message)


@app.command()
def play(
    csv_path: str = typer.Argument(..., help="Path to the board CSV file"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Validate the board without playing through the moves."
    ),
):
    """Play Minesweeper using a CSV board."""
    print(f"[DEBUG] Starting play command with csv_path={csv_path}, dry_run={dry_run}")
    try:
        print(f"[DEBUG] About to load board from {csv_path}")
        board = BoardBuilder.from_csv(csv_path)
        print(f"[DEBUG] Board loaded, dry_run={dry_run}")
        if dry_run:
            if board.is_valid():
                message = "The board is valid."
            else:
                message = "The board has inconsistencies."
            logger.info(message)
            print(message)
        else:
            solver = ConstraintSolver()
            while True:
                move = solver.choose_move(board)
                if move is None:
                    break
                if isinstance(move, tuple):
                    row, col = move
                else:
                    row, col = move.row, move.col
                board.reveal(row, col)

        message = "Game completed! All hypotheses resolved."
        logger.info(message)
        print(message)
    except FileNotFoundError:
        message = f"Error: File '{csv_path}' not found."
        logger.error(message)
        print(message)
    except Exception as e:
        message = f"An error occurred during gameplay: {e}"
        logger.exception(message)
        print(message)
