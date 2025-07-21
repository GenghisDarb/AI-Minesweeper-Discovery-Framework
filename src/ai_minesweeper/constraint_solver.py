"""
Constraint Solver for AI Minesweeper with χ-recursive form and meta-cell confidence.

This module provides consolidated constraint solving logic with:
- Meta-cell confidence integration
- Robust contradiction handling
- χ-recursive decision optimization
- TORUS theory alignment for cyclical improvement
"""

import logging
from typing import Dict, List, Tuple, Set, Optional, Union
from itertools import combinations
import numpy as np

from .board import Board, CellState
from .risk_assessor import RiskAssessor
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
from .meta_cell_confidence.beta_confidence import BetaConfidence


class ConstraintSolver:
    """
    Consolidated constraint solver with meta-cell confidence and χ-recursive optimization.
    
    Features:
    - Integrated constraint satisfaction solving
    - Meta-cell confidence-based decision making
    - Robust contradiction detection and handling
    - χ-recursive optimization for complex scenarios
    - TORUS theory alignment for adaptive learning
    """
    
    def __init__(self):
        """Initialize the constraint solver."""
        self.risk_assessor = RiskAssessor()
        self.confidence_tracker = BetaConfidence()
        self.policy_wrapper = ConfidencePolicy(self.risk_assessor, self.confidence_tracker)
        
        # Solver state
        self.constraints: List[Dict] = []
        self.solution_cache: Dict[frozenset, Dict] = {}
        self.contradiction_detected = False
        
        # χ-recursive state
        self.solver_iterations = 0
        self.recursive_depth = 0
        self.chi_cycle_progress = 0
        
        self.logger = logging.getLogger(__name__)
        
    def solve_step(self, board: Board) -> Dict:
        """
        Perform one step of constraint solving with χ-recursive optimization.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary with recommended action and analysis
        """
        self.solver_iterations += 1
        self.recursive_depth = 0
        
        # Extract constraints from current board state
        self.constraints = self._extract_constraints(board)
        
        # Check for contradictions
        if self._detect_contradictions():
            self.contradiction_detected = True
            return {
                "action": "contradiction",
                "reason": "Board state contains contradictions",
                "confidence": 0.0
            }
        
        self.contradiction_detected = False
        
        # Try constraint satisfaction solving
        constraint_solution = self._solve_constraints(board)
        if constraint_solution["action"] != "none":
            return constraint_solution
        
        # Fall back to confidence-based policy
        policy_solution = self.policy_wrapper.get_recommended_action(board)
        
        # Apply χ-recursive optimization
        final_solution = self._apply_chi_recursive_optimization(
            constraint_solution, policy_solution, board
        )
        
        # Update χ-cycle progress
        self._update_chi_cycle(final_solution, board)
        
        return final_solution
    
    def _extract_constraints(self, board: Board) -> List[Dict]:
        """
        Extract minesweeper constraints from current board state.
        
        Args:
            board: Current board state
            
        Returns:
            List of constraint dictionaries
        """
        constraints = []
        
        for pos in board.get_revealed_cells():
            x, y = pos
            mine_count = board.revealed_numbers[pos]
            
            # Get hidden and flagged neighbors
            hidden_neighbors = []
            flagged_neighbors = 0
            
            for nx, ny in board.get_neighbors(x, y):
                if (nx, ny) in board.get_hidden_cells():
                    hidden_neighbors.append((nx, ny))
                elif board.cell_states[(nx, ny)] in [CellState.FLAGGED, CellState.SAFE_FLAGGED]:
                    flagged_neighbors += 1
            
            if hidden_neighbors:
                remaining_mines = mine_count - flagged_neighbors
                constraints.append({
                    "center": pos,
                    "hidden_neighbors": hidden_neighbors,
                    "remaining_mines": remaining_mines,
                    "satisfied": remaining_mines <= 0
                })
        
        self.logger.debug(f"Extracted {len(constraints)} constraints")
        return constraints
    
    def _detect_contradictions(self) -> bool:
        """
        Detect contradictions in current constraint set.
        
        Returns:
            True if contradictions detected
        """
        for constraint in self.constraints:
            remaining_mines = constraint["remaining_mines"]
            hidden_count = len(constraint["hidden_neighbors"])
            
            # Impossible constraints
            if remaining_mines < 0:
                self.logger.warning(f"Negative mines constraint at {constraint['center']}")
                return True
            
            if remaining_mines > hidden_count:
                self.logger.warning(f"Too many mines constraint at {constraint['center']}")
                return True
        
        # Check for conflicting constraints on same cells
        cell_constraints = {}
        for constraint in self.constraints:
            for cell in constraint["hidden_neighbors"]:
                if cell not in cell_constraints:
                    cell_constraints[cell] = []
                cell_constraints[cell].append(constraint)
        
        # Advanced contradiction detection would go here
        # For now, basic checks are sufficient
        
        return False
    
    def _solve_constraints(self, board: Board) -> Dict:
        """
        Solve constraints using logical deduction.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary with solution or "none" action
        """
        # Check cache first
        cache_key = self._create_constraint_cache_key()
        if cache_key in self.solution_cache:
            return self.solution_cache[cache_key]
        
        solution = {"action": "none"}
        
        # Simple constraint solving - exact matches
        for constraint in self.constraints:
            if constraint["satisfied"]:
                continue
                
            remaining_mines = constraint["remaining_mines"]
            hidden_neighbors = constraint["hidden_neighbors"]
            
            # All remaining cells are mines
            if remaining_mines == len(hidden_neighbors) and remaining_mines > 0:
                pos = hidden_neighbors[0]
                solution = {
                    "action": "flag",
                    "position": pos,
                    "confidence": 0.95,
                    "reason": f"Constraint satisfaction - all remaining cells are mines"
                }
                break
            
            # No more mines in this constraint
            if remaining_mines == 0:
                pos = hidden_neighbors[0]
                solution = {
                    "action": "reveal",
                    "position": pos,
                    "confidence": 0.95,
                    "reason": f"Constraint satisfaction - no mines remaining"
                }
                break
        
        # Advanced constraint solving with overlapping constraints
        if solution["action"] == "none":
            solution = self._solve_overlapping_constraints(board)
        
        # Cache the result
        self.solution_cache[cache_key] = solution
        
        return solution
    
    def _solve_overlapping_constraints(self, board: Board) -> Dict:
        """
        Solve overlapping constraints using advanced techniques.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary with solution or "none" action
        """
        self.recursive_depth += 1
        
        # Limit recursion for χ-recursive stability
        if self.recursive_depth > 5:
            self.recursive_depth -= 1
            return {"action": "none"}
        
        # Find overlapping constraint groups
        overlap_groups = self._find_constraint_overlaps()
        
        for group in overlap_groups:
            # Try to solve each group
            group_solution = self._solve_constraint_group(group, board)
            if group_solution["action"] != "none":
                self.recursive_depth -= 1
                return group_solution
        
        self.recursive_depth -= 1
        return {"action": "none"}
    
    def _find_constraint_overlaps(self) -> List[List[Dict]]:
        """
        Find groups of overlapping constraints.
        
        Returns:
            List of constraint groups that overlap
        """
        groups = []
        processed = set()
        
        for i, constraint in enumerate(self.constraints):
            if i in processed:
                continue
                
            group = [constraint]
            group_cells = set(constraint["hidden_neighbors"])
            processed.add(i)
            
            # Find overlapping constraints
            for j, other_constraint in enumerate(self.constraints):
                if j <= i or j in processed:
                    continue
                    
                other_cells = set(other_constraint["hidden_neighbors"])
                if group_cells & other_cells:  # Intersection exists
                    group.append(other_constraint)
                    group_cells.update(other_cells)
                    processed.add(j)
            
            if len(group) > 1:
                groups.append(group)
        
        return groups
    
    def _solve_constraint_group(self, group: List[Dict], board: Board) -> Dict:
        """
        Solve a group of overlapping constraints.
        
        Args:
            group: List of overlapping constraints
            board: Current board state
            
        Returns:
            Dictionary with solution or "none" action
        """
        # Collect all cells involved in this group
        all_cells = set()
        for constraint in group:
            all_cells.update(constraint["hidden_neighbors"])
        
        all_cells = list(all_cells)
        
        # Try different mine distributions
        total_remaining_mines = sum(c["remaining_mines"] for c in group)
        
        # Simple case: if total mines equals total cells
        if total_remaining_mines == len(all_cells):
            return {
                "action": "flag",
                "position": all_cells[0],
                "confidence": 0.9,
                "reason": "Overlapping constraints - all cells are mines"
            }
        
        if total_remaining_mines == 0:
            return {
                "action": "reveal",
                "position": all_cells[0],
                "confidence": 0.9,
                "reason": "Overlapping constraints - no mines in group"
            }
        
        # More complex solving would require constraint satisfaction algorithms
        # For now, return no solution for complex cases
        return {"action": "none"}
    
    def _apply_chi_recursive_optimization(
        self,
        constraint_solution: Dict,
        policy_solution: Dict,
        board: Board
    ) -> Dict:
        """
        Apply χ-recursive optimization to combine solutions.
        
        Args:
            constraint_solution: Solution from constraint solving
            policy_solution: Solution from confidence policy
            board: Current board state
            
        Returns:
            Optimized final solution
        """
        # Prefer constraint solution if available and high confidence
        if (constraint_solution["action"] != "none" and 
            constraint_solution.get("confidence", 0) > 0.8):
            return constraint_solution
        
        # Use policy solution with χ-recursive enhancement
        if policy_solution["action"] != "none":
            enhanced_solution = policy_solution.copy()
            
            # Apply χ-recursive confidence boost based on solver history
            confidence_boost = self._calculate_chi_recursive_boost(board)
            original_confidence = enhanced_solution.get("confidence", 0.5)
            enhanced_solution["confidence"] = min(0.95, original_confidence * confidence_boost)
            
            return enhanced_solution
        
        return {"action": "none", "reason": "No viable solution found"}
    
    def _calculate_chi_recursive_boost(self, board: Board) -> float:
        """
        Calculate χ-recursive confidence boost based on solver performance.
        
        Args:
            board: Current board state
            
        Returns:
            Confidence boost factor
        """
        # Base boost
        boost = 1.0
        
        # Boost based on recent success pattern
        if len(board.confidence_history) >= 5:
            recent_avg = sum(board.confidence_history[-5:]) / 5
            if recent_avg > 0.7:
                boost *= 1.1  # Recent success
            elif recent_avg < 0.4:
                boost *= 0.9  # Recent struggles
        
        # χ-cycle based adjustment
        cycle_phase = (self.chi_cycle_progress % 20) / 20.0
        cycle_boost = 0.95 + 0.1 * np.sin(2 * np.pi * cycle_phase)
        boost *= cycle_boost
        
        return boost
    
    def _update_chi_cycle(self, solution: Dict, board: Board) -> None:
        """
        Update χ-cycle progress based on solution quality.
        
        Args:
            solution: Current solution
            board: Current board state
        """
        self.chi_cycle_progress += 1
        
        # Update board's χ-cycle tracking
        confidence = solution.get("confidence", 0.5)
        board.update_chi_cycle(confidence)
    
    def _create_constraint_cache_key(self) -> frozenset:
        """Create cache key for current constraint set."""
        key_items = []
        for constraint in self.constraints:
            center = constraint["center"]
            neighbors = tuple(sorted(constraint["hidden_neighbors"]))
            mines = constraint["remaining_mines"]
            key_items.append((center, neighbors, mines))
        
        return frozenset(key_items)
    
    def update_outcome(
        self, 
        action: str, 
        position: Tuple[int, int], 
        success: bool,
        board: Board
    ) -> None:
        """
        Update solver based on action outcome.
        
        Args:
            action: Action taken
            position: Position of action
            success: Whether action was successful
            board: Updated board state
        """
        # Update confidence tracker
        outcome_quality = 1.0 if success else 0.0
        self.policy_wrapper.update_policy_outcome(action, position, success, outcome_quality)
        
        # Clear cache on state change
        self.solution_cache.clear()
        self.risk_assessor.clear_cache()
        
        self.logger.debug(f"Solver outcome updated: {action} at {position}, success={success}")
    
    def get_solver_statistics(self) -> Dict:
        """
        Get comprehensive solver statistics.
        
        Returns:
            Dictionary with solver performance statistics
        """
        policy_stats = self.policy_wrapper.get_policy_statistics()
        risk_stats = self.risk_assessor.get_risk_statistics(None) if hasattr(self, '_last_board') else {}
        
        return {
            "solver_iterations": self.solver_iterations,
            "current_recursive_depth": self.recursive_depth,
            "chi_cycle_progress": self.chi_cycle_progress,
            "contradiction_detected": self.contradiction_detected,
            "active_constraints": len(self.constraints),
            "cache_size": len(self.solution_cache),
            "policy_stats": policy_stats,
            "risk_stats": risk_stats
        }
    
    def reset_solver(self) -> None:
        """Reset solver to initial state."""
        self.constraints.clear()
        self.solution_cache.clear()
        self.contradiction_detected = False
        self.solver_iterations = 0
        self.recursive_depth = 0
        self.chi_cycle_progress = 0
        
        # Reset sub-components
        self.risk_assessor.clear_cache()
        self.confidence_tracker.reset_confidence()
        
        self.logger.info("Constraint solver reset to initial state")
