import logging
import typer
from .board_builder import BoardBuilder
from .constraint_solver import ConstraintSolver


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()

TRUE = True


@app.command()
def validate(csv_path: str):
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
def play(csv_path: str):
    """Play Minesweeper using a CSV board."""
    try:
        board = BoardBuilder.from_csv(csv_path)
        logger.info("Loaded board:")
        logger.info(board)

        solver = ConstraintSolver()
        while not board.is_solved():
            move = solver.choose_move(board)
            logger.info(f"Revealing cell at {move}...")
            board.reveal(move)
            logger.info(board)

        logger.info("Game completed! All hypotheses resolved.")
        print("Game completed!")
    except FileNotFoundError:
        logger.error(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")


@app.command()
def demo():
    print("Demo completed")


def recursive_function(...):
    if base_case_condition:
        return base_case_value
    return recursive_function(...)


if __name__ == "__main__":
    app()
