from typing import Any, Dict, List, Tuple
import numpy as np
from ai_minesweeper.board import Board

class DPP14RecursionEngine:
    @staticmethod
    def _as_coords(move):
        return move if isinstance(move, tuple) else (move.row, move.col)
    """
    Implements a 14-lane Deep Parallel Processing (DPP) recursion engine
    aligned with TORUS Theory for hypothesis discovery.
    """

    class RecursionLane:
        def __init__(self, lane_id: int, board: Any, solver_policy: Any):
            self.lane_id = lane_id
            self.board = board
            self.solver_policy = solver_policy
            from typing import Optional, Union
            self.chi_value: Optional[float] = None
            self.resonance_zones: List[Union[Tuple[int, int], str]] = []
            self.collapsed = False
            # Simple, reproducible per-lane metric: safe move ratio
            self._moves_total = 0
            self._moves_safe = 0

    def __init__(self, board: Any, solver_policy_class: Any, debug_mode: bool = False):
        self.lanes = []
        self.debug_mode = debug_mode
        self.osqn = 0  # Observation Sequence Quantum Number
        for lane_id in range(14):
            lane_board = self._copy_board(board)
            solver_policy = solver_policy_class()
            self.lanes.append(self.RecursionLane(lane_id, lane_board, solver_policy))

    def _copy_board(self, board: Any) -> Any:
        """Creates a deep copy of the board for each lane."""
        import copy

        return copy.deepcopy(board)

    def run(self) -> Dict[str, Any]:
        """
        Executes the 14-lane recursion engine and aggregates results.

        :return: A dictionary containing final_chi14, lane_results, and collapsed_lanes.
        """
        print("[DPP14] Starting engine...")
        if self.debug_mode:
            print("[DPP14] Debug mode ON ")

        for lane in self.lanes[: 2 if self.debug_mode else len(self.lanes)]:
            self._run_lane(lane)

        # Aggregate only lanes that produced a chi_value; fallback to 0.0
        chi_values = []
        for lane in self.lanes:
            # Ensure a fallback chi_value using safe move ratio
            if lane.chi_value is None:
                lane.chi_value = (
                    lane._moves_safe / max(1, lane._moves_total)
                ) if lane._moves_total is not None else 0.0
            chi_values.append(float(lane.chi_value))
        final_chi14 = float(sum(chi_values) / len(chi_values)) if chi_values else 0.0
        collapsed_lanes = [lane.lane_id for lane in self.lanes if lane.collapsed]

        return {
            "chi_values": chi_values,
            "final_chi14": final_chi14,
            "lane_results": [lane.resonance_zones for lane in self.lanes],
            "collapsed_lanes": collapsed_lanes,
            "osqn_last": self.osqn,
        }

    def _run_lane(self, lane: RecursionLane) -> None:
        """Runs the solver for a single lane."""
        max_steps = 1000
        steps = 0

        while not lane.collapsed:
            if steps > max_steps:
                print(
                    f"[DPP14] Lane {lane.lane_id} hit max steps ({max_steps}). Aborting."
                )
                break

            print(f"[DPP14] Lane {lane.lane_id}, Step {steps}")
            move = lane.solver_policy.choose_move(lane.board)
            if move is None:
                print(f"[DPP14] Lane {lane.lane_id} – No valid moves returned. Terminating.")
                break
            # Accept Cell or tuple moves
            if hasattr(move, 'row') and hasattr(move, 'col'):
                r, c = move.row, move.col
            else:
                r, c = move
            # Predict probability for feedback (optional)
            predicted = 0.0
            if hasattr(lane.solver_policy, 'confidence'):
                solver = getattr(lane.solver_policy, 'solver', lane.solver_policy)
                try:
                    if hasattr(solver, 'predict'):
                        pm = solver.predict(lane.board)
                    else:
                        pm = solver.estimate(lane.board)
                    predicted = pm.get((r, c), 0.0)
                except Exception:
                    predicted = 0.0

            if not lane.board.has_unresolved_cells():
                print(f"[DPP14] Lane {lane.lane_id} – Discovery converged.")
                break

            print(f"[DPP14] Lane {lane.lane_id}, Board State: {lane.board}")
            print(f"[DPP14] Lane {lane.lane_id}, Move: {move}")

            # If only mines remain hidden, treat as converged (avoid forced collapse)
            try:
                hidden = set(lane.board.get_hidden_cells()) if hasattr(lane.board, 'get_hidden_cells') else set()
                mines = set(lane.board.mine_positions) if hasattr(lane.board, 'mine_positions') else set()
                if hidden and hidden.issubset(mines):
                    print(f"[DPP14] Lane {lane.lane_id} – Only mines remain hidden. Converged.")
                    break
            except Exception:
                pass

            result = self._reveal_cell(lane, r, c)
            print(f"[DPP14] Step {steps} – Chose cell ({r},{c}), result={result}")
            self._visualize_board(lane.board)
            # Update confidence tracker and chi_value for this lane
            cell = lane.board.grid[r][c]
            lane._moves_total += 1
            if not getattr(cell, 'is_mine', False):
                lane._moves_safe += 1
            # OSQN tick on each observation
            self._tick_osqn()
            if hasattr(lane.solver_policy, 'confidence'):
                try:
                    lane.solver_policy.confidence.update(
                        predicted_probability=predicted,
                        revealed_is_mine=bool(getattr(cell, 'is_mine', False)),
                    )
                    lane.chi_value = float(lane.solver_policy.confidence.mean())
                except Exception:
                    # Fallback: safe move ratio
                    lane.chi_value = lane._moves_safe / max(1, lane._moves_total)
            if result == "false_hypothesis":
                print(f"[DPP14] Lane {lane.lane_id} collapsed: Contradiction encountered.")
                lane.collapsed = True
                # Treat contradiction as an observation
                self._tick_osqn()
            else:
                lane.resonance_zones.append(result)
            steps += 1

    def _tick_osqn(self):
        self.osqn = (self.osqn + 1) % 14

    def _reveal_cell(self, lane, r, c):
        cell = lane.board.grid[r][c]
        lane.board.reveal(r, c)
        return "false_hypothesis" if cell.is_mine else "empty"

    def _test_hypothesis(self, board: Any, move: Any) -> str:
        """Simulates testing a hypothesis. Robust to mocks and missing board methods."""
        # Accept both tuple and Cell moves
        if isinstance(move, tuple):
            r, c = move
        else:
            r, c = move.row, move.col
        if hasattr(board, "grid"):
            cell = board.grid[r][c]
            is_mine = getattr(cell, "is_mine", False)
        else:
            is_mine = False
        if is_mine:
            return "contradiction"
        # Only expand if board supports it
        if hasattr(board, 'add_cell') and hasattr(board, 'expand_grid') and hasattr(board, 'reveal'):
            board.add_cell(r, c, is_mine=False)
            board.expand_grid(board.n_rows, board.n_cols)
            board.reveal(r, c)
        # If not, just check the hypothesis
        return "valid"

    def _visualize_board(self, board: "Board") -> None:
        """(Dev stub) No-op visualiser used only in debug mode."""
        return
