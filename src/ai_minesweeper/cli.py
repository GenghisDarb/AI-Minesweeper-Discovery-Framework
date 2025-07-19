import logging
import typer
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer(help="AI Minesweeper CLI – play or validate boards via the command line.")


@app.command()
def validate(csv_path: str = typer.Argument(..., help="Path to the board CSV file")):
    """Validate the integrity of a CSV board."""
    try:
        board = BoardBuilder.from_csv(csv_path)
        if board.is_valid():
            logger.info("The board is valid.")
        else:
            logger.warning("The board has inconsistencies.")
    except FileNotFoundError:
        logger.error(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        logger.exception(f"An error occurred during validation: {e}")


@app.command()
def play(csv_path: str = typer.Argument(..., help="Path to the board CSV file"),
         dry_run: bool = typer.Option(False, "--dry-run", help="Validate the board without playing through the moves.")):
    """Play Minesweeper using a CSV board."""
    try:
        # Pass header=0 to skip the header row in CSV files
        board = BoardBuilder.from_csv(csv_path, header=0)
        if dry_run:
            if board.is_valid():
                print("The board is valid.")  # Use print for test compatibility
                logger.info("The board is valid.")
            else:
                print("The board has inconsistencies.")  # Use print for test compatibility
                logger.warning("The board has inconsistencies.")
            return

        logger.info("Loaded board:")
        logger.info(board)

        solver = ConstraintSolver()
        while not board.is_solved():
            move = solver.choose_move(board)
            if move is None:
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

        logger.info("Game completed! All hypotheses resolved.")
        print("Game completed!")
    except FileNotFoundError:
        logger.error(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        logger.exception(f"An error occurred during gameplay: {e}")


if __name__ == "__main__":
    app()
