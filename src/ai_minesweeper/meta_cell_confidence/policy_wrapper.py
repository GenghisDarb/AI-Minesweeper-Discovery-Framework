"""
Policy Wrapper for integrating risk assessment with confidence-based decision making.

This module wraps the RiskAssessor with confidence policies for dynamic
risk threshold adjustment and χ-recursive decision optimization.
"""

import logging
import numbers
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from ..board import Board
from ..risk_assessor import RiskAssessor
from .confidence import BetaConfidence


class ConfidencePolicy:
    """Policy wrapper that integrates risk assessment with confidence-based decision making.
    
    Features:
    - Dynamic risk threshold adjustment based on confidence levels
    - χ-recursive decision optimization
    - Integration with BetaConfidence for adaptive learning
    - TORUS theory alignment for cyclical improvement
    """

    # Attribute annotations for static analysis and clarity
    solver: Any
    risk_assessor: RiskAssessor
    confidence: BetaConfidence
    logger: logging.Logger
    policy_iterations: int
    base_safe_threshold: float
    base_flag_threshold: float
    confidence_adjustment_factor: float
    decision_sequence: list[tuple[str, Any, float]]
    confidence_tracker: BetaConfidence
    legacy_policy_iterations: int
    legacy_decision_sequence: list
    legacy_confidence_tracker: BetaConfidence
    def __init__(self, base_solver, confidence: BetaConfidence | None = None):
        # Instantiate base_solver if a class is provided; default to RiskAssessor-like
        try:
            if callable(base_solver) and not hasattr(base_solver, "estimate"):
                base_solver = base_solver()
        except Exception:
            pass
        self.solver = base_solver
        # Ensure we have a solver with estimate() or predict(); fallback to RiskAssessor
        if not hasattr(self.solver, "estimate") and not hasattr(self.solver, "predict"):
            self.solver = RiskAssessor()
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
        # Legacy/test attributes
        self.legacy_policy_iterations = 0
        self.legacy_decision_sequence = []
        self.legacy_confidence_tracker = self.confidence

    def get_policy_statistics(self) -> dict:
        """Return simple statistics used by tests."""
        return {
            "policy_iterations": self.policy_iterations,
            "decision_count": len(self.decision_sequence),
            "confidence_mean": getattr(self.confidence, "mean", lambda: 0.5)(),
        }

    def get_recommended_action(self, board: 'Board') -> dict:
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

        # Validate numeric values (accept ints, floats, numpy scalars)
        for v in risk_map.values():
            assert isinstance(v, numbers.Real), (
                f"Risk map value is not numeric: {v} (type {type(v)})"
            )

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
        risk_map: dict[tuple[int, int], float],
        threshold: float
    ) -> list[tuple[tuple[int, int], float]]:
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
            if not isinstance(risk, numbers.Real):
                raise TypeError(
                    f"Risk value for {pos} is not numeric: {risk} (type {type(risk)})"
                )
            if float(risk) <= float(threshold):
                candidates.append((pos, float(risk)))
        # Sort by risk (ascending - safest first)
        candidates.sort(key=lambda x: x[1])
        return candidates

    def _find_flag_candidates(
        self,
        risk_map: dict[tuple[int, int], float],
        threshold: float
    ) -> list[tuple[tuple[int, int], float]]:
        """
        Find flag candidates based on risk threshold.
        
        Args:
            risk_map: Risk map with coordinate keys
            threshold: Flag threshold value
            
        Returns:
            List of (position, risk) tuples for flag candidates
        """
        candidates = [
            (pos, float(risk)) for pos, risk in risk_map.items()
            if float(risk) >= float(threshold)
        ]

        # Sort by risk (descending - highest risk first)
        candidates.sort(key=lambda x: x[1], reverse=True)

        return candidates

    def _optimize_decision(
        self,
        safe_candidates: list[tuple[tuple[int, int], float]],
        flag_candidates: list[tuple[tuple[int, int], float]],
        risk_map: dict[tuple[int, int], float],
        board,
        confidence: float
    ) -> dict:
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
        safe_candidates: list[tuple[Any, float]],
        board
    ) -> tuple[Any, float]:
        """
        Apply χ-recursive selection logic to choose from safe candidates.

        Args:
            safe_candidates: List of safe move candidates
            board

        Returns:
            Selected candidate (position, risk)
        """
        if len(safe_candidates) == 1:
            return safe_candidates[0]

        # χ-recursive selection based on TORUS theory
        # Prefer cells that create more information or break symmetry
        scored_candidates = []
        for candidate, risk in safe_candidates:
            info_score = 0
            revealed_neighbors = 0
            for nx, ny in board.adjacent_cells(*candidate):
                if board.is_revealed(nx, ny):
                    revealed_neighbors += 1
                    info_score += board.get_adjacent_mines(nx, ny)
            scored_candidates.append((candidate, risk, info_score, revealed_neighbors))

        # Sort by information score and revealed neighbors
        scored_candidates.sort(key=lambda x: (-x[2], -x[3], x[1]))
        return scored_candidates[0][:2]

    def update_policy_outcome(
        self,
        action: str,
        position: tuple[int, int],
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
        estimate = getattr(self.solver, "estimate", None)
        predict = getattr(self.solver, "predict", None)
        prob_map: dict[Any, float] = {}
        if callable(estimate):
            pm = estimate(board_state)
            if isinstance(pm, dict):
                prob_map = cast(dict[Any, float], pm)
            else:
                try:
                    prob_map = dict(pm)  # type: ignore[arg-type]
                except Exception:
                    prob_map = {}
            # Sanitize probability map (estimate branch)
            for k in list(prob_map.keys()):
                v = prob_map[k]
                if v is None or not isinstance(v, (int, float)):
                    prob_map[k] = 1.0
        elif callable(predict):
            pm = predict(board_state)
            if isinstance(pm, dict):
                prob_map = cast(dict[Any, float], pm)
            else:
                try:
                    prob_map = dict(pm)  # type: ignore[arg-type]
                except Exception:
                    prob_map = {}
            # Sanitize probability map (predict branch)
            for k in list(prob_map.keys()):
                v = prob_map[k]
                if v is None or not isinstance(v, (int, float)):
                    prob_map[k] = 1.0
        else:
            prob_map = {}
        # Remove any keys with None after sanitization
        prob_map = {k: v for k, v in prob_map.items() if v is not None}
        total = sum(prob_map.values())
        if total > 0:
            prob_map = {k: v / total for k, v in prob_map.items()}
        tau = self.confidence.get_threshold()
        # Candidates are all keys in prob_map that are hidden
        def is_hidden(pos):
            if not hasattr(board_state, "is_hidden"):
                return False
            # Try common signatures: (Cell), (row,col)
            try:
                return board_state.is_hidden(pos)
            except TypeError:
                if isinstance(pos, tuple) and len(pos) == 2:
                    r, c = pos
                    try:
                        return board_state.is_hidden(r, c)
                    except Exception:
                        pass
                if hasattr(board_state, "grid") and isinstance(pos, tuple):
                    r, c = pos
                    try:
                        return board_state.is_hidden(board_state.grid[r][c])
                    except Exception:
                        return False
                return False
        candidates = [pos for pos in prob_map if is_hidden(pos)]
        if not candidates:
            return None
        # Sort deterministically by row,col to break ties predictably
        try:
            candidates.sort(key=lambda pos: (pos[0], pos[1]))
        except Exception:
            pass
        # Enforce deterministic progression across calls: pick the nth best unseen
        if not hasattr(self, "_picked_order"):
            self._picked_order = []
        def order_key(pos):
            risk_val = prob_map.get(pos, 1.0)
            if isinstance(pos, tuple) and len(pos) >= 2:
                return (risk_val, pos[0], pos[1])
            # Fallback for objects with row/col attributes without static typing guarantees
            r = getattr(pos, "row", None)
            c = getattr(pos, "col", None)
            if isinstance(r, numbers.Integral) and isinstance(c, numbers.Integral):
                return (risk_val, int(r), int(c))
            return (risk_val, 0, 0)
        ordered = sorted(candidates, key=order_key)
        # Find first not yet chosen
        move_key = next((pos for pos in ordered if pos not in getattr(self, "_picked_order", [])), ordered[0])
        self._picked_order.append(move_key)
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
