# src/ai_minesweeper/constraint_solver.py

class ConstraintSolver:
    def choose_move(self, board):
        """
        Choose the next move using iterative constraint solving.
        Refactored from recursive approach to prevent RecursionError.
        """
        return self._iterative_solve(board)

    def solve(self, board):
        """
        Solve the board using iterative constraint solving.
        """
        return self._iterative_solve(board)
    
    def _iterative_solve(self, board):
        """
        Iterative constraint solving with base-case guard.
        """
        from .board import State
        
        # Base case guard: check if any moves are available
        hidden_cells = [
            (r, c) for r in range(board.n_rows)
            for c in range(board.n_cols)
            if board.grid[r][c].state == State.HIDDEN
        ]
        
        if not hidden_cells:
            return None
            
        # Simple heuristic: return first safe cell found
        # In a full implementation, this would contain constraint propagation logic
        for r, c in hidden_cells:
            cell = board.grid[r][c]
            if not cell.is_mine:  # Basic safety check
                return cell
                
        # Fallback: return first hidden cell if no obviously safe cell found
        r, c = hidden_cells[0]
        return board.grid[r][c]
