"""
Beta Confidence module for χ-recursive feedback mechanisms.

This module implements confidence tracking and feedback for the χ-recursive
minesweeper AI, providing adaptive learning capabilities.
"""

import logging

import numpy as np


class BetaConfidence:
    """
    Beta confidence tracker for χ-recursive decision making.
    
    Implements adaptive confidence measurement and feedback mechanisms
    aligned with TORUS theory for cyclical learning improvement.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        """
        Initialize beta confidence tracker.
        
        Args:
            alpha: Success parameter for beta distribution
            beta: Failure parameter for beta distribution
        """
        self.alpha = alpha
        self.beta = beta
        self.initial_alpha = alpha
        self.initial_beta = beta

        # Track decision outcomes
        self.decision_history: list[tuple[str, bool, float]] = []
        self.confidence_scores: list[float] = []

        # χ-recursive state
        self.chi_cycle_phase = 0
        self.recursive_updates = 0

        self.logger = logging.getLogger(__name__)

    def get_confidence(self) -> float:
        """
        Get current confidence level based on beta distribution.
        
        Returns:
            Confidence value between 0.0 and 1.0
        """
        # Beta distribution mean: alpha / (alpha + beta)
        base_confidence = self.alpha / (self.alpha + self.beta)

        # Apply χ-recursive modulation
        chi_modulation = self._calculate_chi_modulation()

        # Combine base confidence with χ-recursive feedback
        final_confidence = base_confidence * chi_modulation

        # Ensure bounds
        final_confidence = max(0.01, min(0.99, final_confidence))

        self.confidence_scores.append(final_confidence)
        return final_confidence

    def update_success(self, decision_type: str, outcome_quality: float = 1.0) -> None:
        """
        Update confidence based on successful decision.
        
        Args:
            decision_type: Type of decision made ('reveal', 'flag', 'deduce')
            outcome_quality: Quality of outcome (0.0 to 1.0)
        """
        # Update beta distribution parameters
        self.alpha += outcome_quality

        # Record decision
        self.decision_history.append((decision_type, True, outcome_quality))

        # χ-recursive update
        self._update_chi_recursive_state(True, outcome_quality)

        self.logger.debug(f"Success update: {decision_type}, quality={outcome_quality:.3f}")

    def update_failure(self, decision_type: str, failure_severity: float = 1.0) -> None:
        """
        Update confidence based on failed decision.
        
        Args:
            decision_type: Type of decision made
            failure_severity: Severity of failure (0.0 to 1.0)
        """
        # Update beta distribution parameters
        self.beta += failure_severity

        # Record decision
        self.decision_history.append((decision_type, False, failure_severity))

        # χ-recursive update
        self._update_chi_recursive_state(False, failure_severity)

        self.logger.debug(f"Failure update: {decision_type}, severity={failure_severity:.3f}")

    def _calculate_chi_modulation(self) -> float:
        """
        Calculate χ-recursive modulation factor.
        
        Returns:
            Modulation factor for confidence adjustment
        """
        if len(self.confidence_scores) < 5:
            return 1.0

        # Analyze recent confidence trend
        recent_scores = self.confidence_scores[-5:]
        trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]

        # χ-cycle phase progression
        self.chi_cycle_phase = (self.chi_cycle_phase + 1) % 20

        # TORUS theory cyclical modulation
        torus_factor = 0.9 + 0.2 * np.cos(2 * np.pi * self.chi_cycle_phase / 20)

        # Trend-based adjustment
        if trend > 0.01:  # Improving trend
            trend_factor = 1.05
        elif trend < -0.01:  # Declining trend
            trend_factor = 0.95
        else:  # Stable trend
            trend_factor = 1.0

        return torus_factor * trend_factor

    def _update_chi_recursive_state(self, success: bool, magnitude: float) -> None:
        """
        Update χ-recursive state based on decision outcome.
        
        Args:
            success: Whether the decision was successful
            magnitude: Magnitude of the outcome
        """
        self.recursive_updates += 1

        # χ-recursive adaptation based on outcome pattern
        if len(self.decision_history) >= 3:
            recent_outcomes = [outcome for _, outcome, _ in self.decision_history[-3:]]

            # Pattern detection for χ-recursive learning
            if all(recent_outcomes):
                # Consecutive successes - increase confidence adaptation rate
                self.alpha *= 1.02
            elif not any(recent_outcomes):
                # Consecutive failures - decrease confidence more slowly
                self.beta *= 0.98

    def get_decision_confidence(self, decision_type: str) -> float:
        """
        Get confidence level for a specific decision type.
        
        Args:
            decision_type: Type of decision ('reveal', 'flag', 'deduce')
            
        Returns:
            Confidence level for this decision type
        """
        base_confidence = self.get_confidence()

        # Type-specific adjustments based on history
        type_history = [
            (outcome, quality) for dtype, outcome, quality in self.decision_history
            if dtype == decision_type
        ]

        if not type_history:
            return base_confidence

        # Calculate type-specific success rate
        successes = sum(quality for outcome, quality in type_history if outcome)
        attempts = len(type_history)
        type_success_rate = successes / attempts if attempts > 0 else 0.5

        # Combine base confidence with type-specific rate
        combined_confidence = (base_confidence + type_success_rate) / 2

        return max(0.01, min(0.99, combined_confidence))

    def reset_confidence(self) -> None:
        """Reset confidence to initial values."""
        self.alpha = self.initial_alpha
        self.beta = self.initial_beta
        self.decision_history.clear()
        self.confidence_scores.clear()
        self.chi_cycle_phase = 0
        self.recursive_updates = 0

        self.logger.info("Beta confidence reset to initial values")

    def get_confidence_trend(self, window: int = 10) -> float:
        """
        Get confidence trend over recent decisions.
        
        Args:
            window: Number of recent scores to analyze
            
        Returns:
            Trend value (positive = improving, negative = declining)
        """
        if len(self.confidence_scores) < 2:
            return 0.0

        recent_scores = self.confidence_scores[-window:]
        if len(recent_scores) < 2:
            return 0.0

        # Linear regression slope
        trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
        return trend

    def get_statistics(self) -> dict:
        """
        Get statistical summary of confidence tracking.
        
        Returns:
            Dictionary with confidence statistics
        """
        if not self.confidence_scores:
            return {"error": "No confidence data available"}

        decision_types = {}
        for dtype, outcome, quality in self.decision_history:
            if dtype not in decision_types:
                decision_types[dtype] = {"successes": 0, "attempts": 0}
            decision_types[dtype]["attempts"] += 1
            if outcome:
                decision_types[dtype]["successes"] += quality

        return {
            "current_confidence": self.get_confidence(),
            "alpha": self.alpha,
            "beta": self.beta,
            "total_decisions": len(self.decision_history),
            "confidence_trend": self.get_confidence_trend(),
            "chi_cycle_phase": self.chi_cycle_phase,
            "recursive_updates": self.recursive_updates,
            "decision_types": decision_types,
            "mean_confidence": np.mean(self.confidence_scores),
            "confidence_std": np.std(self.confidence_scores)
        }
