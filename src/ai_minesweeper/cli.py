"""
Command-line interface for AI Minesweeper with χ-recursive capabilities.

This module provides a CLI interface with:
- Meta-cell mode support
- Board validation and game simulation
"""

import logging
import time
import typer
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver
from ai_minesweeper.board import CellState

app = typer.Typer()

# Configure logging
logging.basicConfig(level=logging.INFO)

class MinesweeperCLI:
    def __init__(self, width: int, height: int, mines: int, meta_mode: bool = False):
        """
        Initialize the Minesweeper CLI with board dimensions and mine count.
        
        Args:
            width: Board width
            height: Board height
            mines: Number of mines
            meta_mode: Enable meta-cell confidence mode
        """
        self.width = width
        self.height = height
        self.mines = mines
        self.meta_mode = meta_mode
        
        self.board = None
        self.solver = None
        self.game_started = False
        self.start_time = None
        self.moves_made = 0
        
        self._initialize_game()
    
    def _initialize_game(self) -> None:
        """Initialize the game board and solver."""
        self.board = BoardBuilder().build(self.width, self.height, self.mines)
        self.solver = ConstraintSolver(self.board)
    
    def start_game(self, first_click: tuple[int, int] = None) -> bool:
        """
        Start the game with optional first click.
        
        Args:
            first_click: Optional first click coordinates
        """
        if not first_click:
            # Auto-select first click (center or random)
            first_click = (self.board.width // 2, self.board.height // 2)
        
        self.board.place_mines(first_click)
        success = self.board.reveal_cell(*first_click)
        
        if not success:
            typer.echo("ERROR: Hit mine on first click! This shouldn't happen.")
            return False
        
        self.game_started = True
        self.start_time = time.time()
        self.moves_made = 1
        
        logging.info(f"Game started with first click at {first_click}")
        return True
    
    def play_interactive(self) -> None:
        """Play in interactive mode with user input."""
        print("AI Minesweeper - Interactive Mode")
        print("Commands: 'auto' for AI move, 'solve' for full auto-solve, 'quit' to exit")
        print("Manual moves: 'r x y' to reveal, 'f x y' to flag")
        
        if not self.game_started:
            self.start_game()
        
        while True:
            self.display_board()
            
            if self.board.is_solved():
                self._display_victory()
                break
            
            print(f"\nMove {self.moves_made + 1}:")
            if self.meta_mode:
                self._display_solver_status()
            
            command = input("Enter command: ").strip().lower()
            
            if command == "quit":
                break
            elif command == "auto":
                self._make_ai_move()
            elif command == "solve":
                self._auto_solve()
                break
            elif command.startswith("r "):
                self._handle_manual_reveal(command)
            elif command.startswith("f "):
                self._handle_manual_flag(command)
            else:
                print("Invalid command. Use 'auto', 'solve', 'r x y', 'f x y', or 'quit'")
    
    def auto_solve(self) -> bool:
        """
        Automatically solve the entire game.
        
        Returns:
            True if solved successfully
        """
        if not self.game_started:
            self.start_game()
        
        print("Auto-solving with AI...")
        self._auto_solve()
        
        return self.board.is_solved()
    
    def _auto_solve(self) -> None:
        """Internal auto-solve implementation."""
        max_moves = self.board.width * self.board.height
        
        for move_num in range(max_moves):
            if self.board.is_solved():
                self._display_victory()
                break
            
            print(f"\nMove {self.moves_made + 1}:")
            if self.meta_mode:
                self.display_board()
                self._display_solver_status()
            
            success = self._make_ai_move()
            if not success:
                break
            
            if self.meta_mode:
                time.sleep(0.5)  # Pause for visualization
        
        if not self.board.is_solved():
            print("Auto-solve failed to complete the game.")
    
    def _make_ai_move(self) -> bool:
        """
        Make one AI move using the constraint solver.
        
        Returns:
            True if move was successful
        """
        solution = self.solver.solve_step(self.board)
        
        if solution["action"] == "none":
            print("AI: No valid moves found.")
            return False
        
        if solution["action"] == "contradiction":
            print("AI: Contradiction detected in board state!")
            return False
        
        action = solution["action"]
        position = solution["position"]
        confidence = solution.get("confidence", 0.5)
        reason = solution.get("reason", "No reason provided")
        
        print(f"AI {action}s at {position} (confidence: {confidence:.3f})")
        print(f"Reason: {reason}")
        
        # Execute the move
        success = True
        if action == "reveal":
            success = self.board.reveal_cell(*position)
            if not success:
                print("💥 MINE HIT! Game Over.")
                self._display_game_over()
                return False
        elif action == "flag":
            safe_flag = self.meta_mode and confidence < 0.9
            self.board.flag_cell(*position, safe_flag=safe_flag)
        
        # Update solver with outcome
        self.solver.update_outcome(action, position, success, self.board)
        self.moves_made += 1
        
        return True
    
    def _handle_manual_reveal(self, command: str) -> None:
        """Handle manual reveal command."""
        try:
            parts = command.split()
            x, y = int(parts[1]), int(parts[2])
            
            if not (0 <= x < self.board.width and 0 <= y < self.board.height):
                print("Invalid coordinates.")
                return
            
            success = self.board.reveal_cell(x, y)
            self.moves_made += 1
            
            if not success:
                print("💥 MINE HIT! Game Over.")
                self._display_game_over()
            
        except (ValueError, IndexError):
            print("Invalid format. Use 'r x y'")
    
    def _handle_manual_flag(self, command: str) -> None:
        """Handle manual flag command."""
        try:
            parts = command.split()
            x, y = int(parts[1]), int(parts[2])
            
            if not (0 <= x < self.board.width and 0 <= y < self.board.height):
                print("Invalid coordinates.")
                return
            
            self.board.flag_cell(x, y)
            self.moves_made += 1
            
        except (ValueError, IndexError):
            print("Invalid format. Use 'f x y'")
    
    def _display_solver_status(self) -> None:
        """Display current solver status in meta-cell mode."""
        if not self.meta_mode:
            return
        
        stats = self.solver.get_solver_statistics()
        confidence_stats = stats.get("policy_stats", {}).get("confidence_stats", {})
        
        print(f"χ-Cycle Progress: {stats.get('chi_cycle_progress', 0)}")
        print(f"Solver Iterations: {stats.get('solver_iterations', 0)}")
        print(f"Active Constraints: {stats.get('active_constraints', 0)}")
        
        if confidence_stats:
            print(f"Confidence Trend: {confidence_stats.get('confidence_trend', 0):.3f}")
            print(f"Total Decisions: {confidence_stats.get('total_decisions', 0)}")
    
    def _display_victory(self) -> None:
        """Display victory message with statistics."""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        
        print("\n🎉 VICTORY! Board solved successfully! 🎉")
        print(f"Moves made: {self.moves_made}")
        print(f"Time elapsed: {elapsed_time:.1f} seconds")
        
        if self.meta_mode:
            stats = self.solver.get_solver_statistics()
            print(f"Final confidence: {self.solver.confidence_tracker.get_confidence():.3f}")
            print(f"χ-Cycle iterations: {stats.get('chi_cycle_progress', 0)}")
        
        self.display_board()
    
    def _display_game_over(self) -> None:
        """Display game over message."""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        
        print("\n💥 GAME OVER 💥")
        print(f"Moves made: {self.moves_made}")
        print(f"Time elapsed: {elapsed_time:.1f} seconds")
        
        # Reveal all mines
        for mine_pos in self.board.mines:
            self.board.cell_states[mine_pos] = CellState.REVEALED
        
        self.display_board()


@app.command()
def cli(width: int = 9, height: int = 9, mines: int = 10, meta: bool = False, auto: bool = False, interactive: bool = True):
    """
    AI Minesweeper with χ-recursive form and TORUS theory integration.
    
    Example usage:
    
    Basic game: ai-minesweeper
    
    Custom board: ai-minesweeper -w 16 -h 16 -m 40
    
    Meta-cell mode: ai-minesweeper --meta
    
    Auto-solve: ai-minesweeper --auto
    """
    # Validate inputs
    if width < 1 or height < 1:
        typer.echo("Error: Width and height must be positive integers")
        return
    
    if mines < 0 or mines >= width * height:
        typer.echo("Error: Invalid number of mines")
        return
    
    # Create CLI interface
    cli = MinesweeperCLI(width, height, mines, meta_mode=meta)
    
    typer.echo(f"AI Minesweeper - χ-Recursive Form v1.1.0")
    typer.echo(f"Board: {width}x{height}, Mines: {mines}")
    if meta:
        typer.echo("Meta-cell confidence mode enabled")
    
    try:
        if auto:
            # Auto-solve mode
            success = cli.auto_solve()
            if success:
                typer.echo("✅ Auto-solve completed successfully!")
            else:
                typer.echo("❌ Auto-solve failed")
        else:
            # Interactive mode (default)
            cli.play_interactive()
    
    except KeyboardInterrupt:
        typer.echo("\n\nGame interrupted by user.")
    except Exception as e:
        typer.echo(f"\nError: {e}")
        if meta:
            # Show debug info in meta mode
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app()
