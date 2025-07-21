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
    
    def __init__(self, risk_assessor: RiskAssessor, confidence_tracker: BetaConfidence):
        """
        Initialize the confidence policy wrapper.
        
        Args:
            risk_assessor: RiskAssessor instance for base risk calculation
            confidence_tracker: BetaConfidence instance for confidence tracking
        """
        self.risk_assessor = risk_assessor
        self.confidence_tracker = confidence_tracker
        
        # Policy parameters
        self.base_safe_threshold = 0.2
        self.base_flag_threshold = 0.8
        self.confidence_adjustment_factor = 0.3
        
        # χ-recursive state
        self.policy_iterations = 0
        self.decision_sequence: List[Tuple[str, Tuple[int, int], float]] = []
        
        self.logger = logging.getLogger(__name__)
    
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
            Adjusted threshold value
        """
        # Confidence adjustment
        confidence_adjustment = (confidence - 0.5) * self.confidence_adjustment_factor
        
        if threshold_type == "safe":
            # For safe moves, higher confidence allows taking slightly more risk
            adjusted_threshold = base_threshold + confidence_adjustment
        else:  # flag
            # For flagging, higher confidence allows being more selective
            adjusted_threshold = base_threshold - confidence_adjustment
        
        # Apply χ-recursive stability bounds
        chi_bounds = self._calculate_chi_recursive_bounds(threshold_type)
        adjusted_threshold = max(chi_bounds[0], min(chi_bounds[1], adjusted_threshold))
        
        return adjusted_threshold
    
    def _calculate_chi_recursive_bounds(self, threshold_type: str) -> Tuple[float, float]:
        """
        Calculate χ-recursive stability bounds for thresholds.
        
        Args:
            threshold_type: Type of threshold ('safe' or 'flag')
            
        Returns:
            Tuple of (min_bound, max_bound)
        """
        # Analyze recent decision pattern for χ-recursive feedback
        if len(self.decision_sequence) >= 5:
            recent_actions = [action for action, _, _ in self.decision_sequence[-5:]]
            recent_confidences = [conf for _, _, conf in self.decision_sequence[-5:]]
            
            # If recent actions were mostly successful (high confidence maintained)
            avg_recent_confidence = sum(recent_confidences) / len(recent_confidences)
            
            if avg_recent_confidence > 0.7:
                # High success rate - allow more aggressive thresholds
                if threshold_type == "safe":
                    return (0.05, 0.4)
                else:  # flag
                    return (0.6, 0.95)
            else:
                # Lower success rate - be more conservative
                if threshold_type == "safe":
                    return (0.1, 0.3)
                else:  # flag
                    return (0.7, 0.9)
        
        # Default bounds
        if threshold_type == "safe":
            return (0.05, 0.35)
        else:  # flag
            return (0.65, 0.95)
    
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
        candidates = [
            (pos, risk) for pos, risk in risk_map.items()
            if risk <= threshold
        ]
        
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
        safe_candidates: List[Tuple[Tuple[int, int], float]],
        board: Board
    ) -> Tuple[Tuple[int, int], float]:
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
            x, y = pos
            
            # Calculate information potential
            info_score = 0
            revealed_neighbors = 0
            for nx, ny in board.get_neighbors(x, y):
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
    
    def get_policy_statistics(self) -> Dict:
        """
        Get statistical summary of policy performance.
        
        Returns:
            Dictionary with policy statistics
        """
        confidence_stats = self.confidence_tracker.get_statistics()
        
        # Analyze decision sequence
        action_counts = {}
        for action, _, _ in self.decision_sequence:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        return {
            "policy_iterations": self.policy_iterations,
            "total_decisions": len(self.decision_sequence),
            "action_distribution": action_counts,
            "current_safe_threshold": self._calculate_dynamic_threshold(
                self.base_safe_threshold, 
                self.confidence_tracker.get_decision_confidence("reveal"), 
                "safe"
            ),
            "current_flag_threshold": self._calculate_dynamic_threshold(
                self.base_flag_threshold,
                self.confidence_tracker.get_decision_confidence("flag"),
                "flag"
            ),
            "confidence_stats": confidence_stats
        }
    
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(
        self,
        base_solver: Any,
        alpha: float = 1.0,
        beta: float = 1.0,
        confidence: BetaConfidence | None = None,
    ):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param alpha: initial α for confidence prior.
        :param beta: initial β for confidence prior.
        :param confidence: Optional pre-initialized confidence tracker.
        """
        self.solver = base_solver
        self.confidence = confidence if confidence else BetaConfidence(alpha, beta)
        # Risk threshold τ will be computed each move as a function of confidence

    def choose_move(self, board_state: Board) -> Cell:
        """
        Select the next move based on confidence-adjusted risk threshold.

        :param board_state: Current state of the Minesweeper board.
        :return: The chosen Cell object.
        """
        # 1. Get the probability map from the underlying solver
        prob_map = self.solver.estimate(board_state)  # Use RiskAssessor's estimate method

        hidden_cells = [
            cell for row in board_state.grid for cell in row if board_state.is_hidden(cell)
        ]

        # 2. Compute dynamic risk threshold τ based on current confidence level
        tau = self.confidence.get_threshold()

        # 3. Find candidate moves with probability <= τ
        safe_candidates = [cell for cell in hidden_cells if prob_map[cell] <= tau]
        if safe_candidates:
            # choose the candidate with the lowest mine probability
            move = min(safe_candidates, key=lambda cell: prob_map[cell])
        else:
            # no cell is below threshold; take the least risky cell available
            move = min(hidden_cells, key=lambda cell: prob_map[cell])

        return move
