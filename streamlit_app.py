import time
from typing import Optional, Tuple

import pandas as pd
import streamlit as st

from ai_minesweeper.board import Board, CellState
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


class StreamlitMinesweeperApp:
    def __init__(self) -> None:
        self.logger = None
        self.setup_logging()
        self.initialize_session_state()

    def setup_logging(self) -> None:
        import logging

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def initialize_session_state(self) -> None:
        if "board" not in st.session_state:
            st.session_state.board = None
        if "solver" not in st.session_state:
            st.session_state.solver = None
        if "game_started" not in st.session_state:
            st.session_state.game_started = False
        if "auto_solve_running" not in st.session_state:
            st.session_state.auto_solve_running = False
        if "move_history" not in st.session_state:
            st.session_state.move_history = []
        if "last_action" not in st.session_state:
            st.session_state.last_action = None
        if "meta_mode" not in st.session_state:
            st.session_state.meta_mode = True
        if "show_risk_overlay" not in st.session_state:
            st.session_state.show_risk_overlay = True

    def run(self) -> None:
        st.title("🧠 AI Minesweeper - χ-Recursive Form v1.1.0")
        st.markdown("*Advanced AI with TORUS theory integration and meta-cell confidence*")

        self.create_sidebar()

        col1, col2 = st.columns(2)
        with col1:
            self.create_game_board()
        with col2:
            self.create_control_panel()
            self.create_statistics_panel()

        self.create_visualization_panels()

    def create_sidebar(self) -> None:
        st.sidebar.header("🎮 Game Configuration")
        width = st.sidebar.slider("Board Width", 5, 20, 9)
        height = st.sidebar.slider("Board Height", 5, 20, 9)
        mine_density = st.sidebar.slider("Mine Density (%)", 10, 30, 15)
        mines = int((width * height * mine_density) / 100)
        st.sidebar.write(f"**Mines:** {mines}")

        st.sidebar.header("🤖 AI Configuration")
        meta_mode = st.sidebar.checkbox("Meta-cell confidence mode", value=st.session_state.meta_mode)
        show_risk_overlay = st.sidebar.checkbox("Show risk overlay", value=st.session_state.show_risk_overlay)

        st.sidebar.header("📄 Load Board (CSV)")
        csv_file = st.sidebar.file_uploader("Upload a CSV board", type=["csv"])
        if csv_file is not None:
            try:
                csv_text = csv_file.getvalue().decode("utf-8")
                st.session_state.board = BoardBuilder.from_text(csv_text)
                st.session_state.solver = ConstraintSolver()
                st.session_state.game_started = False
                st.session_state.move_history = []
                st.success("Loaded board from CSV upload.")
            except Exception as e:  # pragma: no cover - UI path
                st.error(f"Failed to load board: {e}")

        st.sidebar.header("🎯 Game Controls")
        if st.sidebar.button("🚀 New Game", type="primary"):
            self.start_new_game(width, height, mines, meta_mode)

        if st.session_state.game_started:
            if st.sidebar.button("🧠 AI Move"):
                self.make_ai_move()
            auto_solve = st.sidebar.button("⚡ Auto-Solve")
            if auto_solve and not st.session_state.auto_solve_running:
                st.session_state.auto_solve_running = True
                st.rerun()
            if st.session_state.auto_solve_running:
                if st.sidebar.button("⏹️ Stop Auto-Solve"):
                    st.session_state.auto_solve_running = False
                else:
                    self.auto_solve_step()

        st.session_state.show_risk_overlay = show_risk_overlay
        st.session_state.meta_mode = meta_mode

    def start_new_game(self, width: int, height: int, mines: int, meta_mode: bool) -> None:
        st.session_state.board = Board(width, height, mines)
        st.session_state.solver = ConstraintSolver()
        st.session_state.game_started = False
        st.session_state.auto_solve_running = False
        st.session_state.move_history = []
        st.session_state.last_action = None
        st.session_state.meta_mode = meta_mode
        st.success(f"New {width}x{height} game created with {mines} mines!")

    def create_game_board(self) -> None:
        st.header("🎯 Game Board")
        if st.session_state.board is None:
            st.info("👆 Configure and start a new game in the sidebar!")
            return

        board = st.session_state.board
        status_col1, status_col2, status_col3 = st.columns(3)
        with status_col1:
            remaining = getattr(board, "remaining_mines", None)
            if remaining is None and hasattr(board, "mines_remaining"):
                remaining = board.mines_remaining
            st.metric("Remaining Mines", remaining if remaining is not None else "-")
        with status_col2:
            moves = len(st.session_state.move_history)
            st.metric("Moves Made", moves)
        with status_col3:
            if hasattr(board, "is_solved") and board.is_solved():
                st.success("🎉 SOLVED!")
            elif st.session_state.game_started:
                st.info("🎮 Playing...")
            else:
                st.warning("🔸 Click to start")

        try:
            cols = getattr(board, "n_cols", getattr(board, "width", "?"))
            rows = getattr(board, "n_rows", getattr(board, "height", "?"))
            st.text(f"Board: {cols} x {rows}")
        except Exception as e:  # pragma: no cover - UI path
            st.error(f"Error creating board visualization: {e}")

        if st.session_state.board and not board.is_solved():
            self.create_interactive_controls()

    def create_interactive_controls(self) -> None:
        st.subheader("🎮 Manual Controls")
        col1, col2 = st.columns(2)
        cols = getattr(st.session_state.board, "n_cols", getattr(st.session_state.board, "width", 1))
        rows = getattr(st.session_state.board, "n_rows", getattr(st.session_state.board, "height", 1))
        with col1:
            x = int(st.number_input("X Coordinate", 0, int(cols) - 1, 0))
            y = int(st.number_input("Y Coordinate", 0, int(rows) - 1, 0))
        with col2:
            if st.button("🔍 Reveal Cell"):
                self.manual_reveal(x, y)
            if st.button("🚩 Flag Cell"):
                self.manual_flag(x, y)

    def manual_reveal(self, x: int, y: int) -> None:
        board = st.session_state.board
        if not st.session_state.game_started:
            board.place_mines((x, y))
            st.session_state.game_started = True
        success = board.reveal_cell(x, y)
        self.record_move("reveal", (x, y), success)
        if not success:
            st.error(f"💥 Mine hit at ({x}, {y})! Game Over.")
        elif board.is_solved():
            st.success("🎉 Congratulations! Board solved!")
        st.rerun()

    def manual_flag(self, x: int, y: int) -> None:
        board = st.session_state.board
        state = board.cell_states[(x, y)] if hasattr(board, "cell_states") else None
        if state == CellState.HIDDEN:
            board.flag_cell(x, y)
            self.record_move("flag", (x, y), True)
            st.rerun()
        elif state in [CellState.FLAGGED, CellState.SAFE_FLAGGED]:
            board.unflag_cell(x, y)
            self.record_move("unflag", (x, y), True)
            st.rerun()

    def make_ai_move(self) -> None:
        if not st.session_state.game_started:
            cols = getattr(st.session_state.board, "n_cols", getattr(st.session_state.board, "width", 1))
            rows = getattr(st.session_state.board, "n_rows", getattr(st.session_state.board, "height", 1))
            center_x = int(cols) // 2
            center_y = int(rows) // 2
            st.session_state.board.place_mines((center_x, center_y))
            st.session_state.board.reveal_cell(center_x, center_y)
            st.session_state.game_started = True
            self.record_move("reveal", (center_x, center_y), True)
        solution = st.session_state.solver.solve_step(st.session_state.board)
        if solution["action"] == "none":
            st.warning("AI: No valid moves found.")
            return
        if solution["action"] == "contradiction":
            st.error("AI: Contradiction detected in board state!")
            return
        action = solution["action"]
        position = solution["position"]
        confidence = solution.get("confidence", 0.5)
        reason = solution.get("reason", "No reason provided")
        success = True
        if action == "reveal":
            success = st.session_state.board.reveal_cell(*position)
        elif action == "flag":
            safe_flag = st.session_state.meta_mode and confidence < 0.9
            st.session_state.board.flag_cell(*position, safe_flag=safe_flag)
        st.session_state.solver.update_outcome(action, position, success, st.session_state.board)
        self.record_move(action, position, success, ai_move=True, confidence=confidence, reason=reason)
        if not success:
            st.error(f"💥 AI hit a mine at {position}! Game Over.")
            st.session_state.auto_solve_running = False
        elif st.session_state.board.is_solved():
            st.success("🎉 AI solved the board!")
            st.session_state.auto_solve_running = False
        st.rerun()

    def auto_solve_step(self) -> None:
        if not st.session_state.board.is_solved():
            self.make_ai_move()
            time.sleep(0.5)
        else:
            st.session_state.auto_solve_running = False

    def record_move(
        self,
        action: str,
        position: Tuple[int, int],
        success: bool,
        ai_move: bool = False,
        confidence: Optional[float] = None,
        reason: Optional[str] = None,
    ) -> None:
        move_record = {
            "move_number": len(st.session_state.move_history) + 1,
            "action": action,
            "position": position,
            "success": success,
            "ai_move": ai_move,
            "confidence": confidence,
            "reason": reason,
            "timestamp": time.time(),
        }
        st.session_state.move_history.append(move_record)
        st.session_state.last_action = move_record

    def create_control_panel(self) -> None:
        st.header("🤖 AI Control Panel")
        if not st.session_state.solver:
            st.info("Start a game to see AI controls")
            return
        if st.session_state.last_action and st.session_state.last_action["ai_move"]:
            last = st.session_state.last_action
            st.write(f"**Last AI Action:** {last['action']} at {last['position']}")
            if last["confidence"] is not None:
                st.write(f"**Confidence:** {last['confidence']:.3f}")
            if last["reason"]:
                st.write(f"**Reason:** {last['reason']}")
        if st.session_state.game_started and not st.session_state.board.is_solved():
            try:
                recommendation = st.session_state.solver.solve_step(st.session_state.board)
                if recommendation["action"] != "none":
                    st.subheader("💡 AI Recommendation")
                    st.write(
                        f"**Action:** {recommendation['action']} at {recommendation.get('position', 'N/A')}"
                    )
                    st.write(f"**Confidence:** {recommendation.get('confidence', 0.5):.3f}")
                    st.write(f"**Reason:** {recommendation.get('reason', 'No reason')}")
            except Exception as e:  # pragma: no cover - UI path
                st.error(f"Error getting AI recommendation: {e}")

    def create_statistics_panel(self) -> None:
        st.header("📊 Statistics")
        if not st.session_state.solver:
            return
        try:
            stats = st.session_state.solver.get_solver_statistics()
            st.subheader("🎯 Game Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Solver Iterations", stats.get("solver_iterations", 0))
                st.metric("Active Constraints", stats.get("active_constraints", 0))
            with col2:
                st.metric("χ-Cycle Progress", stats.get("chi_cycle_progress", 0))
                confidence_val = (
                    stats.get("policy_stats", {})
                    .get("confidence_stats", {})
                    .get("current_confidence", 0.0)
                )
                st.metric("Current Confidence", f"{confidence_val:.3f}")
            if st.session_state.move_history:
                ai_moves = [m for m in st.session_state.move_history if m["ai_move"]]
                if ai_moves:
                    success_rate = len([m for m in ai_moves if m["success"]]) / len(ai_moves)
                    confidences = [m["confidence"] for m in ai_moves if m["confidence"] is not None]
                    avg_confidence = (sum(confidences) / len(confidences)) if confidences else 0.0
                    st.subheader("🎯 AI Performance")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Success Rate", f"{success_rate:.1%}")
                    with c2:
                        st.metric("Avg Confidence", f"{avg_confidence:.3f}")
        except Exception as e:  # pragma: no cover - UI path
            st.error(f"Error displaying statistics: {e}")

    def create_visualization_panels(self) -> None:
        if not st.session_state.solver or not st.session_state.board:
            return
        tab1, tab2, tab3 = st.tabs(["📈 Confidence Trends", "🎯 Risk Analysis", "📜 Move History"])
        with tab1:
            self.create_confidence_visualization()
        with tab2:
            self.create_risk_analysis()
        with tab3:
            self.create_move_history()

    def create_confidence_visualization(self) -> None:
        st.subheader("📈 χ-Recursive Confidence Evolution")
        confidence_history = getattr(st.session_state.board, "confidence_history", [])
        if confidence_history:
            df = pd.DataFrame({"Step": list(range(1, len(confidence_history) + 1)), "Confidence": confidence_history})
            st.line_chart(df.set_index("Step"))
        else:
            st.info("No confidence data available yet. Make some AI moves to see trends.")

    def create_risk_analysis(self) -> None:
        st.subheader("🎯 Risk Assessment Analysis")
        if not st.session_state.game_started:
            st.info("Start the game to see risk analysis.")
            return
        risk_map = st.session_state.solver.risk_assessor.calculate_risk_map(st.session_state.board)
        if not risk_map:
            st.info("No hidden cells to analyze.")
            return
        rows = [
            {"Position": f"({r},{c})", "Risk": float(risk)}
            for (r, c), risk in sorted(risk_map.items(), key=lambda kv: kv[1])[:10]
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    def create_move_history(self) -> None:
        st.subheader("📜 Move History")
        if not st.session_state.move_history:
            st.info("No moves recorded yet.")
            return
        df_data = []
        for move in st.session_state.move_history:
            pos = move["position"]
            df_data.append(
                {
                    "Move": move["move_number"],
                    "Action": move["action"],
                    "Position": f"({pos[0]}, {pos[1]})",
                    "Success": "✅" if move["success"] else "❌",
                    "Player": "🤖 AI" if move["ai_move"] else "👤 Human",
                    "Confidence": f"{move['confidence']:.3f}" if move["confidence"] is not None else "N/A",
                }
            )
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Move History", csv, "minesweeper_moves.csv", "text/csv")


def main() -> None:
    app = StreamlitMinesweeperApp()
    app.run()


if __name__ == "__main__":
    main()
