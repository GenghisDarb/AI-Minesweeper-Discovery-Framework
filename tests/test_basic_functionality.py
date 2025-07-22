"""
Basic tests for AI Minesweeper core functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_minesweeper.board import Board, CellState
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.constraint_solver import ConstraintSolver


class TestBoard:
    """Test cases for Board class."""
    
    def test_board_initialization(self):
        """Test board initialization."""
        board = Board(9, 9, 10)
        assert board.width == 9
        assert board.height == 9
        assert board.mine_count == 10
        assert board.remaining_mines == 10
        assert len(board.get_hidden_cells()) == 81
        assert len(board.get_revealed_cells()) == 0
    
    def test_mine_placement(self):
        """Test mine placement."""
        board = Board(5, 5, 5)
        board.place_mines((2, 2))
        
        assert len(board.mines) == 5
        assert (2, 2) not in board.mines  # First click position avoided
    
    def test_cell_reveal(self):
        """Test cell revealing."""
        board = Board(3, 3, 1)
        board.mines = {(0, 0)}  # Manually place one mine
        
        # Reveal safe cell
        success = board.reveal_cell(2, 2)
        assert success
        assert board.cell_states[(2, 2)] == CellState.REVEALED
        
        # Reveal mine
        success = board.reveal_cell(0, 0)
        assert not success
    
    def test_cell_flagging(self):
        """Test cell flagging."""
        board = Board(3, 3, 1)
        
        # Flag cell
        board.flag_cell(1, 1)
        assert board.cell_states[(1, 1)] == CellState.FLAGGED
        assert board.remaining_mines == 0
        
        # Safe flag
        board.flag_cell(2, 2, safe_flag=True)
        assert board.cell_states[(2, 2)] == CellState.SAFE_FLAGGED
        assert (2, 2) in board.safe_flags
    
    def test_neighbor_calculation(self):
        """Test neighbor calculation."""
        board = Board(3, 3, 0)
        
        # Corner cell
        neighbors = board.get_neighbors(0, 0)
        assert len(neighbors) == 3
        assert (0, 1) in neighbors
        assert (1, 0) in neighbors
        assert (1, 1) in neighbors
        
        # Center cell
        neighbors = board.get_neighbors(1, 1)
        assert len(neighbors) == 8


class TestRiskAssessor:
    """Test cases for RiskAssessor class."""
    
    def test_risk_assessor_initialization(self):
        """Test risk assessor initialization."""
        assessor = RiskAssessor()
        assert assessor.chi_recursive_depth == 0
        assert len(assessor.risk_cache) == 0
    
    def test_risk_map_calculation(self):
        """Test risk map calculation."""
        board = Board(3, 3, 1)
        board.mines = {(0, 0)}
        board.reveal_cell(2, 2)  # Reveal safe cell
        
        assessor = RiskAssessor()
        risk_map = assessor.calculate_risk_map(board)
        
        # Check that risk map has coordinate keys
        assert isinstance(risk_map, dict)
        for pos, risk in risk_map.items():
            assert isinstance(pos, tuple)
            assert len(pos) == 2
            assert 0.0 <= risk <= 1.0
    
    def test_safest_cells(self):
        """Test safest cells identification."""
        board = Board(3, 3, 1)
        board.mines = {(0, 0)}
        board.reveal_cell(2, 2)
        
        assessor = RiskAssessor()
        safest = assessor.get_safest_cells(board, count=2)
        
        assert len(safest) <= 2
        assert all(isinstance(pos, tuple) for pos in safest)


class TestConstraintSolver:
    """Test cases for ConstraintSolver class."""
    
    def test_solver_initialization(self):
        """Test constraint solver initialization."""
        solver = ConstraintSolver()
        assert solver.solver_iterations == 0
        assert not solver.contradiction_detected
        assert len(solver.constraints) == 0
    
    def test_solve_step(self):
        """Test solver step execution."""
        board = Board(3, 3, 1)
        board.mines = {(0, 0)}
        board.place_mines((2, 2))  # This will be ignored since mines already set
        board.reveal_cell(2, 2)
        
        solver = ConstraintSolver()
        solution = solver.solve_step(board)
        
        assert "action" in solution
        assert solution["action"] in ["reveal", "flag", "none", "contradiction"]
        
        if solution["action"] in ["reveal", "flag"]:
            assert "position" in solution
            assert "confidence" in solution
    
    def test_solver_statistics(self):
        """Test solver statistics."""
        solver = ConstraintSolver()
        stats = solver.get_solver_statistics()
        
        assert isinstance(stats, dict)
        assert "solver_iterations" in stats
        assert "chi_cycle_progress" in stats
        assert "contradiction_detected" in stats


class TestIntegration:
    """Integration tests for combined functionality."""
    
    def test_complete_game_flow(self):
        """Test a complete game flow."""
        # Create small game
        board = Board(3, 3, 1)
        solver = ConstraintSolver()
        
        # Start game
        board.place_mines((1, 1))
        board.reveal_cell(1, 1)
        
        # Make several AI moves
        max_moves = 10
        for _ in range(max_moves):
            if board.is_solved():
                break
                
            solution = solver.solve_step(board)
            if solution["action"] == "none":
                break
            elif solution["action"] == "reveal":
                success = board.reveal_cell(*solution["position"])
                solver.update_outcome(solution["action"], solution["position"], success, board)
                if not success:  # Hit mine
                    break
            elif solution["action"] == "flag":
                board.flag_cell(*solution["position"])
                solver.update_outcome(solution["action"], solution["position"], True, board)
        
        # Verify game state is consistent
        assert len(board.get_hidden_cells()) + len(board.get_revealed_cells()) + len(board.get_flagged_cells()) == 9
    
    def test_confidence_tracking(self):
        """Test confidence tracking throughout game."""
        solver = ConstraintSolver()
        
        # Initial confidence
        initial_confidence = solver.confidence_tracker.get_confidence()
        assert 0.0 <= initial_confidence <= 1.0
        
        # Update with success
        solver.confidence_tracker.update_success("reveal", 1.0)
        success_confidence = solver.confidence_tracker.get_confidence()
        
        # Update with failure
        solver.confidence_tracker.update_failure("reveal", 1.0)
        failure_confidence = solver.confidence_tracker.get_confidence()
        
        # Verify confidence changes
        assert isinstance(success_confidence, float)
        assert isinstance(failure_confidence, float)


if __name__ == "__main__":
    pytest.main([__file__])