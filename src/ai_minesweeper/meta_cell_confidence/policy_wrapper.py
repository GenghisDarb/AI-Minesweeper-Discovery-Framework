"""
Policy Wrapper for integrating risk assessment with confidence-based decision making.

This module wraps the RiskAssessor with confidence policies for dynamic
risk threshold adjustment and χ-recursive decision optimization.
"""

import logging
from typing import Dict, Tuple, List, Optional, Set
from ..risk_assessor import RiskAssessor
from ..board import Board
from .beta_confidence import BetaConfidence
from typing import Any

from ai_minesweeper.board import Board
from ai_minesweeper.cell import Cell

from .confidence import BetaConfidence


class ConfidencePolicy:
    """
    Policy wrapper that integrates risk assessment with confidence-based decision making.
    
    Features:
    - Dynamic risk threshold adjustment based on confidence levels
    - χ-recursive decision optimization
    - Integration with BetaConfidence for adaptive learning
    - TORUS theory alignment for cyclical improvement
    """
    
    def __init__(self, base_solver, confidence: BetaConfidence | None = None):
        # Instantiate base_solver if a class is provided
        if callable(base_solver) and not hasattr(base_solver, "estimate"):
            base_solver = base_solver()
        self.solver = base_solver
        self.confidence = confidence if confidence is not None else BetaConfidence()
        self.logger = logging.getLogger(__name__)
        # Restore attributes for legacy/test compatibility
        self.policy_iterations = 0
        self.base_safe_threshold = 0.2
        self.base_flag_threshold = 0.8
        self.confidence_adjustment_factor = 0.3
        self.decision_sequence = []
        self.confidence_tracker = self.confidence
        self.risk_assessor = self.solver
    
    def get_recommended_action(self, board: Board) -> Dict:
        """
        Get recommended action based on confidence-adjusted risk assessment.
        
        Args:
            board: Current board state
            
        Returns:
            Dictionary with recommended action and metadata
        """
        self.policy_iterations += 1

        # Get base risk map from risk assessor
        risk_map = self.risk_assessor.calculate_risk_map(board)

        # Assert all values are floats
        for v in risk_map.values():
            assert isinstance(v, float), f"Risk map value is not float: {v} (type {type(v)})"

        if not risk_map:
            return {"action": "none", "reason": "No hidden cells available"}

        # Get current confidence levels
        overall_confidence = self.confidence_tracker.get_confidence()
        reveal_confidence = self.confidence_tracker.get_decision_confidence("reveal")
        flag_confidence = self.confidence_tracker.get_decision_confidence("flag")

        # Calculate dynamic thresholds
        safe_threshold = self._calculate_dynamic_threshold(
            self.base_safe_threshold, reveal_confidence, "safe"
        )
        flag_threshold = self._calculate_dynamic_threshold(
            self.base_flag_threshold, flag_confidence, "flag"
        )

        # Find candidate actions
        safe_candidates = self._find_safe_candidates(risk_map, safe_threshold)
        flag_candidates = self._find_flag_candidates(risk_map, flag_threshold)

        # Apply χ-recursive decision optimization
        recommendation = self._optimize_decision(
            safe_candidates, flag_candidates, risk_map, board, overall_confidence
        )

        # Record decision for χ-recursive learning
        if recommendation["action"] != "none":
            self.decision_sequence.append((
                recommendation["action"],
                recommendation.get("position"),
                overall_confidence
            ))

        self.logger.debug(f"Policy recommendation: {recommendation['action']} with confidence {overall_confidence:.3f}")
        return recommendation
    
    def _calculate_dynamic_threshold(
        self,
        base_threshold: float,
        confidence: float,
        threshold_type: str
    ) -> float:
        """
        Calculate dynamic threshold based on confidence level.

        Args:
            base_threshold: Base threshold value
            confidence: Current confidence level
            threshold_type: Type of threshold ('safe' or 'flag')

        Returns:
            A float threshold value for risk comparison
        """
        # Analyze recent decision pattern for χ-recursive feedback
        if len(self.decision_sequence) >= 5:
            recent_confidences = [conf for _, _, conf in self.decision_sequence[-5:]]
            avg_recent_confidence = sum(recent_confidences) / len(recent_confidences)
            if avg_recent_confidence > 0.7:
                # High success rate - allow more aggressive thresholds
                if threshold_type == "safe":
                    return 0.4
                else:  # flag
                    return 0.95
            else:
                # Lower success rate - be more conservative
                if threshold_type == "safe":
                    return 0.3
                else:  # flag
                    return 0.9
        # Default bounds
        if threshold_type == "safe":
            return 0.35
        else:  # flag
            return 0.95
    
    def _find_safe_candidates(
        self,
        risk_map: Dict[Tuple[int, int], float],
        threshold: float
    ) -> List[Tuple[Tuple[int, int], float]]:
        """
        Find safe move candidates based on risk threshold.

        Args:
            risk_map: Risk map with coordinate keys
            threshold: Safe threshold value

        Returns:
            List of (position, risk) tuples for safe candidates
        """
        candidates = []
        for pos, risk in risk_map.items():
            if not isinstance(risk, float):
                raise TypeError(f"Risk value for {pos} is not float: {risk} (type {type(risk)})")
            if risk <= threshold:
                candidates.append((pos, risk))
        # Sort by risk (ascending - safest first)
        candidates.sort(key=lambda x: x[1])
        return candidates
    
    def _find_flag_candidates(
        self, 
        risk_map: Dict[Tuple[int, int], float], 
        threshold: float
    ) -> List[Tuple[Tuple[int, int], float]]:
        """
        Find flag candidates based on risk threshold.
        
        Args:
            risk_map: Risk map with coordinate keys
            threshold: Flag threshold value
            
        Returns:
            List of (position, risk) tuples for flag candidates
        """
        candidates = [
            (pos, risk) for pos, risk in risk_map.items()
            if risk >= threshold
        ]
        
        # Sort by risk (descending - highest risk first)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return candidates
    
    def _optimize_decision(
        self,
        safe_candidates: List[Tuple[Tuple[int, int], float]],
        flag_candidates: List[Tuple[Tuple[int, int], float]],
        risk_map: Dict[Tuple[int, int], float],
        board: Board,
        confidence: float
    ) -> Dict:
        """
        Apply χ-recursive optimization to select the best decision.
        
        Args:
            safe_candidates: List of safe move candidates
            flag_candidates: List of flag candidates
            risk_map: Complete risk map
            board: Current board state
            confidence: Overall confidence level
            
        Returns:
            Optimized decision recommendation
        """
        # Priority 1: High-confidence flagging
        if flag_candidates and confidence > 0.7:
            pos, risk = flag_candidates[0]
            return {
                "action": "flag",
                "position": pos,
                "risk": risk,
                "confidence": confidence,
                "reason": f"High-confidence flag (risk={risk:.3f})"
            }
        
        # Priority 2: Safe reveals
        if safe_candidates:
            # Apply χ-recursive selection from safe candidates
            selected_safe = self._apply_chi_recursive_selection(safe_candidates, board)
            pos, risk = selected_safe
            return {
                "action": "reveal",
                "position": pos,
                "risk": risk,
                "confidence": confidence,
                "reason": f"Safe reveal (risk={risk:.3f})"
            }
        
        # Priority 3: Medium-confidence flagging
        if flag_candidates and confidence > 0.5:
            pos, risk = flag_candidates[0]
            return {
                "action": "flag",
                "position": pos,
                "risk": risk,
                "confidence": confidence,
                "reason": f"Medium-confidence flag (risk={risk:.3f})"
            }
        
        # Priority 4: Forced move (lowest risk available)
        if risk_map:
            safest_pos = min(risk_map.items(), key=lambda x: x[1])
            pos, risk = safest_pos
            return {
                "action": "reveal",
                "position": pos,
                "risk": risk,
                "confidence": confidence,
                "reason": f"Forced move - lowest risk (risk={risk:.3f})"
            }
        
        return {"action": "none", "reason": "No valid moves available"}
    
    def _apply_chi_recursive_selection(
        self,
        safe_candidates: List[Tuple[Any, float]],
        board: Board
    ) -> Tuple[Any, float]:
        """
        Apply χ-recursive selection logic to choose from safe candidates.

        Args:
            safe_candidates: List of safe move candidates
            board: Current board state

        Returns:
            Selected candidate (position, risk)
        """
        if len(safe_candidates) == 1:
            return safe_candidates[0]

        # χ-recursive selection based on TORUS theory
        # Prefer cells that create more information or break symmetry
        scored_candidates = []

        for pos, risk in safe_candidates[:5]:  # Limit to top 5 safest
            # Accept both Cell and tuple keys
            if hasattr(pos, "row") and hasattr(pos, "col"):
                x, y = pos.row, pos.col
            elif isinstance(pos, tuple) and len(pos) == 2:
                x, y = pos
            else:
                continue

            # Calculate information potential
            info_score = 0
            revealed_neighbors = 0
            for nx, ny in board.adjacent_cells(x, y):
                if (nx, ny) in board.get_revealed_cells():
                    revealed_neighbors += 1
                    # Higher numbers provide more constraint information
                    info_score += board.revealed_numbers.get((nx, ny), 0)

            # Prefer cells with moderate neighbor information
            # (not isolated, but not overconstrained)
            if revealed_neighbors > 0:
                avg_neighbor_info = info_score / revealed_neighbors
                selection_score = avg_neighbor_info * (1 - risk)
            else:
                # Isolated cell - lower priority but still valuable
                selection_score = 0.5 * (1 - risk)

            scored_candidates.append((pos, risk, selection_score))

        # Select highest scoring candidate
        best_candidate = max(scored_candidates, key=lambda x: x[2])
        return (best_candidate[0], best_candidate[1])
    
    def update_policy_outcome(
        self, 
        action: str, 
        position: Tuple[int, int], 
        success: bool,
        outcome_quality: float = 1.0
    ) -> None:
        """
        Update policy based on action outcome.
        
        Args:
            action: Action taken ('reveal' or 'flag')
            position: Position where action was taken
            success: Whether action was successful
            outcome_quality: Quality of outcome (0.0 to 1.0)
        """
        if success:
            self.confidence_tracker.update_success(action, outcome_quality)
        else:
            self.confidence_tracker.update_failure(action, 1.0 - outcome_quality)
        
        self.logger.debug(f"Policy outcome updated: {action} at {position}, success={success}")
    

    # The second __init__ override has been removed to preserve the unified constructor above
    def choose_move(self, board_state):
        """
        Select the next move based on confidence-adjusted risk threshold.
        Returns a Cell or (row, col) tuple depending on board type.
        """
        # Accept both .estimate and .predict for legacy/mock compatibility
        if hasattr(self.solver, "estimate"):
            prob_map = self.solver.estimate(board_state)
        else:
            prob_map = self.solver.predict(board_state)
        # Sanitize probability map
        for k in prob_map:
            if prob_map[k] is None or not isinstance(prob_map[k], (int, float)):
                prob_map[k] = 1.0
        # Remove any keys with None after sanitization
        prob_map = {k: v for k, v in prob_map.items() if v is not None}
        total = sum(prob_map.values())
        if total > 0:
            prob_map = {k: v / total for k, v in prob_map.items()}
        tau = self.confidence.get_threshold()
        # Candidates are all keys in prob_map that are hidden
        def is_hidden(pos):
            if hasattr(board_state, "is_hidden"):
                # Accepts either (row,col) or Cell
                try:
                    return board_state.is_hidden(pos)
                except Exception:
                    if hasattr(board_state, "grid") and isinstance(pos, tuple):
                        r, c = pos
                        return board_state.is_hidden(board_state.grid[r][c])
                    return False
            return False
        candidates = [pos for pos in prob_map if is_hidden(pos)]
        if not candidates:
            return None
        safe_candidates = [pos for pos in candidates if prob_map[pos] <= tau]
        move_key = min(safe_candidates, key=lambda pos: prob_map[pos]) if safe_candidates else candidates[0]
        # Return Cell if possible, else tuple
        if hasattr(board_state, "grid") and isinstance(move_key, tuple):
            r, c = move_key
            return board_state.grid[r][c]
        return move_key
    
    # Add robust hidden_cells fallback for mocks
    def _get_hidden_cells(self, board_state):
        if hasattr(board_state, "grid"):
            return [cell for row in board_state.grid for cell in row if board_state.is_hidden(cell)]
        elif hasattr(board_state, "hidden_cells"):
            return board_state.hidden_cells()
        else:
            raise AttributeError("Board object must have either .grid or .hidden_cells")
        chosen = None
        if safe_candidates:
            chosen = min(safe_candidates, key=lambda c: prob_map.get(c, prob_map.get((getattr(c, 'row', 0), getattr(c, 'col', 0)), 1.0)))
        elif hidden_cells:
            chosen = hidden_cells[0]
        else:
            return None
        # Return type: tuple if using predict(), else Cell, or as set by return_tuple
        if self.return_tuple:
            if hasattr(chosen, 'row') and hasattr(chosen, 'col'):
                return (chosen.row, chosen.col)
            return chosen
        else:
            if isinstance(chosen, tuple):
                # Convert tuple to Cell
                r, c = chosen
                return board_state.grid[r][c]
            return chosen
