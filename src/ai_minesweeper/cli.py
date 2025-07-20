import logging
import typer
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver
from ai_minesweeper.cell import State


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
<<<<<<< HEAD
        print(f"[DEBUG] About to load board from {csv_path}")
        board = BoardBuilder.from_csv(csv_path)
        print(f"[DEBUG] Board loaded, dry_run={dry_run}")
=======
        # Pass header=0 to skip the header row in CSV files
        board = BoardBuilder.from_csv(csv_path, header=0)
>>>>>>> origin/copilot/fix-73693070-4d50-40b0-97b0-72eeb69256fe
        if dry_run:
<<<<<<< HEAD
            if board.is_valid():
<<<<<<< HEAD
                message = "The board is valid."
            else:
                message = "The board has inconsistencies."
            logger.info(message)
            print(message)
=======
            print(f"[DEBUG] Running validation...")
            if board.is_valid():
                message = "The board is valid."
                logger.info(message)
                print(message)
            else:
                message = "The board has inconsistencies."
                logger.warning(message)
                print(message)
>>>>>>> origin/copilot/fix-66e80e14-9a03-42e2-940c-2e106230e889
=======
                print("The board is valid.")  # Use print for test compatibility
                logger.info("The board is valid.")
            else:
                print("The board has inconsistencies.")  # Use print for test compatibility
                logger.warning("The board has inconsistencies.")
>>>>>>> origin/copilot/fix-73693070-4d50-40b0-97b0-72eeb69256fe
            return

        solver = ConstraintSolver()
        while True:
            move = solver.choose_move(board)
            if move is None:
<<<<<<< HEAD
                break
            board.reveal(move.row, move.col)
=======
                logger.info("No more moves available")
                break
            # Handle both Cell objects and tuples for backwards compatibility
            if hasattr(move, 'row') and hasattr(move, 'col'):
                row, col = move.row, move.col
            else:
                row, col = move
            logger.info(f"Revealing cell at ({row}, {col})...")
            board.reveal(row, col)
            logger.info(board)
>>>>>>> origin/copilot/fix-73693070-4d50-40b0-97b0-72eeb69256fe

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
