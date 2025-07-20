from typing import Dict, Any, List, Tuple
from ai_minesweeper.board import Board  # Fix undefined


class DPP14RecursionEngine:
    """
    Implements a 14-lane Deep Parallel Processing (DPP) recursion engine
    aligned with TORUS Theory for hypothesis discovery.
    """

    class RecursionLane:
        def __init__(self, lane_id: int, board: Any, solver_policy: Any):
            self.lane_id = lane_id
            self.board = board
            self.solver_policy = solver_policy
            self.chi_value = None
            self.resonance_zones: List[Tuple[int, int]] = []
            self.collapsed = False

    def __init__(self, board: Any, solver_policy_class: Any, debug_mode: bool = False):
        self.lanes = []
        self.debug_mode = debug_mode
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

        final_chi14 = sum(lane.chi_value or 0 for lane in self.lanes) / len(self.lanes)
        collapsed_lanes = [lane.lane_id for lane in self.lanes if lane.collapsed]

        chi_values = [lane.chi_value for lane in self.lanes]  # Ensure chi_values is defined

        return {
            "chi_values": chi_values,
            "final_chi14": final_chi14,
            "lane_results": [lane.resonance_zones for lane in self.lanes],
            "collapsed_lanes": collapsed_lanes,
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
                print(
                    f"[DPP14] Lane {lane.lane_id} – No valid moves returned. Terminating."
                )
                break

            if not lane.board.has_unresolved_cells():
                print(f"[DPP14] Lane {lane.lane_id} – Discovery converged.")
                break

            print(f"[DPP14] Lane {lane.lane_id}, Board State: {lane.board}")
            print(f"[DPP14] Lane {lane.lane_id}, Move: {move}")

            result = self._test_hypothesis(lane.board, move)
            print(
                f"[DPP14] Step {steps} – Chose cell ({move.row},{move.col}), result={result}"
            )
            self._visualize_board(lane.board)

            if result == "contradiction":
                print(
                    f"[DPP14] Lane {lane.lane_id} collapsed: Contradiction encountered."
                )
                lane.collapsed = True
            else:
                lane.resonance_zones.append(result)
            steps += 1

    def _test_hypothesis(self, board: Any, move: Any) -> str:
        """Simulates testing a hypothesis."""
        # Use board.grid for direct access or board[(row, col)] for __getitem__
        cell = board.grid[move.row][move.col]
        if cell.is_mine:  # Check if it's a mine using proper attribute
            return "contradiction"
        else:
            # Ensure `row` and `col` are defined before use
            if isinstance(move, tuple):
                row, col = move
            else:
                row, col = move.row, move.col

            board.reveal(row, col)
            return "valid"

    def _visualize_board(self, board: "Board") -> None:
        """(Dev stub) No-op visualiser used only in debug mode."""
        pass
