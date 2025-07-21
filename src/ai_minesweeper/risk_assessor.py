"""
Risk Assessment module for AI Minesweeper with χ-recursive form.

This module provides risk analysis capabilities with:
- Risk maps with coordinate keys for test consistency
- Dynamic risk calculation based on board state
- Integration with TORUS theory for χ-recursive feedback
- Removal of duplicate logic for clean implementation
"""

import logging
from typing import Dict, Tuple, Set, List, Optional
import numpy as np
from .board import Board, CellState


class RiskAssessor:
    """
    Risk assessment engine for minesweeper AI with χ-recursive capabilities.
    
    Features:
    - Returns risk maps with coordinate keys for test consistency
    - Dynamic risk calculation based on revealed information
    - Integration with χ-recursive decision making
    - TORUS theory alignment for confidence feedback
    """
    
    def __init__(self):
        """Initialize the risk assessor."""
        self.logger = logging.getLogger(__name__)
        self.risk_cache: Dict[frozenset, Dict[Tuple[int, int], float]] = {}
        self.chi_recursive_depth = 0
        
    def calculate_risk_map(self, board: Board) -> Dict[Tuple[int, int], float]:
        """
        Calculate risk map with coordinate keys for all hidden cells.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary mapping coordinates to risk values [0.0, 1.0]
        """
        risk_map = {}
        hidden_cells = board.get_hidden_cells()
        revealed_cells = board.get_revealed_cells()
        
        if not hidden_cells:
            return risk_map
            
        # Create cache key from board state
        cache_key = self._create_cache_key(board)
        if cache_key in self.risk_cache:
            self.logger.debug("Using cached risk calculation")
            return self.risk_cache[cache_key]
        
        # Calculate base risk for each hidden cell
        for cell in hidden_cells:
            risk_map[cell] = self._calculate_cell_risk(cell, board)
        
        # Apply χ-recursive refinement
        risk_map = self._apply_chi_recursive_refinement(risk_map, board)
        
        # Cache the result
        self.risk_cache[cache_key] = risk_map
        
        self.logger.debug(f"Risk map calculated for {len(hidden_cells)} hidden cells")
        return risk_map
    
    def _create_cache_key(self, board: Board) -> frozenset:
        """Create a cache key from board state."""
        state_items = []
        
        # Add revealed cells with their numbers
        for pos, state in board.cell_states.items():
            if state == CellState.REVEALED:
                number = board.revealed_numbers.get(pos, 0)
                state_items.append((pos, 'revealed', number))
            elif state in [CellState.FLAGGED, CellState.SAFE_FLAGGED]:
                state_items.append((pos, 'flagged'))
        
        return frozenset(state_items)
    
    def _calculate_cell_risk(self, cell: Tuple[int, int], board: Board) -> float:
        """
        Calculate risk for a single cell based on neighboring constraints.
        
        Args:
            cell: Cell coordinates
            board: Current board state
            
        Returns:
            Risk value between 0.0 and 1.0
        """
        x, y = cell
        total_risk = 0.0
        constraint_count = 0
        
        # Check all revealed neighbors for constraints
        for nx, ny in board.get_neighbors(x, y):
            if (nx, ny) in board.get_revealed_cells():
                revealed_number = board.revealed_numbers[(nx, ny)]
                neighbor_risk = self._calculate_neighbor_constraint_risk(
                    (nx, ny), revealed_number, cell, board
                )
                total_risk += neighbor_risk
                constraint_count += 1
        
        # Base risk from global mine density
        if constraint_count == 0:
            base_risk = board.remaining_mines / len(board.get_hidden_cells())
            return min(base_risk, 1.0)
        
        # Average constraint risk
        avg_risk = total_risk / constraint_count
        
        # Apply TORUS theory dampening for χ-recursive stability
        dampening_factor = 1.0 - (0.1 * board.chi_cycle_count / 100)
        dampening_factor = max(0.5, min(1.0, dampening_factor))
        
        return min(avg_risk * dampening_factor, 1.0)
    
    def _calculate_neighbor_constraint_risk(
        self, 
        neighbor_pos: Tuple[int, int], 
        revealed_number: int,
        target_cell: Tuple[int, int], 
        board: Board
    ) -> float:
        """
        Calculate risk contribution from a revealed neighbor's constraint.
        
        Args:
            neighbor_pos: Position of revealed neighbor
            revealed_number: Number shown on revealed neighbor
            target_cell: Cell we're calculating risk for
            board: Current board state
            
        Returns:
            Risk contribution from this constraint
        """
        nx, ny = neighbor_pos
        
        # Get all hidden neighbors of this revealed cell
        hidden_neighbors = []
        flagged_neighbors = 0
        
        for nnx, nny in board.get_neighbors(nx, ny):
            if (nnx, nny) in board.get_hidden_cells():
                hidden_neighbors.append((nnx, nny))
            elif board.cell_states[(nnx, nny)] in [CellState.FLAGGED, CellState.SAFE_FLAGGED]:
                flagged_neighbors += 1
        
        # Calculate remaining mines needed for this constraint
        remaining_mines_needed = revealed_number - flagged_neighbors
        
        if remaining_mines_needed <= 0:
            # All mines already found for this constraint
            return 0.0
        
        if len(hidden_neighbors) == 0:
            # No hidden neighbors but mines still needed - inconsistent state
            return 1.0
        
        if target_cell not in hidden_neighbors:
            # Target cell not constrained by this neighbor
            return 0.0
        
        # Simple probability: remaining mines / remaining hidden cells
        base_probability = remaining_mines_needed / len(hidden_neighbors)
        
        # χ-recursive adjustment based on constraint satisfaction
        chi_adjustment = self._calculate_chi_recursive_adjustment(
            neighbor_pos, hidden_neighbors, board
        )
        
        return min(base_probability * chi_adjustment, 1.0)
    
    def _calculate_chi_recursive_adjustment(
        self,
        constraint_pos: Tuple[int, int],
        hidden_neighbors: List[Tuple[int, int]],
        board: Board
    ) -> float:
        """
        Calculate χ-recursive adjustment factor for constraint risk.
        
        Args:
            constraint_pos: Position of constraining cell
            hidden_neighbors: Hidden neighbors of constraint
            board: Current board state
            
        Returns:
            Adjustment factor for χ-recursive feedback
        """
        self.chi_recursive_depth += 1
        
        # Limit recursion depth for stability
        if self.chi_recursive_depth > 3:
            self.chi_recursive_depth -= 1
            return 1.0
        
        # Calculate feedback from confidence history
        if len(board.confidence_history) > 5:
            recent_confidence = sum(board.confidence_history[-5:]) / 5
            
            # High confidence increases precision (lower adjustment)
            # Low confidence increases caution (higher adjustment)
            confidence_factor = 2.0 - recent_confidence
        else:
            confidence_factor = 1.0
        
        # TORUS theory integration - cyclical adjustment
        torus_cycle = (board.chi_cycle_count % 10) / 10.0
        torus_adjustment = 0.9 + 0.2 * np.sin(2 * np.pi * torus_cycle)
        
        self.chi_recursive_depth -= 1
        return confidence_factor * torus_adjustment
    
    def _apply_chi_recursive_refinement(
        self, 
        risk_map: Dict[Tuple[int, int], float], 
        board: Board
    ) -> Dict[Tuple[int, int], float]:
        """
        Apply χ-recursive refinement to risk map for improved accuracy.
        
        Args:
            risk_map: Initial risk map
            board: Current board state
            
        Returns:
            Refined risk map with χ-recursive adjustments
        """
        refined_map = risk_map.copy()
        
        # Sort cells by risk for χ-recursive processing
        sorted_cells = sorted(risk_map.items(), key=lambda x: x[1], reverse=True)
        
        # Apply refinement in risk order
        for cell, risk in sorted_cells:
            # Check for local consistency with high-risk neighbors
            neighbor_risks = []
            for nx, ny in board.get_neighbors(*cell):
                if (nx, ny) in refined_map:
                    neighbor_risks.append(refined_map[(nx, ny)])
            
            if neighbor_risks:
                # χ-recursive smoothing - balance local vs global risk
                local_avg = sum(neighbor_risks) / len(neighbor_risks)
                global_risk = risk
                
                # Weighted combination favoring global at high risk
                weight = risk  # Higher risk = more global influence
                refined_risk = weight * global_risk + (1 - weight) * local_avg
                refined_map[cell] = min(refined_risk, 1.0)
        
        return refined_map
    
    def get_safest_cells(
        self, 
        board: Board, 
        count: int = 1
    ) -> List[Tuple[int, int]]:
        """
        Get the safest cells to reveal based on risk assessment.
        
        Args:
            board: Current board state
            count: Number of safest cells to return
            
        Returns:
            List of safest cell coordinates
        """
        risk_map = self.calculate_risk_map(board)
        
        if not risk_map:
            return []
        
        # Sort by risk (ascending - lowest risk first)
        sorted_cells = sorted(risk_map.items(), key=lambda x: x[1])
        
        # Return the requested number of safest cells
        safest = [cell for cell, risk in sorted_cells[:count]]
        
        self.logger.debug(f"Identified {len(safest)} safest cells")
        return safest
    
    def get_highest_risk_cells(
        self, 
        board: Board, 
        threshold: float = 0.8,
        count: int = None
    ) -> List[Tuple[int, int]]:
        """
        Get cells with highest mine risk for flagging.
        
        Args:
            board: Current board state
            threshold: Minimum risk threshold for flagging
            count: Maximum number of cells to return (None for all above threshold)
            
        Returns:
            List of high-risk cell coordinates
        """
        risk_map = self.calculate_risk_map(board)
        
        # Filter by threshold
        high_risk_cells = [
            cell for cell, risk in risk_map.items() 
            if risk >= threshold
        ]
        
        # Sort by risk (descending - highest risk first)
        high_risk_cells.sort(key=lambda cell: risk_map[cell], reverse=True)
        
        # Limit count if specified
        if count is not None:
            high_risk_cells = high_risk_cells[:count]
        
        self.logger.debug(f"Identified {len(high_risk_cells)} high-risk cells above {threshold}")
        return high_risk_cells
    
    def clear_cache(self) -> None:
        """Clear the risk calculation cache."""
        self.risk_cache.clear()
        self.logger.debug("Risk cache cleared")
    
    def get_risk_statistics(self, board: Board) -> Dict:
        """
        Get statistical summary of current risk assessment.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary with risk statistics
        """
        risk_map = self.calculate_risk_map(board)
        
        if not risk_map:
            return {"error": "No hidden cells to assess"}
        
        risks = list(risk_map.values())
        
        return {
            "total_cells": len(risks),
            "min_risk": min(risks),
            "max_risk": max(risks),
            "mean_risk": sum(risks) / len(risks),
            "std_risk": np.std(risks),
            "safe_cells": len([r for r in risks if r < 0.2]),
            "dangerous_cells": len([r for r in risks if r > 0.8]),
            "chi_recursive_depth": self.chi_recursive_depth,
            "cache_size": len(self.risk_cache)
        }
